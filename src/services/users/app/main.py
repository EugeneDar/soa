import os
import json
import grpc
from datetime import datetime
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from kafka import KafkaProducer

from database.database import db
from util.util import get_field, password_hasher, connect_to_db, proto_post_to_dict
from schemas.user_schema import UserSchema

from api.posts.posts_pb2 import CreatePostRequest, UpdatePostRequest, DeletePostRequest, GetPostByIdRequest, ListPostsRequest
from api.posts.posts_pb2_grpc import PostServiceStub

from api.statistics.statistics_pb2 import ViewsAndLikesRequest, TopPostsRequest, Empty
from api.statistics.statistics_pb2_grpc import StatisticsServiceStub

# Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
from models.user import User
CORS(app)
jwt = JWTManager(app)

# MySql
user_schema = UserSchema()

# Kafka
producer = None  # init in main


# TODO move this function to the separate file
def call_grpc_get_post_by_id(post_id):
    with grpc.insecure_channel('posts-service:5300') as channel:
        stub = PostServiceStub(channel)
        return stub.GetPostById(GetPostByIdRequest(
            id=post_id
        ))


@app.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'OK'})


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
    response = call_grpc_get_post_by_id(post_id)
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
    event_author_id = User.query.filter_by(username=get_jwt_identity()).first().id
    post_author_id = call_grpc_get_post_by_id(post_id).user_id

    message = {
        'post_id': post_id,
        'post_author_id': post_author_id,
        'viewed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'event_author_id': event_author_id
    }
    producer.send('post_views', message)
    return jsonify({'success': True})


@app.route("/posts/<post_id>/likes", methods=["POST"])
@jwt_required()
def add_post_like(post_id):
    event_author_id = User.query.filter_by(username=get_jwt_identity()).first().id
    post_author_id = call_grpc_get_post_by_id(post_id).user_id

    message = {
        'post_id': post_id,
        'post_author_id': post_author_id,
        'liked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'event_author_id': event_author_id
    }
    producer.send('post_likes', message)
    return jsonify({'success': True})


@app.route("/posts/<post_id>/statistics", methods=["GET"])
def get_post_statistics(post_id):
    with grpc.insecure_channel('statistics-service:5100') as channel:
        stub = StatisticsServiceStub(channel)
        response = stub.GetTotalViewsAndLikes(ViewsAndLikesRequest(
            post_id=post_id
        ))
    return jsonify({'post_id': post_id, 'views': response.views, 'likes': response.likes})


@app.route("/posts/top", methods=["GET"])
def get_top_posts():
    sort_by_param = request.args.get('sort_by', 'likes').upper()
    sort_by = TopPostsRequest.SortBy.LIKES if sort_by_param == 'LIKES' else TopPostsRequest.SortBy.VIEWS

    with grpc.insecure_channel('statistics-service:5100') as channel:
        stub = StatisticsServiceStub(channel)
        response = stub.GetTopPosts(TopPostsRequest(
            sort_by=sort_by
        ))

    if sort_by_param == 'LIKES':
        posts = [
            {
                'post_id': p.post_id,
                'author_username': User.query.filter_by(id=p.author_id).first().username,
                'likes': p.likes
            }
            for p in response.posts
        ]
    else:
        posts = [
            {
                'post_id': p.post_id,
                'author_username': User.query.filter_by(id=p.author_id).first().username,
                'views': p.views
            }
            for p in response.posts
        ]
    return jsonify(posts)


@app.route("/users/top", methods=["GET"])
def get_top_users():
    with grpc.insecure_channel('statistics-service:5100') as channel:
        stub = StatisticsServiceStub(channel)
        response = stub.GetTopUsers(Empty())

    users = [
        {
            'username': User.query.filter_by(id=u.user_id).first().username,
            'likes': u.likes
        }
        for u in response.users
    ]
    return jsonify(users)


if __name__ == "__main__":
    connect_to_db(db, app)

    producer = KafkaProducer(
        bootstrap_servers=['kafka:29092'],
        api_version=(0, 11, 5),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        request_timeout_ms=3000
    )

    app.run(host='0.0.0.0', debug=True)
