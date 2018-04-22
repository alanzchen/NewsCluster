import sys
import grpc

from protos import NewsCluster_pb2_grpc

from tests import testPingPong

if __name__ == '__main__':
    uri = sys.argv[-1] + ':50051'
    channel = grpc.insecure_channel(uri)
    stub = NewsCluster_pb2_grpc.NewsServiceStub(channel)
    testPingPong(stub)
