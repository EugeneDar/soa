### List Posts
grpcurl -proto ../../../resources/protos/posts/posts.proto -d '{"page": 1, "page_size": 10}' -plaintext localhost:5300 posts.PostService/ListPosts
