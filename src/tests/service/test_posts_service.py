import grpc
import sys
import os
import subprocess
import time
import requests
import pytest


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from services.users.app.api.posts.posts_pb2 import CreatePostRequest, UpdatePostRequest, DeletePostRequest, GetPostByIdRequest, ListPostsRequest
from services.users.app.api.posts.posts_pb2_grpc import PostServiceStub


POSTS_SERVICE_ADDRESS = 'localhost:5300'

PATH_TO_DOCKER_COMPOSE = '../services'


@pytest.fixture(scope="module", autouse=True)
def setup_compose():
    print("Starting Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "up", "-d", "--build"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)
    time.sleep(10)

    yield

    print("Stopping and cleaning up Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "down", "--volumes"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)


def test_posts_create_post():
    with grpc.insecure_channel(POSTS_SERVICE_ADDRESS) as channel:
        stub = PostServiceStub(channel)
        response = stub.CreatePost(CreatePostRequest(
            title='some title',
            content='some text here',
            user_id=1
        ))

    assert response.title == 'some title'
    assert int(response.created_at) != 0
    assert response.created_at == response.updated_at


def test_posts_create_and_update_post():
    with grpc.insecure_channel(POSTS_SERVICE_ADDRESS) as channel:
        stub = PostServiceStub(channel)
        response = stub.CreatePost(CreatePostRequest(
            title='title',
            content='text',
            user_id=1
        ))

    assert response.title == 'title'
    post_id = response.id

    time.sleep(2)  # to have different created_at and updated_at

    with grpc.insecure_channel(POSTS_SERVICE_ADDRESS) as channel:
        stub = PostServiceStub(channel)
        response = stub.UpdatePost(UpdatePostRequest(
            id=post_id,
            title='other title',
            content='other text',
            user_id=1
        ))

    assert response.title == 'other title'
    assert response.created_at != response.updated_at
