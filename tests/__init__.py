from __future__ import print_function

import grpc

from protos import NewsCluster_pb2, NewsCluster_pb2_grpc

def testNews(stub):
    response = stub.CreateNewsIfNotExists(NewsCluster_pb2.CreateNewsRequest(id=0))
    assert response.created == True
    response = stub.CreateNewsIfNotExists(NewsCluster_pb2.CreateNewsRequest(id=0))
    assert response.created == False


def testDocument(stub):
    pass


def run(uri: str):
    channel = grpc.insecure_channel(uri)
    stub = NewsCluster_pb2_grpc.NewsServiceStub(channel)
    testNews(stub)
    testDocument(stub)
