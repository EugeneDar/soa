import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from util.util import get_field
from models.user import User
from schemas.user_schema import UserSchema

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
db = SQLAlchemy(app)
jwt = JWTManager(app)

user_schema = UserSchema()


@app.route("/signup", methods=["POST"])
def create_user():
    user_details = request.json
    new_user = user_schema.load(user_details)

    password = generate_password_hash(user_details.get('password'))
    new_user['password'] = password

    existing_user = User.query.filter_by(username=new_user['username']).first()
    if existing_user is not None:
        return jsonify(message="User with such username already exists."), 400

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


@app.route("/login", methods=["POST"])
def login():
    username = get_field(request, 'username')
    password = get_field(request, 'password')

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify(message="Invalid credentials"), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/users/<id>", methods=["PUT"])
@jwt_required
def update_user(id):
    user_details = request.json
    user = User.query.get(id)
    if user is None:
        return jsonify(message="User not found"), 404

    user = user_schema.load(user_details, partial=True)

    db.session.commit()
    return jsonify(user_schema.dump(user))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
