#go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
#go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
export PATH="$PATH:$(go env GOPATH)/bin"

#protoc -I . --go_out=. reverse.proto --go-grpc_out=.
protoc --go_out=../../../services/posts/app/api --go-grpc_out=../../../services/posts/app/api posts.proto