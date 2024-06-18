import time
import unittest
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from services.statistics.app.api.statistics.statistics_pb2 import ViewsAndLikesRequest, TopPostsRequest, Empty
from services.statistics.app.api.statistics.statistics_pb2_grpc import StatisticsServiceStub


POST_ID_1 = 'abacaba'
LIKES_FOR_POST_1 = 2
VIEWS_FOR_POST_1 = 5
STATISTICS_SERVICE_ADDRESS = 'statistics-service:5100'


def init_clickhouse():
    pass


class TestMyService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(10)
        init_clickhouse()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_statistics_for_post(self):
        with grpc.insecure_channel(STATISTICS_SERVICE_ADDRESS) as channel:
            stub = StatisticsServiceStub(channel)
            response = stub.GetTotalViewsAndLikes(ViewsAndLikesRequest(
                post_id=POST_ID_1
            ))
        self.assertEqual(response.likes, LIKES_FOR_POST_1)
        self.assertEqual(response.views, VIEWS_FOR_POST_1)


if __name__ == '__main__':
    unittest.main()
