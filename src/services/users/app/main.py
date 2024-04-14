import os

import grpc
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS

from database.database import db
from util.util import get_field, password_hasher, connect_to_db, proto_post_to_dict
from schemas.user_schema import UserSchema
from api.posts.posts_pb2 import CreatePostRequest, UpdatePostRequest, DeletePostRequest, GetPostByIdRequest, ListPostsRequest
from api.posts.posts_pb2_grpc import PostServiceStub

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

    return jsonify({
        'access_token': access_token,
        'user_id': user.id
    })


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


@app.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    post_details = request.json
    user_id = User.query.filter_by(username=get_jwt_identity()).first().id

    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        response = stub.CreatePost(CreatePostRequest(
            title=post_details['title'],
            content=post_details['content'],
            user_id=user_id
        ))

    return jsonify(proto_post_to_dict(response)), 201


@app.route("/posts/<post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    post_details = request.json
    user_id = User.query.filter_by(username=get_jwt_identity()).first().id

    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        response = stub.UpdatePost(UpdatePostRequest(
            id=post_id,
            title=post_details['title'],
            content=post_details['content'],
            user_id=user_id
        ))

    return jsonify(proto_post_to_dict(response))


@app.route("/posts/<post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = User.query.filter_by(username=get_jwt_identity()).first().id

    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        response = stub.DeletePost(DeletePostRequest(
            id=post_id,
            user_id=user_id
        ))

    return jsonify({
        'success': response.success
    })


@app.route("/posts/<post_id>", methods=["GET"])
@jwt_required()
def get_post_by_id(post_id):
    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        response = stub.GetPostById(GetPostByIdRequest(
            id=post_id
        ))

    return jsonify(proto_post_to_dict(response))


@app.route("/posts", methods=["GET"])
@jwt_required()
def list_posts():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        response = stub.ListPosts(ListPostsRequest(
            user_id=request.json['user_id'],
            page=page,
            limit=limit
        ))

    posts = [
        proto_post_to_dict(post)
        for post in response.posts
    ]

    return jsonify({
        'posts': posts,
        'total_count': response.total_count,
        'page': page,
        'limit': limit
    })

@app.route("/posts/<post_id>/views", methods=["POST"])
@jwt_required()
def add_post_view(post_id):
    # TODO
    return jsonify({'success': True})


@app.route("/posts/<post_id>/likes", methods=["POST"])
@jwt_required()
def add_post_like(post_id):
    # TODO
    return jsonify({'success': True})



if __name__ == "__main__":
    connect_to_db(db, app)
    app.run(host='0.0.0.0', debug=True)
