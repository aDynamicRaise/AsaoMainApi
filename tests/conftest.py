import sys
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Теперь переменные из .env доступны через os.environ
pythonpath = os.environ.get('PYTHONPATH')
if pythonpath:
    sys.path.append(pythonpath)
