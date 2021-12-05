from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return render_template('base.html')


@app.route('/new')
def test():  # put application's code here
    return render_template('new_base.html')


if __name__ == '__main__':
    app.run()
