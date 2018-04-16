from concurrent import futures
import grpc
import time

from protos import NewsCluster_pb2
from protos import NewsCluster_pb2_grpc

from NewsCluster import NewsCluster

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# app = Flask(__name__)
# api = Api(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

# NEWS_list = {i.rstrip('.json').lstrip('static/'): NewsCluster(id=i.rstrip('.json'), data=json.load(open(i, 'r')))
#              for i in glob.glob('static/*.json')}

# import models

# db.create_all()

# def get_new_id():
#     new_id = 0
#     for key in NEWS_list.keys():
#         if int(key) > new_id:
#             new_id = int(key)
#     new_id += 1
#     return new_id

# def abort_if_doesnt_exist(news_id):
#     if news_id not in NEWS_list:
#         abort(404, message="{} doesn't exist".format(news_id))

# class News(Resource):
#     def get(self, news_id):
#         """

#         :param news_id: the ID of the news cluster.
#         :return: a JSON representation of the news cluster.
#         """
#         user = models.News.query.filter_by(username=username).first_or_404()
#         abort_if_doesnt_exist(str(news_id))
#         return jsonify(NEWS_list[str(news_id)].data)

#     def delete(self, news_id):
#         abort_if_doesnt_exist(str(news_id))
#         del NEWS_list[str(news_id)]
#         return '', 204

#     def put(self, news_id):
#         """
#         Do the prediction.
#         :param news_id: the ID of the news cluster.
#         :return: the representation of the score.
#         """
#         abort_if_doesnt_exist(str(news_id))
#         parser = reqparse.RequestParser()
#         parser.add_argument('content', type=str, help='Content of the unseen news')
#         args = parser.parse_args()
#         n = NEWS_list[news_id]
#         result = n.predict(args['content'])
#         return result, 201

#     def post(self, news_id):
#         """
#         Add a new document to a single news inside a news cluster.
#         :param news_id: the id of the news cluster
#         :return: None
#         """
#         abort_if_doesnt_exist(str(news_id))
#         parser = reqparse.RequestParser()
#         parser.add_argument('content', type=str, help='Content of the news')
#         parser.add_argument('title', type=str, help='Title of the news')
#         args = parser.parse_args()
#         n = NEWS_list[str(news_id)]
#         n.add_document(args['title'], args['content'])
#         return args['title'] + ' added to ' + str(news_id), 201

# # TodoList
# # shows a list of all NewsClusters, and lets you POST to add new NewsClusters
# class NewsList(Resource):
#     def get(self):
#         return {
#             k: v.data['title'] for k, v in NEWS_list.items()
#         }

#     def post(self):
#         """
#         Create a news cluster.
#         :return: the assigned ID of the news
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('title', type=str, help='Title of the news')
#         args = parser.parse_args()
#         id_ = get_new_id()
#         n = NewsCluster(id_, title=args['title'])
#         NEWS_list[str(id_)] = n
#         return str(id_), 201

#     def put(self):
#         """
#         Find the best matching news given a new document.
#         :return: an ordered list of suggestions.
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('content', type=str, help='Content of the unseen news')
#         args = parser.parse_args()
#         result = sorted([{'id': k, 'score': v.predict(args['content']), 'title': v.data['title']} for k, v in NEWS_list.items()],
#                         key=lambda s: s['score'], reverse=True)
#         return result, 200

# api.add_resource(NewsList, '/news')
# api.add_resource(News, '/news/<string:news_id>', endpoint='news')

class Service(NewsCluster_pb2_grpc.NewsServiceServicer):

    def CreateNews(self, request, context):
        return NewsCluster_pb2.Result()


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
