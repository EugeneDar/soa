### Get Post by ID
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"id": "EMr4-NKdV-XEYx-B0y3", "user_id": 1}' -plaintext localhost:5300 posts.PostService/GetPostById