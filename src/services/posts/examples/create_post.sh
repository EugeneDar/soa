### Create post
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"title": "New Post", "content": "This is a new post", "user_id": 1}' -plaintext localhost:5300 posts.PostService/CreatePost
