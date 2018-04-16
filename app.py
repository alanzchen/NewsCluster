from concurrent import futures
import grpc
import time
import json

from protos import NewsCluster_pb2
from protos import NewsCluster_pb2_grpc

from models import get_session, News, Document
from utils import default_error

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Service(NewsCluster_pb2_grpc.NewsServiceServicer):

    def __createResult(self, value):
        return NewsCluster_pb2.CreateResult(created=value)

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
                            title=request.title,
                            url=request.url,
                            content=request.content,
                            news_id=request.news_id
                        ))
                    return self.__createResult(True)
                else:
                    return self.__createResult(False)

    def GetDocumentById(self, request, context):
        with default_error(context):
            with get_session() as session:
                result = session.query(Document)\
                    .filter(Document.id == request.id)
                if (len(result) == 0):
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Document is not found')
                else:
                    doc = result[0]
                    return NewsCluster_pb2.Document(
                        id = doc.id,
                        title = doc.title,
                        url = doc.url,
                        mercury_data = json.dumps(doc.mercury_data),
                        news_id = doc.news_id
                    )


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
    serve()
