from data.db_session import global_init, create_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User


def module_1(bd_name):
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(Department).get(1)
    jobs = db_sess.query(Jobs).all()
    for elem in lst.members.split(', '):
        user = db_sess.query(User).get(int(elem))
        s = 0
        for job in jobs:
            if str(elem) in job.collaborators.split(', '):
                s += job.work_size
        if s > 25:
            print(user.surname, user.name)


module_1(input())
