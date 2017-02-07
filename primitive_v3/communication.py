

class CommunicationObject():

    AGENT_STATUS_IDLE = 0
    AGENT_STATUS_CONNECTED = 1
    AGENT_STATUS_ERROR = 2
    AGENT_STATUS_WORKING = 3

    def __init__(self):
        self.agent_status = self.AGENT_STATUS_IDLE
        self.agent_progress = {}
        self.message = {}