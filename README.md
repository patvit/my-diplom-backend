# Облачное хранилище My Cloud
Мой дипломный проект  

### Запуск на рег.ру
http://194.58.114.103:3000/


### Запуск локально
___
1. Установка зависимостей
```
pip install -r requirements.txt
```

2. Установка зависимостей React

```
перейти в папку Diplom-front
cd Diplom-front
выполнить команду
yarn
```

3. Проверьте файл конфигурации, измените конфигурацию базы данных
```
# Diplom/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
} 

```

4. Перенос базы данных
```
python manage.py migrate

```
5. Создайте суперпользователя
```
python manage.py createsuperuser
```
6. Запустите локальный сервер
```
python manage.py runserver
```
### Скриншот страницы (картинки находятся в папке images)
___ 
Панель администратора

![screen shot](Images/admin.png) 

Вход или Регистрация  

![screen shot](Images/main.png)  

Список файлов  

![screen shot](Images/myfiles.png)

