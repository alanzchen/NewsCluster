

main:
	python3 -m grpc_tools.protoc -I./v2land-grpc --python_out=. --grpc_python_out=. ./v2land-grpc/protos/*.proto

