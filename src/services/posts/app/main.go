package main

import (
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/grpclog"
	"net"

	pb "grpc-server/api/posts"
)

type postServer struct {
	pb.UnimplementedPostServiceServer
	// Здесь можно добавить необходимые зависимости, например, доступ к базе данных
}

func (s *postServer) CreatePost(ctx context.Context, req *pb.CreatePostRequest) (*pb.Post, error) {
	// Логика создания нового поста
	// ...
	return &pb.Post{
		Id:           1,
		Title:        req.Title,
		Body:         req.Body,
		CreationTime: 123456789,
		UserId:       req.UserId,
	}, nil
}

func (s *postServer) UpdatePost(ctx context.Context, req *pb.UpdatePostRequest) (*pb.Post, error) {
	// Логика обновления поста
	// ...
	return &pb.Post{
		Id:           req.Id,
		Title:        req.Title,
		Body:         req.Body,
		CreationTime: 123456789,
		UserId:       1,
	}, nil
}

func (s *postServer) DeletePost(ctx context.Context, req *pb.DeletePostRequest) (*pb.Post, error) {
	// Логика удаления поста
	// ...
	return &pb.Post{
		Id:           req.Id,
		Title:        "Post Title",
		Body:         "Post Body",
		CreationTime: 123456789,
		UserId:       1,
	}, nil
}

func (s *postServer) GetPostById(ctx context.Context, req *pb.GetPostByIdRequest) (*pb.Post, error) {
	// Логика получения поста по ID
	// ...
	return &pb.Post{
		Id:           req.Id,
		Title:        "Post Title",
		Body:         "Post Body",
		CreationTime: 123456789,
		UserId:       1,
	}, nil
}

func (s *postServer) ListPosts(ctx context.Context, req *pb.ListPostsRequest) (*pb.ListPostsResponse, error) {
	// Логика получения списка постов с пагинацией
	// ...
	return &pb.ListPostsResponse{
		Posts: []*pb.Post{
			{Id: 1, Title: "Post 1", Body: "Body 1", CreationTime: 123456789, UserId: 1},
			{Id: 2, Title: "Post 2", Body: "Body 2", CreationTime: 987654321, UserId: 2},
		},
		TotalCount: 2,
	}, nil
}

func main() {
	listener, err := net.Listen("tcp", ":5300")
	if err != nil {
		grpclog.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterPostServiceServer(s, &postServer{})

	grpclog.Printf("server listening at %v", listener.Addr())
	if err := s.Serve(listener); err != nil {
		grpclog.Fatalf("failed to serve: %v", err)
	}
}
