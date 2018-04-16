PYTHON = python3

main: create-all create-proto
	$(PYTHON) app.py

create-all:
	$(PYTHON) createTable.py

create-proto:
	$(PYTHON) -m grpc_tools.protoc -I./v2land-grpc --python_out=. --grpc_python_out=. ./v2land-grpc/protos/*.proto
