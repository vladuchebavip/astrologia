from flask import Blueprint, render_template, request, redirect, url_for, json
from flask_login import login_required, current_user
from . import db
from .models import Experts, Zodiacs

# В этом файле мы описываем логику открытия информационных страниц сайта

views = Blueprint("views",
                  __name__)  # подраздел общего сайта в котором описаны элементы сайта связанные с основной логикой


# (Отображение списков экспертов, информационные разделы сайта: 12 месяцев, календарь китайский и т.п. Все что связано с логикой сайта)


# идет переход
@views.route('/')  # мы написали, когда фласк должен вызывать функцию home
def home():  #
    experts = Experts.query.all()  # делаем запрос в базу данных и достаём всех экспертов
    return render_template('home.html', user=current_user,
                           experts=experts)  # пользователь перешёл на корневую страницу сайта, то ему нужно отобразить файл home.html, в который будет вписана информация о экспертах


# функция которая будет отображать информацию об экспертах
@views.route('/expert/<id>')
def experts_info(id):
    expert = Experts.query.filter_by(id=id).first()
    if not expert:
        return render_template("no_expert.html")
    return render_template("expert_info.html", user=current_user, expert=expert)


@views.route("/example")
def example():
    return render_template("example.html", a=["огурцы", "помидоры", "яйца", "курица", "пельмени"])


@views.route('/zodiac/<name>')
def zodiac_info(name):
    zodiac = Zodiacs.query.filter_by(name=name).first()
    if not zodiac:
        return render_template("no_expert.html")
    return render_template("zodiac.html", user=current_user, zodiac=zodiac)
