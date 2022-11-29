# My_blog
### Описание
Социальная сеть для публикации личных дневников, с возможностью подписок и комментирования.
### Технологии
Python 3.9
Django 4.1
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv/scripts/activate
``` 
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Выполните миграции
```
python manage.py makemigrations
python manage.py migrat
``` 
- Выполните команду:
```
python manage.py runserver
```
- Запустите сайт:
```
http://127.0.0.1:8000