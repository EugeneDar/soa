package main

import (
	"go.mongodb.org/mongo-driver/bson"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/grpclog"
	"google.golang.org/grpc/status"
	"net"
	"sync"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"grpc-server/util"

	pb "grpc-server/api/posts"
)

type postServer struct {
	pb.UnimplementedPostServiceServer
	mu         sync.Mutex
	client     *mongo.Client
	collection *mongo.Collection
}

func (s *postServer) CreatePost(ctx context.Context, req *pb.CreatePostRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	postID := util.GenerateRandomID()

	post := &pb.Post{
		Id:        postID,
		Title:     req.Title,
		Content:   req.Content,
		UserId:    req.UserId,
		CreatedAt: time.Now().Unix(),
		UpdatedAt: time.Now().Unix(),
	}

	_, err := s.collection.InsertOne(ctx, post)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to create post: %v", err)
	}

	return post, nil
}

func (s *postServer) UpdatePost(ctx context.Context, req *pb.UpdatePostRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	filter := bson.M{"id": req.Id, "userid": req.UserId}
	update := bson.M{
		"$set": bson.M{
			"title":     req.Title,
			"content":   req.Content,
			"updatedat": time.Now().Unix(),
		},
	}

	result := s.collection.FindOneAndUpdate(ctx, filter, update, options.FindOneAndUpdate().SetReturnDocument(options.After))

	var post pb.Post
	if err := result.Decode(&post); err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, grpc.Errorf(codes.NotFound, "post not found")
		}
		return nil, grpc.Errorf(codes.Internal, "failed to update post: %v", err)
	}

	return &post, nil
}

func (s *postServer) DeletePost(ctx context.Context, req *pb.DeletePostRequest) (*pb.DeletePostResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	filter := bson.M{"id": req.Id, "userid": req.UserId}

	result, err := s.collection.DeleteOne(ctx, filter)
	if err != nil {
		return nil, grpc.Errorf(codes.Internal, "failed to delete post: %v", err)
	}

	if result.DeletedCount == 0 {
		return nil, grpc.Errorf(codes.NotFound, "post not found")
	}

	return &pb.DeletePostResponse{Success: true}, nil
}

func (s *postServer) GetPostById(ctx context.Context, req *pb.GetPostByIdRequest) (*pb.Post, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	filter := bson.M{"id": req.Id, "userid": req.UserId}

	var post pb.Post
	if err := s.collection.FindOne(ctx, filter).Decode(&post); err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, grpc.Errorf(codes.NotFound, "post not found")
		}
		return nil, grpc.Errorf(codes.Internal, "failed to get post: %v", err)
	}

	return &post, nil
}

func (s *postServer) ListPosts(ctx context.Context, req *pb.ListPostsRequest) (*pb.ListPostsResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	skip := int64((req.GetPage() - 1) * req.GetLimit())
	limit := int64(req.GetLimit())

	filter := bson.M{"userid": req.GetUserId()}

	totalCount, err := s.collection.CountDocuments(ctx, filter)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to count posts: %v", err)
	}

	cur, err := s.collection.Find(ctx, filter, options.Find().SetSkip(skip).SetLimit(limit))
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to list posts: %v", err)
	}
	defer cur.Close(ctx)

	var posts []*pb.Post
	for cur.Next(ctx) {
		var post pb.Post
		if err := cur.Decode(&post); err != nil {
			return nil, status.Errorf(codes.Internal, "failed to decode post: %v", err)
		}
		posts = append(posts, &post)
	}

	if err := cur.Err(); err != nil {
		return nil, status.Errorf(codes.Internal, "failed to iterate posts: %v", err)
	}

	return &pb.ListPostsResponse{
		Posts:      posts,
		TotalCount: totalCount,
	}, nil
}

func main() {
	// Connect to db

	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://posts_db:27017"))
	if err != nil {
		grpclog.Fatalf("failed to create MongoDB client: %v", err)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 7*time.Second)
	defer cancel()
	err = client.Connect(ctx)
	if err != nil {
		grpclog.Fatalf("failed to connect to MongoDB: %v", err)
	}
	defer client.Disconnect(ctx)

	collection := client.Database("postsdb").Collection("posts")

	// Listen connections

	listener, err := net.Listen("tcp", ":5300")
	if err != nil {
		grpclog.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterPostServiceServer(s, &postServer{client: client, collection: collection})

	grpclog.Printf("server listening at %v", listener.Addr())
	if err := s.Serve(listener); err != nil {
		grpclog.Fatalf("failed to serve: %v", err)
	}
}
