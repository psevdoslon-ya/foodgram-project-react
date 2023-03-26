# Foodgram «Продуктовый помощник» 
![example workflow](https://github.com/psevdoslon-ya/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание проекта
Cайт Foodgram «Продуктовый помощник» - это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

[Ссылка на проект на сервере Yandex.Cloud](http://51.250.8.234/)

Логин (email) суперюзера: admin@admin.com

Пароль суперюзера: admin

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Системные требования
- Python 3.7+
- Docker
- Works on Linux, Windows, macOS

## Запуск проекта в контейнере
Клонируйте репозиторий с проектом и перейдите в него:
```
git clone https://github.com/psevdoslon-ya/foodgram-project-react.git

cd foodgram-project-react
```
Создайте и активируйте виртуальное окружение:
```
python3.7 -m venv venv

. venv/bin/activate
```
Перейдите в директорию с файлом docker-compose.yaml:
```
cd infra
```
Cоздать и открыть файл .env с переменными окружения:
```
touch .env
```
Заполнить .env файл переменными окружения (SECRET_KEY см. в файле settings.py). 
Пример файла с переменными окружения .env:
```
#.env
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
POSTGRES_USER=<пользователь бд>
POSTGRES_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ проекта django>
```
Запуск docker-compose.yaml:
```
sudo docker-compose up -d --build
```
После успешного запуска проекта выполните миграции:
```
sudo docker-compose exec backend python manage.py makemigrations

sudo docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input 
```
Наполните БД заготовленными данными:
```
sudo docker-compose exec backend python manage.py loaddata ingredients.json

sudo docker-compose exec backend python manage.py loaddata tags.json
```
Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```
sudo docker-compose down -v
```