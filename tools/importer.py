import couchbase
from couchbase.bucket import  Bucket
import json

class Importer(object):

    CONN_STR = 'couchbase://10.0.0.175/train_data_1'

    def __init__(self):
        self.bucket = object
        self.all_docs = list()

    def connect(self):
        try:
            self.bucket = Bucket(self.CONN_STR)
        except:
            print "connection error"
            return False
        return True

    def run(self):
        if self.connect():
            doc_id = 0;
            with open("data.txt", "r") as lines:
                for line in lines:
                    doc = json.loads(line)
                    doc["category"] = doc["category"].split("-")[0]
                    self.bucket.upsert(str(doc_id), doc)
                    doc_id += 1

ex = Importer()
ex.run()

