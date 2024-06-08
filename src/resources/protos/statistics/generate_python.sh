mkdir -p ../../../services/users/app/api/statistics
/opt/homebrew/bin/python3.11 -m grpc_tools.protoc -I. --python_out=../../../services/users/app/api/statistics --grpc_python_out=../../../services/users/app/api/statistics statistics.proto

# use this if ModuleNotFoundError
# from . import statistics_pb2 as statistics__pb2


mkdir -p ../../../services/statistics/app/api/statistics
/opt/homebrew/bin/python3.11 -m grpc_tools.protoc -I. --python_out=../../../services/statistics/app/api/statistics --grpc_python_out=../../../services/statistics/app/api/statistics statistics.proto

# use this if ModuleNotFoundError
# from . import statistics_pb2 as statistics__pb2
