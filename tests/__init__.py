from __future__ import print_function

import grpc
import time

from protos import NewsCluster_pb2, NewsCluster_pb2_grpc

def testNews(stub):
    response = stub.CreateNewsIfNotExists(NewsCluster_pb2.CreateNewsRequest(id=0))
    assert response.created == True
    response = stub.CreateNewsIfNotExists(NewsCluster_pb2.CreateNewsRequest(id=0))
    assert response.created == False


def testDocument(stub):
    response = stub.AddDocumentIfNotExists(
        NewsCluster_pb2.AddDocumentRequest(
            id = 0,
            url = 'http://www.kanfanews.com/pc/index/article/1005035',
            news_id = 0
        )
    )
    assert response.created == True
    flag = False
    for i in range(0, 5):
        doc = stub.GetDocumentById(
            NewsCluster_pb2.GetDocumentByIdRequest(id=0)
        )
        if (doc.mercury_data != None):
            flag = True
            break
        print(str(i) + " failed, retrying...")
        time.sleep(1)
    if not flag:
        raise Exception("Fetch mercury api failed")


def run(uri: str):
    channel = grpc.insecure_channel(uri)
    stub = NewsCluster_pb2_grpc.NewsServiceStub(channel)
    testNews(stub)
    testDocument(stub)
