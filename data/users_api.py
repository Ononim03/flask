import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(rules=('-jobs', '-jobs.user'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(rules=('-jobs', '-jobs.user'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'about', 'email', 'password',
                  'created_date']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if 'id' in request.json and db_sess.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists.'})
    new_user = User()
    if 'id' in request.json:
        new_user.id = request.json['id']
    if 'surname' in request.json:
        new_user.surname = request.json['surname']
    if 'name' in request.json:
        new_user.name = request.json['name']
    if 'about' in request.json:
        new_user.about = request.json['about']
    if 'email' in request.json:
        new_user.email = request.json['email']
    if 'password' in request.json:
        new_user.password = request.json['password']
    if 'created_date' in request.json:
        new_user.created_date = request.json['created_date']
    db_sess.add(new_user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Jobs).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


def put_users(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    if 'id' in request.json and db_sess.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists.'})

    if 'id' in request.json:
        user.id = request.json['id']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'about' in request.json:
        user.about = request.json['about']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'password' in request.json:
        user.password = request.json['password']
    if 'created_date' in request.json:
        user.created_date = request.json['created_date']
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
