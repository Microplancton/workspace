# -*- coding: utf-8 -*-

import random
import string

def generate_password(length):
    """Генерирует пароль заданной длины"""

    char = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(char) for _ in range(length))
    return password

def main():
    """Вводится длина пароля и генерится пароль"""

    length = int(input())
    password = generate_password(length)
    return password

if __name__ == "__main__":
    main()
