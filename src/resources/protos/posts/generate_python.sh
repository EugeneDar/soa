mkdir -p ../../../services/users/app/api/posts
/opt/homebrew/bin/python3.11 -m grpc_tools.protoc -I. --python_out=../../../services/users/app/api/posts --grpc_python_out=../../../services/users/app/api/posts posts.proto

# use this if ModuleNotFoundError
# from . import posts_pb2 as posts__pb2
