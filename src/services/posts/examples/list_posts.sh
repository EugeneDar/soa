### List Posts
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"user_id": 1, "page": 1, "limit": 10}'  -plaintext localhost:5300 posts.PostService/ListPosts
