from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User


def module_1(bd_name):
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished != True).all()
    for i in lst:
        print(i)


module_1(input())
