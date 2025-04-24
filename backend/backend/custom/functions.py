import os, uuid, re
from django.utils import timezone
from rest_framework.exceptions import ValidationError

import random
import string


def check_validate_password(password):
    """Hàm kiểm tra mật khẩu hợp lệ"""
    if len(password) < 8:
        raise ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
    if " " in password:
        raise ValidationError("Mật khẩu không được chứa khoảng trắng.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Mật khẩu phải chứa ít nhất một số.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Mật khẩu phải chứa ít nhất một chữ in hoa.")
    if not any(char in "!@#$%^&*()_+-=" for char in password):
        raise ValidationError("Mật khẩu phải chứa ít nhất một ký tự đặc biệt.")
    return password

def check_validate_username(username):
    """Hàm kiểm tra tính hợp lệ của Username"""
    from django.contrib.auth import get_user_model  # Import tại đây để tránh lỗi vòng lặp
    User = get_user_model()

    if len(username) < 4 or len(username) > 20:
        raise ValidationError("Username phải có độ dài từ 4 đến 20 ký tự.")
    if " " in username:
        raise ValidationError("Username không được chứa khoảng trắng.")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Username chỉ được chứa chữ cái, số và dấu gạch dưới (_).")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username đã tồn tại, vui lòng chọn tên khác.")
    return username

def get_random_password(length=10): # Tạo mật khẩu ngẫu nhiên (quy định mặc định mật khẩu là 10 kí tự)
    if length < 4: # Kiểm tra số liệu tham số nhập vào nếu < 4 thì trả lỗi (khi dev nhập nhầm)
        raise ValueError('Mật khẩu phải có ít nhất 4 ký tự')
    password = [
        random.choice(string.ascii_uppercase), # Lấy ngẫu nhiên một kí tự in hoa
        random.choice(string.ascii_lowercase), # Lấy ngẫu nhiên một kí tự thường
        random.choice(string.digits), # Lấy ngẫu nhiên một kí tự số
        random.choice('!@#$%^&*()_+-=') # Lấy ngẫu nhiên một kí tự đặc biệt
    ]

    all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=' # Thêm các kí tự ngẫu nhiên còn lại cho đủ length=10
    password += random.choices(all_chars, k=length - 4) # Lấy password ở trên (4 kí tự) + kí tự bổ sung thêm (nhớ là phải dùng k=length-4 để trừ đi 4 kí tự password đã có ở trên)

    random.shuffle(password) # Trộn ngẫu nhiên tất cả các kí tự trong password (hàm shuffle chỉ dùng được với list ko dùng được với chuỗi(str), nên password quy định ban đầu phải là một list)
    return ''.join(password) # Trả ra chuỗi kí tự password để gửi cho người dùng


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    result = os.path.join(instance._meta.app_label, instance.__class__.__name__, timezone.datetime.today().strftime("%Y/%m/%d"), f'{str(uuid.uuid4())}.{ext}')
    return result