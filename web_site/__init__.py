from flask import Flask  # загрузка Flask
from flask_sqlalchemy import SQLAlchemy  # библиотека для работы с базой данных
from os import path  # проверяет существования пути. Существование файла или папки
from flask_login import LoginManager  # модуль для системы авторизации
from flask_migrate import Migrate  # модуль для миграций
from flask_admin import Admin # модуль для панели администратора
from flask_admin.contrib.sqla import ModelView # табличку для визуализации модели из базы данных


# В этом файле у нас описан запуск нашего приложения и связь файлов в проекте

db = SQLAlchemy()  # создание базы данных
DB_NAME = "database.sqlite3"  # название базы данных
migrate = Migrate()  # создание миграций для базы данных


def create_app():  # запустить сервер
    app = Flask(__name__)  # название проекта внутри фласка
    app.config['SECRET_KEY'] = "qwe123asd"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # наша БД будет называться DB-NAME
    db.init_app(app)  # запускается база данных
    migrate.init_app(app, db)  # подключаются миграции


    from .views import views  # подключается файл views( логика открытия информации на сайте)
    from .auth import auth  # авторизация и регистрация на сайте

    app.register_blueprint(views,
                           url_prefix="/")  # связывание отдельных файликов с основным приложением.  app.register_blueprint - привязка файла к init
    app.register_blueprint(auth,
                           url_prefix="/")  # связывание отдельных файликов с основным приложением.  app.register_blueprint - привязка файла к init

    from web_site.models import \
        Experts,AgesHoroscop  # import из базы данных таблицу с экспертами. Тут логика работы с базы данных, поэтому оно не привязывается
    from .models import Zodiacs # импортируем таблицу с зодиаками
    admin = Admin(app, name='Astrology', template_mode='bootstrap3') # создаём панель администратора
    admin.add_view(ModelView(Zodiacs, db.session)) # добавляем таблицу с зодиаками в панель администратора
    admin.add_view(ModelView(AgesHoroscop, db.session))
    create_database(app)  # создаются таблицы внутри базы данных . А здесь привязывается по-другому

    # сохранение авторизованного пользователя у себя в браузере.
    login_manager = LoginManager()  # Создание модуля авторизации
    login_manager.login_view = "auth.login"  # указываем название функции для авторизации на сайте
    login_manager.init_app(app)  # подключение модуля авторизации к нашему сайту (связываем)

    @login_manager.user_loader  # описываем способ получения авторизованного пользователя с базы данных. Всю информацию о пользователе с сервера
    def load_user(id):
        return Experts.query.get(int(id))  # сделать запрос к базе данных и получить пользователя по его id

    return app  # вернуть приложение. компанует и возращает единой переменной app


def create_database(app):  # функция по созданию базы данных
    if not path.exists("website/" + DB_NAME):  # если база данных не существует, то она создается
        db.create_all(app=app)  # создание базы данных
