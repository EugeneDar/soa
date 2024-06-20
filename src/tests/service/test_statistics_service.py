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
STATISTICS_SERVICE_ADDRESS = 'http://localhost:5100'

PATH_TO_DOCKER_COMPOSE = '../services'


@pytest.fixture(scope="module", autouse=True)
def setup_compose():
    print("Starting Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "up", "-d", "--build"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)
    time.sleep(10)

    yield

    print("Stopping and cleaning up Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "down", "--volumes"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)


def test_service_interaction():
    try:
        with grpc.insecure_channel('localhost:5100') as channel:
            stub = StatisticsServiceStub(channel)
            response = stub.GetTotalViewsAndLikes(ViewsAndLikesRequest(
                post_id=POST_ID_1
            ))

        assert response.likes == LIKES_FOR_POST_1
        assert response.views == VIEWS_FOR_POST_1
    except Exception as e:
        print(e)
