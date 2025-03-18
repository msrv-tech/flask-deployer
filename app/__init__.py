from flask import Flask
from config import Config  # Импортируем конфигурацию

app = Flask(__name__)
app.config.from_object(Config)  # Загружаем конфигурацию

# Импортируем routes ПОСЛЕ создания app
from app import routes