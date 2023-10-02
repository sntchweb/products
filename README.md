## Описание проекта:

Тестовое задание для НаrdQоdе.  
Проект представляет собой `API` для просмотра информации по продуктам и урокам в этих продуктах.

## Установка:

Клонируйте репозиторий:
```
git clone git@github.com:sntchweb/products.git
```

Создайте и активируйте вертуальное окружение:
  ```
  python -m venv venv
  source venv\Scripts\activate
  ```

Установите зависимости:
```
pip install -r requirements.txt
```

Добавьте `.env` файл в директорию с settings.py. Пример `.env` файла:
```
SECRET_KEY='django-insecure-ka!et2fl)gsdt5j7skr4_ko8ftod#93314y(gmwgmtg4hun*xv+'
DEBUG='True'
ALLOWED_HOSTS = 'localhost localhost:8000 127.0.0.1 127.0.0.1:8000'
```
## Запуск проекта:

Для запуска необходимо из корня проекта выполнить команду:
```
python manage.py runserver
```

Сайт будет доступен по адресу `127.0.0.1:8000`

## Стек технологий:
- Django 4.2
- Python 3.9
- DRF 3.14
- SQLite

## Автор:
Лашин Артём.