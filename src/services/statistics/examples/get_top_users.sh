### Get top users by likes
grpcurl -proto ../../../resources/protos/statistics/statistics.proto -d '{}' -plaintext localhost:5100 statistics.StatisticsService/GetTopUsers
