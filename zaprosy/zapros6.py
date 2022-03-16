from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User


def module_1(bd_name):
    lst1 = []
    global_init(bd_name)
    db_sess = create_session()
    lst = db_sess.query(Jobs).all()
    max_count = 0
    for i in lst:
        max_count = len(i.collaborators.split(', ')) if len(
            i.collaborators.split(', ')) > max_count else max_count
    for i in [i for i in lst if len(i.collaborators.split(', ')) == max_count]:
        team_leader = db_sess.query(User).filter(User.id == i.team_leader).one()
        lst1.append((team_leader.surname, team_leader.name))
    for i in list(set(lst1)):
        print(*i)


module_1(input())
