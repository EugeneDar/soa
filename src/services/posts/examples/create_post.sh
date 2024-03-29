### Create post
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"title": "alice", "body": "hey", "user_id": 1}' -plaintext localhost:5300 posts.PostService/CreatePost