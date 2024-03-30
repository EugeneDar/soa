package main

import (
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/grpclog"
	"net"
	"sync"
	"time"

	pb "grpc-server/api/posts"
)

type postServer struct {
	pb.UnimplementedPostServiceServer
	mu    sync.Mutex
	posts []*pb.Post
}

func (s *postServer) CreatePost(ctx context.Context, req *pb.CreatePostRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	post := &pb.Post{
		Id:        int64(len(s.posts) + 1),
		Title:     req.Title,
		Content:   req.Content,
		UserId:    req.UserId,
		CreatedAt: time.Now().Unix(),
		UpdatedAt: time.Now().Unix(),
	}

	s.posts = append(s.posts, post)

	return post, nil
}

func (s *postServer) UpdatePost(ctx context.Context, req *pb.UpdatePostRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, post := range s.posts {
		if post.Id == req.Id {
			if post.UserId != req.UserId {
				return nil, grpc.Errorf(codes.PermissionDenied, "you are not allowed to update this post")
			}
			post.Title = req.Title
			post.Content = req.Content
			post.UpdatedAt = time.Now().Unix()
			return post, nil
		}
	}

	return nil, grpc.Errorf(codes.NotFound, "post not found")
}

func (s *postServer) DeletePost(ctx context.Context, req *pb.DeletePostRequest) (*pb.DeletePostResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for i, post := range s.posts {
		if post.Id == req.Id {
			if post.UserId != req.UserId {
				return nil, grpc.Errorf(codes.PermissionDenied, "you are not allowed to delete this post")
			}
			s.posts = append(s.posts[:i], s.posts[i+1:]...)
			return &pb.DeletePostResponse{Success: true}, nil
		}
	}

	return nil, grpc.Errorf(codes.NotFound, "post not found")
}

func (s *postServer) GetPostById(ctx context.Context, req *pb.GetPostByIdRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, post := range s.posts {
		if post.Id == req.Id {
			if post.UserId != req.UserId {
				return nil, grpc.Errorf(codes.PermissionDenied, "you are not allowed to access this post")
			}
			return post, nil
		}
	}

	return nil, grpc.Errorf(codes.NotFound, "post not found")
}

func (s *postServer) ListPosts(ctx context.Context, req *pb.ListPostsRequest) (*pb.ListPostsResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	var posts []*pb.Post
	for _, post := range s.posts {
		if post.UserId == req.UserId {
			posts = append(posts, post)
		}
	}

	offset := (req.Page - 1) * req.Limit
	limit := int(offset) + int(req.Limit)
	if limit > len(posts) {
		limit = len(posts)
	}

	return &pb.ListPostsResponse{
		Posts:      posts[offset:limit],
		TotalCount: int64(len(posts)),
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
