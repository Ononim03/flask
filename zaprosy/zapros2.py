from data.db_session import global_init, create_session
from data.users import User


def module_1(bd_name):
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(User).filter(User.address == 'module_1', User.speciality.notlike('%engineer%'),
                                     User.position.notlike('%engineer%')).all()
    for i in lst:
        print(i.id)


module_1(input())
