### Update Post
grpcurl -proto ../../../resources/protos/posts/posts.proto -d  '{"id": "EMr4-NKdV-XEYx-B0y3", "title": "Updated Post", "content": "This post has been updated", "user_id": 1}' -plaintext localhost:5300 posts.PostService/UpdatePost