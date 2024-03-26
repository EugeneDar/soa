import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS

from database.database import db
from util.util import get_field, password_hasher, connect_to_db
from schemas.user_schema import UserSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

from models.user import User

CORS(app)

jwt = JWTManager(app)

user_schema = UserSchema()


@app.route("/signup", methods=["POST"])
def create_user():
    user_details = request.json

    username = get_field(request, 'username')
    password = get_field(request, 'password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        return jsonify(message="User with such username already exists."), 400

    new_user = user_schema.load(user_details)
    new_user['password'] = password_hasher(username, password)

    new_user = User(**new_user)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


@app.route("/login", methods=["POST"])
def login():
    username = get_field(request, 'username')
    password = get_field(request, 'password')

    user = User.query.filter_by(username=username).first()
    if user is None or password_hasher(username, password) != user.password:
        return jsonify(message="Invalid credentials"), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/users/<username>", methods=["PUT"])
@jwt_required()
def update_user(username):
    user_details = request.json
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(message="User not found"), 404

    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="Unauthorized request"), 401

    user = user_schema.load(user_details, partial=True)

    db.session.commit()
    return jsonify(user_schema.dump(user))


if __name__ == "__main__":
    connect_to_db(db, app)
    app.run(host='0.0.0.0', debug=True)
