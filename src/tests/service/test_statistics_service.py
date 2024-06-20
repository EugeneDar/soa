import time
import unittest
import grpc
import sys
import os
import pytest
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from services.statistics.app.api.statistics.statistics_pb2 import ViewsAndLikesRequest, TopPostsRequest, Empty
from services.statistics.app.api.statistics.statistics_pb2_grpc import StatisticsServiceStub


pytest_plugins = ["docker_compose"]

POST_ID_1 = 'abacaba'
LIKES_FOR_POST_1 = 2
VIEWS_FOR_POST_1 = 5
STATISTICS_SERVICE_ADDRESS = 'statistics-service:5100'


@pytest.fixture(scope="module")
def grpc_service(module_scoped_container_getter):
    service = module_scoped_container_getter.get("statistics-service").network_info[0]
    host, port = service.hostname, service.host_port
    grpc_channel = grpc.insecure_channel(f"{host}:{port}")

    for _ in range(10):
        try:
            grpc.channel_ready_future(grpc_channel).result(timeout=1)
            return grpc_channel
        except grpc.FutureTimeoutError:
            time.sleep(1)

    pytest.fail("GRPC service did not become available in time")


def test_addition(grpc_service):
    """Тестирование функции сложения"""
    grpc_channel = grpc_service
    stub = StatisticsServiceStub(grpc_channel)

    response = stub.GetTotalViewsAndLikes(ViewsAndLikesRequest(
        post_id=POST_ID_1
    ))

    assert response.likes == LIKES_FOR_POST_1
    assert response.views == VIEWS_FOR_POST_1
