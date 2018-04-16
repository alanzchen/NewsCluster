

main:
	python3 -m grpc_tools.protoc -I./v2land-grpc/protos --python_out=./protos --grpc_python_out=. ./v2land-grpc/protos/NewsCluster.proto

