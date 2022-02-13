from flask import Blueprint, render_template, request, redirect, url_for, json
from flask_login import login_required, current_user
from . import db
from .models import Experts
# В этом файле мы описываем логику открытия информационных страниц сайта

views = Blueprint("views", __name__)


# идет переход
@views.route('/')
def home(): # put application's code here
    experts = Experts.query.all()
    return render_template('home.html', user=current_user, experts = experts)


# логика информационных страниц сайта
