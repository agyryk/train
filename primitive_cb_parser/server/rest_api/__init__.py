from multiprocessing import Queue
from threading import Thread
from ..communication import CommunicationObject, CommuncationProtocol


class RestApiEngine(object):

    msg_queue = Queue()
    protocol = CommuncationProtocol()

    def __init__(self, dbagent):
        self.dbagent = dbagent
        self.dbagent_thread = Thread(target=dbagent.run, args=(self.msg_queue,))
        self.dbagent_thread.daemon = True

    def ping_parser_server(self):
        return "pong\n"

    def start_dbagent(self):
        self.dbagent_thread.start()

    def dbagent_get_progress(self):
        response = ""
        try:
            msg_obj = self.msg_queue.get(block=True,timeout=self.protocol.DB_AGENT_RESPONSE_TIMEOUT)
            response = "{}% completed \n".format(msg_obj.agent_progress)
        except Exception as e:
            return "Error connecting DB Agent \n"
        return response




