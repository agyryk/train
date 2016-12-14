
class CommuncationProtocol(object):

    DB_AGENT_RESPONSE_TIMEOUT = 120

    AGENT_STATUS_IDLE = 301
    AGENT_STATUS_ERROR = 302
    AGENT_STATUS_DOWNLOADING = 303

    SERVER_ASKS_START = 103
    SERVER_ASKS_STOP = 104


class CommunicationObject():
    def __init__(self):
        protocol = CommuncationProtocol
        self.agent_status = protocol.AGENT_STATUS_IDLE
        self.agent_progress = 0
        self.server_asks = ""
