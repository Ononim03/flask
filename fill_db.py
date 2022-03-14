from datetime import datetime

from data import db_session
from main import create_job, create_user

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    create_user(name='Scott', surname='Ridley', age=21, speciality='captain', position='research engineer',
                address='module_1',
                email='scott_chief@mars.org')
    create_user('Evans', 'Mihail', 21, 'colonist', 'engineer', 'module_1',
                'evans_mihail@mars.org')
    create_user('Evans', 'Farhad', 21, 'colonist', 'engineer', 'module_1',
                'evans_farhad@mars.org')
    create_user('Evans', 'Ivan', 21, 'colonist', 'engineer', 'module_1',
                'evans_ivan@mars.org')
    create_job(team_leader=2,
               job='deployment of residential modules 1 and 2',
               work_size=15,
               collaborators='2, 3',
               start_date=datetime.now().date(),
               is_finished=False)
    create_job(team_leader=2,
               job='2',
               work_size=20,
               collaborators='2, 3, 4',
               start_date=datetime.now().date(),
               is_finished=False)
    create_job(team_leader=3,
               job='3',
               work_size=25,
               collaborators='2, 3, 4, 5',
               start_date=datetime.now().date(),
               is_finished=False)
