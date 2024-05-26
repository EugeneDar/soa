### Get top posts [By likes]
grpcurl -proto ../../../resources/protos/statistics/statistics.proto -d '{"sort_by": "LIKES"}' -plaintext localhost:5100 statistics.StatisticsService/GetTopPosts


### Get top posts [By views]
grpcurl -proto ../../../resources/protos/statistics/statistics.proto -d '{"sort_by": "VIEWS"}' -plaintext localhost:5100 statistics.StatisticsService/GetTopPosts
