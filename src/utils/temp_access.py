
import random
import string
from cachetools import TTLCache, cached
import time

# Создаем кэш с временем жизни 5 минут
cache = TTLCache(maxsize=100, ttl=300)

def generate_verification_code(user_id: int):
    """Генерация и сохранение кода верификации."""
    code = ''.join(random.choices(string.digits, k=6))
    cache[user_id] = code
    return code

def verify_code(user_id: int, input_code: str):
    """Проверка кода верификации."""
    stored_code = str(cache.get(user_id))
    if stored_code and stored_code == input_code:
        return True
    return False
