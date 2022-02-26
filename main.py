from flask import Flask, render_template
from werkzeug.utils import redirect

import data.db_session
from data import db_session
from data.news import News
from data.users import User
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = data.db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()

        if user and user.check_password(form.password.data):
            return redirect('success')
    return render_template('login.html', title='Регистрация', form=form)


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('all_success.html')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()


def users_add():
    user = User()
    user.name = 'name'
    user.about = 'biography'
    user.email = 'mail'
