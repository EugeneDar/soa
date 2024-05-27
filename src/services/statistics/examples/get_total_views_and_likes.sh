### Get views and likes for post by post_id
grpcurl -proto ../../../resources/protos/statistics/statistics.proto -d '{"post_id": "postid"}' -plaintext localhost:5100 statistics.StatisticsService/GetTotalViewsAndLikes
