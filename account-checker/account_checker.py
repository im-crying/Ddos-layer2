#!/usr/bin/env python3
"""
BOT KIỂM TRA THÔNG TIN TÀI KHOẢN TRƯỚC KHI GIAO DỊCH
Chỉ sử dụng phương pháp kiểm tra công khai, hợp pháp
"""
import re
import json
import hashlib
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple

class AccountSafetyChecker:
    def __init__(self):
        """Khởi tạo bot với cơ sở dữ liệu cảnh báo"""
        self.setup_database()
        self.load_warning_patterns()
    
    def setup_database(self):
        """Thiết lập SQLite database để lưu lịch sử kiểm tra"""
        self.conn = sqlite3.connect('account_checker.db')
        self.cursor = self.conn.cursor()
        
        # Tạo bảng lưu trữ tài khoản đã kiểm tra
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS checked_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT,
                account_type TEXT,
                email TEXT,
                phone TEXT,
                creation_date TEXT,
                risk_score INTEGER,
                check_result TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tạo bảng mẫu cảnh báo
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warning_patterns (
                id INTEGER PRIMARY KEY,
                pattern_type TEXT,
                pattern_value TEXT,
                risk_level TEXT,
                description TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_warning_patterns(self):
        """Tải các mẫu cảnh báo (có thể import từ file)"""
        # Mẫu email disposable/tạm thời
        self.disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'trashmail.com',
            'temp-mail.org', 'fakeinbox.com', 'getairmail.com'
        ]
        
        # Mẫu số điện thoại đáng ngờ
        self.suspicious_phones = []
    
    def check_email_safety(self, email: str) -> Dict:
        """Kiểm tra độ an toàn của email"""
        result = {
            'email': email,
            'is_valid_format': False,
            'is_disposable': False,
            'has_public_breaches': False,
            'age_indicator': 'unknown'
        }
        
        # Kiểm tra định dạng email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            result['is_valid_format'] = True
            
            # Kiểm tra domain disposable
            domain = email.split('@')[1].lower()
            for disposable in self.disposable_domains:
                if disposable in domain:
                    result['is_disposable'] = True
                    break
            
            # Kiểm tra tuổi email dựa trên username
            username = email.split('@')[0].lower()
            suspicious_terms = ['temp', 'fake', 'test', 'dummy', '123456']
            if any(term in username for term in suspicious_terms):
                result['age_indicator'] = 'new'
            else:
                result['age_indicator'] = 'established'
        
        return result
    
    def check_phone_safety(self, phone: str) -> Dict:
        """Kiểm tra số điện thoại"""
        result = {
            'phone': phone,
            'is_valid_vn_format': False,
            'carrier': 'unknown',
            'is_virtual': False,
            'age_indicator': 'unknown'
        }
        
        # Chuẩn hóa số điện thoại
        phone = phone.replace(' ', '').replace('+84', '0')
        
        # Kiểm tra định dạng số VN
        vn_pattern = r'^(09|03|07|08|05)[0-9]{8}$'
        if re.match(vn_pattern, phone):
            result['is_valid_vn_format'] = True
            
            # Xác định nhà mạng
            prefix = phone[:3]
            carriers = {
                '096': 'Viettel', '097': 'Viettel', '098': 'Viettel',
                '086': 'Viettel', '032': 'Viettel', '033': 'Viettel',
                '034': 'Viettel', '035': 'Viettel', '036': 'Viettel',
                '037': 'Viettel', '038': 'Viettel', '039': 'Viettel',
                '090': 'Mobifone', '093': 'Mobifone', '089': 'Mobifone',
                '091': 'Vinaphone', '094': 'Vinaphone', '088': 'Vinaphone',
                '092': 'Vietnamobile',
                '099': 'Gmobile',
            }
            result['carrier'] = carriers.get(prefix, 'Unknown')
            
            # Kiểm tra số ảo (thường dùng cho app)
            virtual_prefixes = ['087', '055', '056']
            if prefix in virtual_prefixes:
                result['is_virtual'] = True
            
            # Đánh giá độ "cũ" dựa trên số
            if phone.endswith(('0000', '1111', '1234', '9999')):
                result['age_indicator'] = 'suspicious'
            else:
                result['age_indicator'] = 'normal'
        
        return result
    
    def check_account_age(self, creation_date: str) -> Dict:
        """Kiểm tra tuổi tài khoản"""
        result = {
            'creation_date': creation_date,
            'age_in_days': None,
            'is_fresh_account': False,
            'age_category': 'unknown'
        }
        
        try:
            # Parse ngày tạo
            if '-' in creation_date:
                create_dt = datetime.strptime(creation_date, '%Y-%m-%d')
            else:
                create_dt = datetime.strptime(creation_date, '%d/%m/%Y')
            
            current_dt = datetime.now()
            age_days = (current_dt - create_dt).days
            
            result['age_in_days'] = age_days
            
            if age_days < 30:
                result['is_fresh_account'] = True
                result['age_category'] = 'new'
            elif age_days < 365:
                result['age_category'] = 'medium'
            else:
                result['age_category'] = 'old'
                
        except:
            pass
        
        return result
    
    def check_blacklist(self, account_info: Dict) -> List[str]:
        """Kiểm tra thông tin trong danh sách cảnh báo"""
        warnings = []
        
        # Kiểm tra trong database local
        if 'email' in account_info and account_info['email']:
            self.cursor.execute('''
                SELECT description FROM warning_patterns 
                WHERE pattern_type = 'email' AND ? LIKE '%' || pattern_value || '%'
            ''', (account_info['email'],))
            for row in self.cursor.fetchall():
                warnings.append(f"Email cảnh báo: {row[0]}")
        
        if 'phone' in account_info and account_info['phone']:
            self.cursor.execute('''
                SELECT description FROM warning_patterns 
                WHERE pattern_type = 'phone' AND ? LIKE '%' || pattern_value || '%'
            ''', (account_info['phone'],))
            for row in self.cursor.fetchall():
                warnings.append(f"Số điện thoại cảnh báo: {row[0]}")
        
        return warnings
    
    def calculate_risk_score(self, checks: Dict) -> Tuple[int, str]:
        """Tính điểm rủi ro và đưa ra kết luận"""
        risk_score = 0
        reasons = []
        
        # Email disposable: +30 điểm
        if checks.get('email', {}).get('is_disposable', False):
            risk_score += 30
            reasons.append("Email tạm thời/disposable")
        
        # Email format không hợp lệ: +20 điểm
        if not checks.get('email', {}).get('is_valid_format', True):
            risk_score += 20
            reasons.append("Email không đúng định dạng")
        
        # Số điện thoại ảo: +25 điểm
        if checks.get('phone', {}).get('is_virtual', False):
            risk_score += 25
            reasons.append("Số điện thoại ảo (virtual)")
        
        # Số điện thoại không hợp lệ: +20 điểm
        if not checks.get('phone', {}).get('is_valid_vn_format', True):
            risk_score += 20
            reasons.append("Số điện thoại không hợp lệ")
        
        # Tài khoản mới (dưới 30 ngày): +15 điểm
        if checks.get('account_age', {}).get('is_fresh_account', False):
            risk_score += 15
            reasons.append("Tài khoản mới tạo (<30 ngày)")
        
        # Có cảnh báo từ blacklist: +40 điểm mỗi cảnh báo
        blacklist_warnings = checks.get('blacklist_warnings', [])
        risk_score += len(blacklist_warnings) * 40
        if blacklist_warnings:
            reasons.append(f"Có {len(blacklist_warnings)} cảnh báo từ danh sách đen")
        
        # Xác định kết quả
        if risk_score >= 60:
            result = "HIGH_RISK"
        elif risk_score >= 30:
            result = "MEDIUM_RISK"
        else:
            result = "LOW_RISK"
        
        return risk_score, result, reasons
    
    def full_account_check(self, account_data: Dict) -> Dict:
        """Thực hiện kiểm tra toàn diện tài khoản"""
        print("\n" + "="*60)
        print("ĐANG KIỂM TRA THÔNG TIN TÀI KHOẢN...")
        print("="*60)
        
        checks = {}
        
        # 1. Kiểm tra email
        if 'email' in account_data and account_data['email']:
            checks['email'] = self.check_email_safety(account_data['email'])
        
        # 2. Kiểm tra số điện thoại
        if 'phone' in account_data and account_data['phone']:
            checks['phone'] = self.check_phone_safety(account_data['phone'])
        
        # 3. Kiểm tra tuổi tài khoản
        if 'creation_date' in account_data and account_data['creation_date']:
            checks['account_age'] = self.check_account_age(account_data['creation_date'])
        
        # 4. Kiểm tra blacklist
        checks['blacklist_warnings'] = self.check_blacklist(account_data)
        
        # 5. Tính điểm rủi ro
        risk_score, risk_level, risk_reasons = self.calculate_risk_score(checks)
        
        # 6. Lưu kết quả vào database
        self.save_check_result(account_data, risk_score, risk_level)
        
        # 7. Tạo báo cáo
        report = {
            'account_info': account_data,
            'checks_performed': checks,
            'risk_assessment': {
                'score': risk_score,
                'level': risk_level,
                'reasons': risk_reasons
            },
            'final_verdict': 'PASS' if risk_level == 'LOW_RISK' else 'FAIL',
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def save_check_result(self, account_data: Dict, risk_score: int, risk_level: str):
        """Lưu kết quả kiểm tra vào database"""
        try:
            self.cursor.execute('''
                INSERT INTO checked_accounts 
                (account_id, account_type, email, phone, creation_date, risk_score, check_result)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                account_data.get('account_id', 'N/A'),
                account_data.get('account_type', 'unknown'),
                account_data.get('email', ''),
                account_data.get('phone', ''),
                account_data.get('creation_date', ''),
                risk_score,
                risk_level
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Lỗi khi lưu kết quả: {e}")
    
    def display_report(self, report: Dict):
        """Hiển thị báo cáo kiểm tra"""
        print("\n" + "="*60)
        print("KẾT QUẢ KIỂM TRA TÀI KHOẢN")
        print("="*60)
        
        acc_info = report['account_info']
        print(f"\n📋 THÔNG TIN TÀI KHOẢN:")
        print(f"   ID: {acc_info.get('account_id', 'N/A')}")
        print(f"   Loại: {acc_info.get('account_type', 'N/A')}")
        print(f"   Email: {acc_info.get('email', 'N/A')}")
        print(f"   SĐT: {acc_info.get('phone', 'N/A')}")
        print(f"   Ngày tạo: {acc_info.get('creation_date', 'N/A')}")
        
        print(f"\n🔍 KẾT QUẢ KIỂM TRA:")
        
        # Hiển thị chi tiết check email
        if 'email' in report['checks_performed']:
            email_check = report['checks_performed']['email']
            print(f"\n   📧 Email Check:")
            print(f"      Định dạng hợp lệ: {'✅' if email_check['is_valid_format'] else '❌'}")
            print(f"      Email tạm thời: {'❌ CÓ' if email_check['is_disposable'] else '✅ KHÔNG'}")
            print(f"      Độ tin cậy: {email_check['age_indicator'].upper()}")
        
        # Hiển thị chi tiết check phone
        if 'phone' in report['checks_performed']:
            phone_check = report['checks_performed']['phone']
            print(f"\n   📱 Phone Check:")
            print(f"      Định dạng hợp lệ: {'✅' if phone_check['is_valid_vn_format'] else '❌'}")
            print(f"      Nhà mạng: {phone_check['carrier']}")
            print(f"      Số ảo: {'❌ CÓ' if phone_check['is_virtual'] else '✅ KHÔNG'}")
            print(f"      Độ tin cậy: {phone_check['age_indicator'].upper()}")
        
        # Hiển thị tuổi tài khoản
        if 'account_age' in report['checks_performed']:
            age_check = report['checks_performed']['account_age']
            if age_check['age_in_days']:
                print(f"\n   📅 Account Age:")
                print(f"      Tuổi tài khoản: {age_check['age_in_days']} ngày")
                print(f"      Phân loại: {age_check['age_category'].upper()}")
        
        # Hiển thị blacklist warnings
        if report['checks_performed'].get('blacklist_warnings'):
            print(f"\n   ⚠️  CẢNH BÁO TỪ DANH SÁCH ĐEN:")
            for warning in report['checks_performed']['blacklist_warnings']:
                print(f"      • {warning}")
        
        print(f"\n🎯 ĐÁNH GIÁ RỦI RO:")
        risk = report['risk_assessment']
        print(f"   Điểm rủi ro: {risk['score']}/100")
        print(f"   Mức độ rủi ro: {risk['level']}")
        
        if risk['reasons']:
            print(f"   Lý do:")
            for reason in risk['reasons']:
                print(f"      • {reason}")
        
        print(f"\n" + "="*60)
        
        # HIỂN THỊ KẾT QUẢ CUỐI CÙNG
        if report['final_verdict'] == 'PASS':
            print("✅ KẾT LUẬN: Done check! Tài khoản CÓ THỂ giao dịch")
        else:
            print("❌ KẾT LUẬN: Giao dịch không thành công! Rủi ro cao")
        
        print("="*60)

def main():
    """Giao diện chính của bot"""
    checker = AccountSafetyChecker()
    
    print("="*60)
    print("🤖 BOT CHECK THÔNG TIN TÀI KHOẢN GIAO DỊCH")
    print("="*60)
    print("⚠️  Lưu ý: Bot chỉ kiểm tra dựa trên thông tin công khai")
    print("   Không đảm bảo 100% an toàn giao dịch")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        print("1. Kiểm tra tài khoản mới")
        print("2. Xem lịch sử kiểm tra")
        print("3. Thêm mẫu cảnh báo")
        print("4. Thoát")
        print("-"*60)
        
        choice = input("Chọn chức năng (1-4): ")
        
        if choice == "1":
            print("\n" + "="*60)
            print("NHẬP THÔNG TIN TÀI KHOẢN CẦN KIỂM TRA")
            print("="*60)
            
            account_data = {}
            account_data['account_id'] = input("ID/Username tài khoản: ").strip()
            account_data['account_type'] = input("Loại tài khoản (Facebook/Google/Github...): ").strip()
            account_data['email'] = input("Email đăng ký (nếu có): ").strip()
            account_data['phone'] = input("Số điện thoại liên kết (nếu có): ").strip()
            account_data['creation_date'] = input("Ngày tạo (YYYY-MM-DD hoặc DD/MM/YYYY): ").strip()
            
            # Thực hiện kiểm tra
            report = checker.full_account_check(account_data)
            
            # Hiển thị kết quả
            checker.display_report(report)
            
            # Hỏi người dùng có lưu không
            save = input("\nLưu kết quả kiểm tra? (y/n): ").lower()
            if save == 'y':
                print("✅ Đã lưu vào database!")
        
        elif choice == "2":
            print("\n" + "="*60)
            print("LỊCH SỬ KIỂM TRA")
            print("="*60)
            
            checker.cursor.execute('''
                SELECT account_id, account_type, email, check_result, checked_at 
                FROM checked_accounts 
                ORDER BY checked_at DESC 
                LIMIT 10
            ''')
            
            rows = checker.cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"\nID: {row[0]}")
                    print(f"Loại: {row[1]}")
                    print(f"Email: {row[2]}")
                    print(f"Kết quả: {row[3]}")
                    print(f"Thời gian: {row[4]}")
                    print("-"*40)
            else:
                print("Chưa có lịch sử kiểm tra nào.")
        
        elif choice == "3":
            print("\n" + "="*60)
            print("THÊM MẪU CẢNH BÁO MỚI")
            print("="*60)
            
            pattern_type = input("Loại (email/phone): ").strip().lower()
            pattern_value = input("Giá trị cần cảnh báo (VD: baduser@gmail.com): ").strip()
            description = input("Mô tả cảnh báo: ").strip()
            
            try:
                checker.cursor.execute('''
                    INSERT INTO warning_patterns (pattern_type, pattern_value, risk_level, description)
                    VALUES (?, ?, 'high', ?)
                ''', (pattern_type, pattern_value, description))
                checker.conn.commit()
                print("✅ Đã thêm mẫu cảnh báo mới!")
            except Exception as e:
                print(f"❌ Lỗi: {e}")
        
        elif choice == "4":
            print("\nCảm ơn đã sử dụng bot!")
            checker.conn.close()
            break
        
        else:
            print("Vui lòng chọn 1-4")

if __name__ == "__main__":
    main()
