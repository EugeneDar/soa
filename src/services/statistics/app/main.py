from concurrent.futures import ThreadPoolExecutor
import grpc
from api.statistics.statistics_pb2 import ViewsAndLikesResponse, Post, TopPostsResponse, User, TopUsersResponse
from api.statistics.statistics_pb2_grpc import StatisticsServiceServicer, add_StatisticsServiceServicer_to_server


class StatisticsService(StatisticsServiceServicer):

    def GetTotalViewsAndLikes(self, request, context):
        return ViewsAndLikesResponse(views=1, likes=2)

    def GetTopPosts(self, request, context):
        top_posts = [
            Post(post_id=str(index), views=index, likes=index)
            for index in range(5)
        ]
        return TopPostsResponse(posts=top_posts)

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
