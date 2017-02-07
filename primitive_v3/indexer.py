class Indexer(object):
    def __init__(self):
        self.tags = {}   # direct index
        self.docids = {} # inverted index
        self.total_records = 0

    def add_instance(self, name, value, docid):
        print "Indexer got new record: {}:{}:{}".format(name, value, docid)
        self.total_records += 1
        if name not in self.tags:
            self.tags[name] = {}
        if value not in self.tags[name]:
            self.tags[name][value] = set()
        self.tags[name][value].add(docid)

        if docid not  in self.docids:
            self.docids[docid] = {}
        if name not in self.docids[docid]:
            self.docids[docid][name] = set();
        self.docids[docid][name].add(value)


    def get_all_tags(self):
        print self.tags.keys()
        return self.tags.keys()

    def get_values_by_tag(self, name):
        if name in self.tags:
            return self.tags[name].keys()
        else:
            return None

    def get_docids_by_tag_and_value(self,name, value):
        if name in self.tags and value in self.tags[name]:
            return self.tags[name][value]

    def get_tags_by_docid(self, docid):
        return self.docids[docid].keys()

    def get_values_by_docid_and_tag(self, name, docid):
        if docid in self.docids and name in self.docids[name]:
            return self.docids[docid][name]
        else:
            return None
