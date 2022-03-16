import os

from flask import Flask, request, render_template, make_response, jsonify
from flask_restful import Api
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session, jobs_api
from data.jobs import Jobs
from data.users import User
from data.users_recource import UserListResource, UserResource
from forms.jobsform import JobsForm
from forms.user import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
# для списка объектов
api.add_resource(UserListResource, '/api/v2/users')

# для одного объекта
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = db_sess.query(Jobs).filter(
            (Jobs.user == current_user) | (Jobs.is_finished != True))
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)

    return render_template("index.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
            address=form.address.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.team_leader_id = form.team_leader_id.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.team_leader_id.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.title.data
            jobs.team_leader_id = form.team_leader_id.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter((Jobs.id == id) | (Jobs.id == 1),
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success")
def success():
    return render_template('success.html')


def create_job(**kwargs):
    db_sess = db_session.create_session()

    new_job = Jobs()
    if 'team_leader' in kwargs:
        new_job.team_leader = kwargs['team_leader']
    if 'job' in kwargs:
        new_job.job = kwargs['job']
    if 'work_size' in kwargs:
        new_job.work_size = kwargs['work_size']
    if 'collaborators' in kwargs:
        new_job.collaborators = kwargs['collaborators']
    if 'start_date' in kwargs:
        new_job.start_date = kwargs['start_date']
    if 'end_date' in kwargs:
        new_job.end_date = kwargs['end_date']
    if 'is_finished' in kwargs:
        new_job.is_finished = kwargs['is_finished']

    db_sess.add(new_job)

    db_sess.commit()


def create_user(surname, name, age, position, speciality, address, email):
    user = User()

    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email

    db_sess = db_session.create_session()

    db_sess.add(user)

    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # create_job(team_leader=1,
    #            job='deployment of residential modules 1 and 2',
    #            work_size=15,
    #            collaborators='2, 3',
    #            start_date=datetime.now().date(),
    #            is_finished=False)
    # app.register_blueprint(jobs_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # serve(app, port=port, host='127.0.0.1')
