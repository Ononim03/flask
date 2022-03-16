from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User


def module_1(bd_name):
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(User).filter(User.address == 'module_1', User.age < 21).all()
    for i in lst:
        i.address = 'module_3'
    db_sess.commit()


module_1(input())
