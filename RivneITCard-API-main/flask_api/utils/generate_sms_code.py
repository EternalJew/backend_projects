import random


def generated_sms_code():
    # Генеруємо 4-х значний код
    code = random.randint(1000, 9999)

    # Повертаємо код у вигляді рядка
    return str(code)