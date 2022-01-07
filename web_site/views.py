from flask import Blueprint, render_template, request, redirect, url_for, json
from flask_login import login_required, current_user
from . import db

# В этом файле мы описываем логику открытия информационных страниц сайта

views = Blueprint("views", __name__)

# идет переход
@views.route('/')
def home():  # put application's code here
    return render_template('base.html',user = current_user)

# логика информационных страниц сайта

