from couchbase.bucket import  Bucket
import json


class Extractor(object):

    def __init__(self):
        self.bucket = object
        self.all_docs = list()

    def connect(self):
        try:
            self.bucket = Bucket('couchbase://cbmonitor.sc.couchbase.com/perf_daily')
            docs = self.bucket.n1ql_query("select perf_daily from perf_daily")
            runs = list()
            for row in docs:
                self.all_docs.append(row["perf_daily"])
        except:
            print "connection error"
            return False
        return True

    def run(self):
        if self.connect():
            outfile = open("data.txt", "w")
            for line in self.all_docs:
                outfile.write(json.dumps(line))
                outfile.write('\n')
            outfile.close()

ex = Extractor()
ex.run()
