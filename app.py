from concurrent import futures
from functools import partial
import grpc
import time
import datetime
import json

from protos import NewsCluster_pb2
from protos import NewsCluster_pb2_grpc

from models import create_all, get_session, News, Document
from utils import default_error
from NewsCluster import extractContentToDatabase

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Service(NewsCluster_pb2_grpc.NewsServiceServicer):

    def __createResult(self, value):
        return NewsCluster_pb2.CreateResult(created=value)

    def PingPong(self, request, context):
        return NewsCluster_pb2.Pong(
            message=request.message,
            serverTime=str(datetime.datetime.now())
        )

    def CreateNewsIfNotExists(self, request, context):
        with default_error(context):
            with get_session() as session:
                count = session.query(News)\
                    .filter(News.id == request.id).count()
                if count == 0:
                    session.add(News(id=request.id))
                    return self.__createResult(True)
                else:
                    return self.__createResult(False)

    def AddDocumentIfNotExists(self, request, context):
        with default_error(context):
            with get_session() as session:
                count = session.query(Document)\
                    .filter(Document.id == request.id).count()
                if count == 0:
                    session.add(
                        Document(
                            id=request.id,
                            url=request.url,
                            news_id=request.newsId
                        ))
                    context.add_callback(
                        partial(
                            extractContentToDatabase,
                            request.newsId,
                            request.url
                        )
                    )
                    return self.__createResult(True)
                else:
                    return self.__createResult(False)

    def GetDocumentById(self, request, context):
        with default_error(context):
            with get_session() as session:
                result = session.query(Document)\
                    .filter(Document.id == request.id)
                for doc in result:
                    return NewsCluster_pb2.Document(
                        id = doc.id,
                        title = doc.title,
                        url = doc.url,
                        mercuryData = json.dumps(doc.mercury_data),
                        newsId = doc.news_id
                    )
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Document is not found')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    NewsCluster_pb2_grpc.add_NewsServiceServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    create_all()
    serve()
