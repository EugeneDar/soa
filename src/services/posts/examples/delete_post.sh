### Delete Post
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"id": "DcT6-VToI-Fjng-BXoH", "user_id": 1}' -plaintext localhost:5300 posts.PostService/DeletePost