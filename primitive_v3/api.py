from multiprocessing import Queue
from threading import Thread
from dbagent import DBAgent
from settings import ParserSettings
from communication import CommunicationObject
from indexer import Indexer

class RestApiEngine(object):
    def __init__(self):
        self.dbagent = DBAgent()
        self.dbagent_thread = None
        self.communication_object = CommunicationObject()
        self.indexer = Indexer()

    def run(self, data):
        if self.dbagent_thread is None:
            self.dbagent_thread = Thread(target=self.dbagent.run, args=(data,
                                                                        self.communication_object,
                                                                        self.indexer))
            self.dbagent_thread.daemon = True
            self.dbagent_thread.start()

    def get_status(self):
            if self.communication_object.agent_status == CommunicationObject.AGENT_STATUS_ERROR:
                return "DB agent internal error: {} \n".format(self.communication_object.message)
            elif self.communication_object.agent_status == CommunicationObject.AGENT_STATUS_IDLE:
                return "Idle \n"
            elif self.communication_object.agent_status == CommunicationObject.AGENT_STATUS_CONNECTED:
                return "Connected".format(self.communication_object.agent_progress)
            elif self.communication_object.agent_status == CommunicationObject.AGENT_STATUS_WORKING:
                return "Parsing now:  {} \n".format(self.communication_object.agent_progress)
            else:
                return "Unexpected status from DB Agent \n"

    def get_index_stats(self):
        r = {"Index size":self.indexer.total_records}
        return "{}\n".format(str(r))

    def query(self, body):
        q = body["type"]
        if q == "all_tags":
            return "{}\n".format(str(self.indexer.get_all_tags()))
        elif q == "values_by_tag":
            return "{}\n".format(str(self.indexer.get_values_by_tag(body["tag"])))
        elif q == "ids_by_tag_and_value":
            return "{}\n".format(str(self.indexer.get_docids_by_tag_and_value(body["tag"], body["value"])))
        elif q == "tags_by_id":
            return "{}\n".format(str(self.indexer.get_tags_by_docid(body["id"])))
        elif q == "value_by_id_and_tag":
            return "{}\n".format(str(self.indexer.get_values_by_docid_and_tag(body["tag"], body["id"])))
        return ""

    def ping(self):
        return "pong! \n"

    '''
    get_all_tags
    get_values_by_tag
    get_docids_by_tag_and_value
    get_tags_by_docid
    get_values_by_docid_and_tag

    curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/query -d '

    {"type":"all_tags"}
    {"type":"values_by_tag", "tag":"city:}
    {"type":"ids_by_tag_and_value", "tag":"city", "value":"Chicago"}
    {"type":"tags_by_id", "id":"13"}
    {"type":"value_by_id_and_tag", "tag":"city", "id":"23"}


    '''
