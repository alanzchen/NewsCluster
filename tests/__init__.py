from __future__ import print_function

import grpc

from protos import NewsCluster_pb2, NewsCluster_pb2_grpc

def run(uri: str):
    channel = grpc.insecure_channel(uri)
    stub = NewsCluster_pb2_grpc.NewsServiceStub(channel)
    response = stub.CreateNews(NewsCluster_pb2.CreateNewsRequest(id=0))
    print("Greeter client received: " + str(response.type))
