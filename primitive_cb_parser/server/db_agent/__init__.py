from couchbase import bucket
from ..communication import CommunicationObject, CommuncationProtocol
import time


class DB_Agent(object):

    def __init__(self):
        self.msg_queue = None

    def run(self, msg_q):
        self.msg_queue = msg_q
        counter = 0
        msg_obj = CommunicationObject()
        print "DBAgent started \n"
        while True:
            time.sleep(1)
            counter +=1
            try:
                msg_obj = self.msg_queue.get(False)
            except Exception as e:
                pass
            msg_obj.agent_progress = counter
            self.msg_queue.put(msg_obj)
