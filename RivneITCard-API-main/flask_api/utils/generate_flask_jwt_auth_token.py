import jwt
from datetime import datetime, timedelta, timezone
from flask import jsonify
from flask_api import app

def generate_token(id):
    # задаємо ключ для підпису токена (варто зберігати його в конфігураційному файлі)
    secret_key = '55555'

    # задаємо дату створення токена
    issued_at = datetime.utcnow()

    # задаємо дату, до якої токен буде дійсним (наприклад, на 1 годину від дати створення)
    expires_at = issued_at + timedelta(hours=1)#upg to 744 after test

    # створюємо payload (вміст) токена
    payload = {
        'id': id,
        'issued_at': issued_at,
        'expires_at': expires_at.isoformat(),
    }

    # генеруємо токен з використанням підпису
    token = jwt.encode(payload, secret_key, algorithm='HS256', json_encoder=app.json_encoder)

    return token


def update_token_expiry(token):
    secret_key = '55555'
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        new_expires_at = datetime.utcnow() + timedelta(hours=1)
        payload['expires_at'] = new_expires_at.isoformat()  # Оновлюємо термін дії токена
        updated_token = jwt.encode(payload, secret_key, algorithm='HS256')
        return updated_token
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None


import jwt
from datetime import datetime
from dateutil import parser


def verify_token(token):
    secret_key = '55555'

    try:
        # Декодуємо токен з використанням ключа для підпису
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Перевіряємо структуру payload і наявність 'expires_at'
        if 'expires_at' not in payload:
            print("Token does not contain 'expires_at'")
            return False

        # Парсимо 'expires_at' з рядка у datetime об'єкт
        expires_at_datetime = parser.parse(payload['expires_at'])

        # Перетворюємо expires_at_datetime у наївний datetime
        if expires_at_datetime.tzinfo is None:
            # Якщо expires_at_datetime наївний, перетворюємо його у UTC
            expires_at_datetime = expires_at_datetime.replace(tzinfo=timezone.utc)
        else:
            # Інакше конвертуємо у UTC
            expires_at_datetime = expires_at_datetime.astimezone(timezone.utc)

        # Перевіряємо, чи токен ще дійсний
        if datetime.now(timezone.utc) < expires_at_datetime:
            print("True")
            return True
        else:
            print("Token has expired")
            return False

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return False
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return False
    except ValueError as e:
        print(f"Error parsing 'expires_at': {e}")
        return False
