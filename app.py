from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)  # создаем сервер для сайта
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"  # подключаем файлик с базы данных
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


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


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        surname = request.form.get("surname")
        second_name = request.form.get("second_name")
        date = request.form.get("date")
        gender = request.form.get("gender")
        specialization = request.form.get("specialization")
        phone = request.form.get("phone")
        agreement = request.form.get("agreement")
        date_parsed = datetime.strptime(date,"%Y-%m-%d") # Y - год, m - месяц, d - день , переводим в формат даты, для того, чтобы сравнить с датой
        min_date = datetime.strptime("1935-01-01", "%Y-%m-%d")
        # email_exists = Experts.query.filter_by(email=email).first() # проверяет в базе данных на существование email

        # if email_exists:
        #     flash('Данный e-mail уже зарегестрирован.', category='error')
        if password1 != password2:
            flash('Введенные пароли не совпадают', category="error")

        elif len(password1) < 6:
            flash('Введенный пароль слишком короткий.', category='error')
        elif len(email) < 4 or "@" not in email:
            flash("Email не корректен.", category='error')
        elif agreement != "on":
            flash("Примите согласие об обработке персональных данных.", category='error')
        elif password1 == "qwerty" or password1 == "123456":
            flash("пароль слишком легкий, придумайте другой")

            # new_user = User(email=email, username=username, password=generate_password_hash(
            #     password1, method='sha256'))
            # db.session.add(new_user)
            # db.session.commit()
            # login_user(new_user, remember=True)
            # flash('User created!')
            # return redirect(url_for('views.home'))

    return render_template("registration.html")


@app.route('/')
def home():  # put application's code here
    return render_template('base.html')


@app.route('/new')
def test():  # put application's code here
    return render_template('base.html')


@app.route('/signup')
def signup():  # put application's code here
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
