#!/bin/bash

# Обновление системы
sudo apt update
sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv git

# Установка и настройка PostgreSQL (если требуется)
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Создание пользователя и базы данных PostgreSQL
sudo -u postgres psql -c "CREATE USER flask_user WITH PASSWORD 'securepassword';"
sudo -u postgres psql -c "CREATE DATABASE flask_inventory WITH OWNER flask_user;"

# Клонирование репозитория
git clone https://github.com/msrv-tech/flask-inventory.git /opt/flask_inventory
cd /opt/flask_inventory

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
echo "DATABASE_URL=postgresql://flask_user:securepassword@localhost/flask_inventory" > .env
echo "SECRET_KEY=your_secret_key_here" >> .env

# Инициализация базы данных
flask db upgrade

# Запуск приложения
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &

# Настройка брандмауэра (открытие порта 5000)
sudo ufw allow 5000/tcp

# Уведомление о завершении
echo "Flask-приложение успешно настроено и запущено!"
echo "Доступно по адресу: http://<IP_вашей_ВМ>:5000"