python3 -m grpc_tools.protoc -I. --python_out=./centralnode --grpc_python_out=./centralnode ./proto/av.proto
python3 -m grpc_tools.protoc -I. --python_out=./centralnode --grpc_python_out=./centralnode ./proto/centralnode.proto
