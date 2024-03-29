### Get Post by ID
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"id": 1}' -plaintext localhost:5300 posts.PostService/GetPostById