import os
import django
import json

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spaces.models import Space
from django.core import serializers

# Получаем все пространства
spaces = Space.objects.all()

if not spaces:
    print("Внимание: в базе данных нет ни одного пространства!")
    print("Сначала добавьте пространства через админку.")
    exit()

# Сериализуем в JSON с правильной кодировкой
data = serializers.serialize('json', spaces, indent=2, ensure_ascii=False)

# Убеждаемся, что папка fixtures существует
os.makedirs('spaces/fixtures', exist_ok=True)

# Сохраняем в файл с UTF-8
with open('spaces/fixtures/spaces.json', 'w', encoding='utf-8') as f:
    f.write(data)

print(f'✅ Экспортировано {spaces.count()} пространств в spaces/fixtures/spaces.json')