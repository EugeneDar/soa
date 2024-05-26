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
from util.templates import GET_TOP_POSTS_TEMPLATE


class StatisticsService(StatisticsServiceServicer):

    def GetTotalViewsAndLikes(self, request, context):
        # if post:
        #     return ViewsAndLikesResponse(post_id=request.post_id, views=post["views"], likes=post["likes"])
        # else:
        #     context.set_code(grpc.StatusCode.NOT_FOUND)
        #     context.set_details('Post not found')
        #     return ViewsAndLikesResponse()

        return ViewsAndLikesResponse(views=1, likes=2)

    def GetTopPosts(self, request, context):
        if request.sort_by == TopPostsRequest.LIKES:
            query = GET_TOP_POSTS_TEMPLATE.format(table_name='post_likes')
            result = clickhouse_request(query)
            return TopPostsResponse(posts=[
                Post(post_id=result[i][0], views=0, likes=int(result[i][1]))
                for i in range(len(result))
            ])
        else:
            query = GET_TOP_POSTS_TEMPLATE.format(table_name='post_views')
            result = clickhouse_request(query)
            return TopPostsResponse(posts=[
                Post(post_id=result[i][0], views=int(result[i][1]), likes=0)
                for i in range(len(result))
            ])

    def GetTopUsers(self, request, context):
        top_users = [
            User(user_id=str(index), views=index, likes=index)
            for index in range(3)
        ]
        return TopUsersResponse(users=top_users)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_StatisticsServiceServicer_to_server(StatisticsService(), server)
    server.add_insecure_port('[::]:5100')
    server.start()
    print("Server started on port 5100")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
