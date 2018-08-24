from app.api import bp
from flask import jsonify, request
from app.models import User
from app.api.error import bad_request
from app import db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('参数错误')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('该用户名已被注册')
    if User.query.filter_by(username=data['email']).first():
        return bad_request('邮箱已被注册')
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data:
        return bad_request('参数错误')
    setattr(user, 'email', data['email'])
    setattr(user, 'username', data['username'])
    db.session.commit()
    return jsonify(user.to_dict())
