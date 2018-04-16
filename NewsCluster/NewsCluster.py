import jieba.analyse
import numpy as np
import json
import os

class NewsCluster:
    def __init__(self, id:int, title:str=None, data:dict=None):
        """
        A class that maintains the news cluster.
        :param title: a friendly title.
        :param data: A single dict containing all the data.
        """
        if not data:
            self.data = {
                'id': str(id),
                'title': title,
                'docs': [],
                'state': {
                    'words': [],
                    'terms_frequency': [],
                }
            }
        else:
            self.data = data
        self.save()

    def set_title(self, title:str):
        """
        Set the title of this news cluster.
        :param title: the title of this news cluster
        :return: None
        """
        self.data['title'] = title

    def set_id(self, id):
        self.data['id'] = str(id)

    def add_document(self, doc_title:str, content:str):
        """
        Add a new document (news) to this news cluster.
        :param doc_title: The title of this document
        :param content: The content of this document
        :return: None
        """
        new_doc = {
            'title': doc_title,
            'content': content
        }
        # TODO: add entity recognition
        doc_words = jieba.analyse.textrank(doc_title + ' ' + content, topK=50, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        self.data['docs'].append(new_doc)
        self.data['state']['words'] = list(set(self.data['state']['words'] + doc_words))
        self.gen_tf()
        self.save()

    def gen_tf(self):
        """
        (Re-)generate the terms frequency array.
        :return: None
        """
        self.data['state']['terms_frequency'] = [sum([d['content'].count(w)/len(d['content'])
                                                      for d in self.data['docs']])
                                                 for w in self.data['state']['words']]

    def predict(self, new_doc:str) -> float:
        """
        Predict the score of matching given a string.
        :param new_doc: the string representation of the un-seen document.
        :return: score of matching.
        """
        doc_tf = np.array([new_doc.count(w) / len(new_doc) for w in self.data['state']['words']])
        return sum(np.array(self.data['state']['terms_frequency']) * doc_tf.transpose()) * 10 ** 4

    def save(self):
        """
        Save this instance to a json file.
        :return: None
        """
        with open(os.path.join('static', self.data['id'] + '.json'), 'w') as f:
            json.dump(self.data, f)