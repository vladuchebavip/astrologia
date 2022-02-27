from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import Experts

# В этом файлике описана логика, связанная с авторизацией на сайте и регистрацией

auth = Blueprint("auth", __name__)


@auth.route("/sign_up", methods=['GET', 'POST']) # Get- попасть, Post- списать регистрация, на 64 меняем. Пометка фреймворку, когда нужно запускать sing up
def sign_up(): # регистрация
    if request.method == 'POST': # Списывает и одобряет регистрацию
        print(request.form)
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        surname = request.form.get("surname")
        second_name = request.form.get("second_name")
        date = request.form.get("date")
        gender = request.form.get("gender") == "Мужской"
        specialization = request.form.get("specialization")
        phone = request.form.get("phone")
        agreement = request.form.get("agreement")
        date_parsed = None
        if date:
            date_parsed = datetime.strptime(date,
                                            "%Y-%m-%d")  # Y - год, m - месяц, d - день , переводим в формат даты, для того, чтобы сравнить с датой
        min_date = datetime.strptime("1935-01-01", "%Y-%m-%d")
        max_date = datetime.strptime("2021-12-19", "%Y-%m-%d")
        email_exists = Experts.query.filter_by(email=email).first()  # проверяет в базе данных на существование email

        if email_exists:
            flash('Данный e-mail уже зарегистрирован.', category='danger')
        if password1 != password2:
            flash('Введенные пароли не совпадают', category="danger")

        elif len(password1) < 6:
            flash('Введенный пароль слишком короткий.', category='danger')
        elif len(email) < 4 or "@" not in email:
            flash("Email не корректен.", category='danger')
        elif agreement != "on":
            flash("Примите согласие об обработке персональных данных.", category='danger')
        elif password1 == "qwerty" or password1 == "123456":
            flash("Введенный пароль не корректный.", category='danger')

        elif not min_date <= date_parsed <= max_date:
            flash("Введеная дата рождения не корректна.", category='danger')

        else:

            expert = Experts(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'), birthday=date_parsed, gender=gender, surname=surname,
                             second_name=second_name, specialization=specialization, phone=phone) # Красная - название столбца в базе данных, белое - название переменной в которой хранятся данные считанные с формы, в которую пользователь ввёл их
            db.session.add(expert)  # database.session.add(добавить)
            db.session.commit()  # database.session.commit(сохранить)
            login_user(expert, remember=True)
            flash('User created!')
            return redirect(url_for('auth.my_profile')) # после регистрации, пересылаем пользователя на старницу с личными данными №

    return render_template("registration.html", user=current_user) # возращаёт шаблон со страницы регистрации


# идет регистрация и авторизация

@auth.route("/login", methods=['GET', 'POST']) # запуск страницы с авторизацией, вход логимся
def login(): # Пользователь вводит данные, далее данная функция проверяет данные на корректность
    if request.method == 'POST':
        email = request.form.get("email") # получаем данные с фронтеда
        password = request.form.get("password") # получаем вводимый пароль
        remember_me = request.form.get("remember_me") == ""
        expert = Experts.query.filter_by(email=email).first() # красное - название столбца в базе данных. Находит в базе пользователя, по e-mail который был введён
        if expert: # если мы нашли такого пользователя в базе данных
            if check_password_hash(expert.password, password): # проверяем пароль. expert.password - сохранённый пароль в базе данных, password- ввёл пользователь
                flash("Вы успешно авторизовались!", category='success')
                login_user(expert, remember=remember_me)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль.', category='danger')
        else:
            flash('Данный e-mail не зарегистрирован', category='danger')

    return render_template("login.html", user=current_user)


@auth.route("/my_profile") # мой профиль
def my_profile():
    return render_template("my_profile.html", user=current_user)


@auth.route("/logout") # выход из аккаунта
def logout():
    logout_user()
    return redirect(url_for("views.home", user=current_user))

@auth.route("/edit", methods=['GET', 'POST']) # редактирование профиля
def edit():
    if request.method == 'POST': # все данные пользователя, в чём отличие?
        print(request.form)
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        surname = request.form.get("surname")
        second_name = request.form.get("second_name")
        date = request.form.get("date")
        gender = request.form.get("gender") == "Мужской"
        specialization = request.form.get("specialization")
        phone = request.form.get("phone")
        agreement = request.form.get("agreement")
        date_parsed = None
        if date:
            date_parsed = datetime.strptime(date,
                                            "%Y-%m-%d")  # Y - год, m - месяц, d - день , переводим в формат даты, для того, чтобы сравнить с датой
        min_date = datetime.strptime("1935-01-01", "%Y-%m-%d")
        max_date = datetime.strptime("2021-12-19", "%Y-%m-%d")
        email_exists = Experts.query.filter_by(email=email).first()  # проверяет в базе данных на существование email

        if email_exists and email_exists != current_user.email:
            flash('Данный e-mail уже занят.', category='danger')
        if password1 != password2:
            flash('Введенные пароли не совпадают', category="danger")

        elif len(password1) < 6:
            flash('Введенный пароль слишком короткий.', category='danger')
        elif len(email) < 4 or "@" not in email:
            flash("Email не корректен.", category='danger')
        elif agreement != "on":
            flash("Примите согласие об обработке персональных данных.", category='danger')
        elif password1 == "qwerty" or password1 == "123456":
            flash("Введенный пароль не корректный.", category='danger')

        elif not min_date <= date_parsed <= max_date:
            flash("Введеная дата рождения не корректна.", category='danger')

        else: #   ОСТАНОВИЛСЯ ТУТ

            current_user.email = email
            current_user.name = name
            current_user.password = generate_password_hash(password1, method='sha256')
            current_user.surname = surname
            current_user.second_name = second_name
            current_user.date = date
            current_user.gender = gender
            current_user.specialization = specialization
            current_user.phone = phone
            db.session.commit()
            login_user(current_user, remember=True) # что данная функция делает?
            return redirect(url_for("auth.my_profile")) # что данная функция делает?
    return render_template("edit.html", user=current_user)