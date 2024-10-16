import grpc
import sys
import os
import subprocess
import time
import requests
import pytest


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from services.statistics.app.api.statistics.statistics_pb2 import ViewsAndLikesRequest, TopPostsRequest, Empty
from services.statistics.app.api.statistics.statistics_pb2_grpc import StatisticsServiceStub


POST_ID_1 = 'abacaba'
LIKES_FOR_POST_1 = 2
VIEWS_FOR_POST_1 = 5
STATISTICS_SERVICE_ADDRESS = 'localhost:5100'

PATH_TO_DOCKER_COMPOSE = '../services'


def init_clickhouse():
    url = 'http://localhost:8123'

    query = """
    CREATE TABLE post_views (
        post_id String,
        viewed_at DateTime,
        post_author_id String,
        event_author_id String
    ) ENGINE = MergeTree()
    ORDER BY post_id;
    """
    response = requests.post(url, data=query)
    print(response)
    query = """
    CREATE TABLE post_likes (
        post_id String,
        liked_at DateTime,
        post_author_id String,
        event_author_id String
    ) ENGINE = MergeTree()
    ORDER BY post_id;
    """
    response = requests.post(url, data=query)
    print(response)
    query = """
    INSERT INTO post_views (post_id, viewed_at, post_author_id, event_author_id) VALUES 
    ('abacaba', '2023-10-01 12:34:56', 'author1', 'viewer1'),
    ('abacaba', '2023-10-02 13:45:56', 'author1', 'viewer2'),
    ('abacaba', '2023-10-02 13:55:56', 'author1', 'viewer3'),
    ('abacaba', '2023-10-02 13:41:56', 'author1', 'viewer4'),
    ('abacaba', '2023-10-03 14:56:56', 'author1', 'viewer5');
    """
    response = requests.post(url, data=query)
    print(response)
    query = """
    INSERT INTO post_likes (post_id, liked_at, post_author_id, event_author_id) VALUES 
    ('abacaba', '2023-10-01 12:34:56', 'author1', 'liker1'),
    ('abacaba', '2023-10-02 13:45:56', 'author1', 'liker2');
    """
    response = requests.post(url, data=query)
    print(response)


@pytest.fixture(scope="module", autouse=True)
def setup_compose():
    print("Starting Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "up", "-d", "--build"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)
    time.sleep(10)
    init_clickhouse()

    yield

    print("Stopping and cleaning up Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "down", "--volumes"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)


def test_statistics_get_total_views_and_likes():
    with grpc.insecure_channel(STATISTICS_SERVICE_ADDRESS) as channel:
        stub = StatisticsServiceStub(channel)
        response = stub.GetTotalViewsAndLikes(ViewsAndLikesRequest(
            post_id=POST_ID_1
        ))

    assert response.likes == LIKES_FOR_POST_1
    assert response.views == VIEWS_FOR_POST_1
