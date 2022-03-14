from data.db_session import global_init, create_session
from data.users import User


def module_1(bd_name):
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(User).filter(User.age < 18).all()
    for i in lst:
        print(i, i.age, 'years')


module_1(input())
