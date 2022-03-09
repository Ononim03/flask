from datetime import datetime

from flask import Flask
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def get_all_users():
    db_sess = db_session.create_session()


if __name__ == '__main__':
    db_session.global_init(input())
