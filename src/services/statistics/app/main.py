from concurrent.futures import ThreadPoolExecutor
import grpc
import sys

from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))


from api.statistics.statistics_pb2 import (
    TopPostsRequest,
    ViewsAndLikesResponse,
    TopPostsResponse,
    TopUsersResponse,
    Post,
    User,
)
from api.statistics.statistics_pb2_grpc import StatisticsServiceServicer, add_StatisticsServiceServicer_to_server
from util.util import clickhouse_request
from util.templates import (
    GET_TOTAL_VIEWS_AND_LIKES_TEMPLATE,
    GET_TOP_POSTS_TEMPLATE,
    GET_TOP_USERS_TEMPLATE
)


def build_views_and_likes_response(response):
    return ViewsAndLikesResponse(views=int(response[0][0]), likes=int(response[0][1]))


def build_top_posts_responses(response, sorted_by):
    return TopPostsResponse(posts=[
        Post(post_id=row[0], **{sorted_by: int(row[1])})
        for row in response
    ])


def build_top_users_responses(response):
    return TopUsersResponse(users=[
        User(user_id=row[0], likes=int(row[1]))
        for row in response
    ])


class StatisticsService(StatisticsServiceServicer):

    def GetTotalViewsAndLikes(self, request, context):
        query = GET_TOTAL_VIEWS_AND_LIKES_TEMPLATE.format(post_id=request.post_id)
        result = clickhouse_request(query)
        return build_views_and_likes_response(result)

    def GetTopPosts(self, request, context):
        sorted_by = request.sort_by == TopPostsRequest.LIKES
        table_name = 'post_{event}'.format(event=sorted_by)
        query = GET_TOP_POSTS_TEMPLATE.format(table_name=table_name)
        result = clickhouse_request(query)
        return build_top_posts_responses(result, sorted_by)

    def GetTopUsers(self, request, context):
        query = GET_TOP_USERS_TEMPLATE.format(table_name='post_likes')
        result = clickhouse_request(query)
        return build_top_users_responses(result)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_StatisticsServiceServicer_to_server(StatisticsService(), server)
    server.add_insecure_port('[::]:5100')
    server.start()
    print("Server started on port 5100")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
