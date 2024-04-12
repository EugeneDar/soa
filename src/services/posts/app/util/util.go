package util

import (
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	pb "grpc-server/api/posts"
	"math/rand"
	"strings"
)

func GenerateRandomID() string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	const segments = 4
	const segmentLength = 4

	var id strings.Builder
	for i := 0; i < segments; i++ {
		if i > 0 {
			id.WriteString("-")
		}
		for j := 0; j < segmentLength; j++ {
			index := rand.Intn(len(charset))
			id.WriteByte(charset[index])
		}
	}

	return id.String()
}

func CheckOwnerCorrectness(collection *mongo.Collection, postId string, userId int64, ctx context.Context) error {
	filter := bson.M{"id": postId}

	var post pb.Post
	if err := collection.FindOne(ctx, filter).Decode(&post); err != nil {
		if err == mongo.ErrNoDocuments {
			return grpc.Errorf(codes.NotFound, "post not found")
		}
		return grpc.Errorf(codes.Internal, "failed to get post for owner check: %v", err)
	}
	if post.UserId != userId {
		return grpc.Errorf(codes.PermissionDenied, "you are not allowed to access this post")
	}

	return nil
}
