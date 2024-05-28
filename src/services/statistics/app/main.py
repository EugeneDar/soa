from concurrent.futures import ThreadPoolExecutor
import grpc

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


class StatisticsService(StatisticsServiceServicer):

    def GetTotalViewsAndLikes(self, request, context):
        query = GET_TOTAL_VIEWS_AND_LIKES_TEMPLATE.format(post_id=request.post_id)
        result = clickhouse_request(query)
        return ViewsAndLikesResponse(views=int(result[0][0]), likes=int(result[0][1]))

    def GetTopPosts(self, request, context):
        if request.sort_by == TopPostsRequest.LIKES:
            query = GET_TOP_POSTS_TEMPLATE.format(table_name='post_likes')
            result = clickhouse_request(query)
            return TopPostsResponse(posts=[
                Post(post_id=result[i][0], likes=int(result[i][1]))
                for i in range(len(result))
            ])
        else:
            query = GET_TOP_POSTS_TEMPLATE.format(table_name='post_views')
            result = clickhouse_request(query)
            return TopPostsResponse(posts=[
                Post(post_id=result[i][0], views=int(result[i][1]))
                for i in range(len(result))
            ])

    def GetTopUsers(self, request, context):
        query = GET_TOP_USERS_TEMPLATE.format(table_name='post_likes')
        result = clickhouse_request(query)
        return TopUsersResponse(users=[
            User(user_id=result[i][0], likes=int(result[i][1]))
            for i in range(len(result))
        ])


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_StatisticsServiceServicer_to_server(StatisticsService(), server)
    server.add_insecure_port('[::]:5100')
    server.start()
    print("Server started on port 5100")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
