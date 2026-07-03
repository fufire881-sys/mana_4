from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _fernet():
    return Fernet(settings.PASSWORD_RECOVERY_KEY.encode())


def encrypt_password(plain_password):
    if not plain_password:
        return ""
    return _fernet().encrypt(plain_password.encode()).decode()


def decrypt_password(token):
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode()).decode()
    except InvalidToken:
        return ""
