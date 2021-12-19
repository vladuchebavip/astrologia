from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# В этом файле описаны таблицы из Базы данных


class Experts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # id - номер специалиста в базе данных(1,2,3...)
    email = db.Column(db.String(50),
                      unique=True)  # Column - столбец ,  String - строка, e-mail не могут быть повторяющимися
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    birthday = db.Column(db.DateTime(timezone=True))  # можем хранить данные
    gender = db.Column(db.Boolean)  # Буливские значение - True и False
    specialty = db.Column(db.String(50))  # специализация
    phone = db.Column(db.String(15))  # номер телфона - строка