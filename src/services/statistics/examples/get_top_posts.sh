### Get top posts
#grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"title": "New Post", "content": "This is a new post", "user_id": 1}' -plaintext localhost:5300 posts.PostService/CreatePost
grpcurl -proto ../../../resources/protos/statistics/statistics.proto -d '{"sort_by": "LIKES"}' -plaintext localhost:5100 statistics.StatisticsService/GetTopPosts
