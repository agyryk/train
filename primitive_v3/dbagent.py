from couchbase import bucket
from communication import CommunicationObject
import time

class DBAgent(object):

    def __init__(self):
        self.docs_to_parse = 1000
        self.connection_settings = None
        self.tagging_settings = None
        self.download_progress = 0

    def run(self, data, communication_object, indexer):
        self.connection_settings = ConnectionSettings(data)
        self.tagging_settings = ParsingRules(data)
        if not self._connect():
            communication_object.agent_status = CommunicationObject.AGENT_STATUS_ERROR
            communication_object.message = "Failed to connect to CB server \n"
            return

        counter = 0
        communication_object.agent_status = CommunicationObject.AGENT_STATUS_CONNECTED

        for i in range(0, self.docs_to_parse+1):
            download_progress = (counter * 100 / self.docs_to_parse)

            communication_object.agent_status = CommunicationObject.AGENT_STATUS_WORKING
            communication_object.agent_progress = {"indexed documents":counter,
                                                   "progress":"{}%".format(download_progress)}
            counter += 1

            key = str(i)
            doc = self.cb.get(key).value
            for rule in self.tagging_settings.rules:
                if rule.source in doc:
                    if rule.filter == "*":
                        indexer.add_instance(rule.name, doc[rule.source], key)
                    elif "include(" in rule.filter:
                        term = rule.filter.split("include(")[1]
                        term = term.split(")")[0]
                        all_terms = list()
                        all_terms = term.split(",")
                        found = True
                        for t in all_terms:
                            if t not in doc[rule.name]:
                                found = False
                                break
                        if found:
                            indexer.add_instance(rule.name, rule.value, key)
                    elif "range(" in rule.filter:
                        val = rule.filter.split("range(")[1]
                        val = val.split(")")[0]
                        if ">=" in val:
                            val = val.split(">=")[1]
                            if doc[rule.name] >= int(val):
                                indexer.add_instance(rule.name, rule.value, key)
                        elif "<=" in val:
                            val = val.split("<=")[1]
                            if doc[rule.name] <= int(val):
                                indexer.add_instance(rule.name, rule.value, key)
                        elif ">" in val:
                            val = val.split(">")[1]
                            if doc[rule.name] > int(val):
                                indexer.add_instance(rule.name, rule.value, key)
                        elif "<" in val:
                            val = val.split("<")[1]
                            if doc[rule.name] < int(val):
                                indexer.add_instance(rule.name, rule.value, key)

        communication_object.agent_status = CommunicationObject.AGENT_STATUS_CONNECTED

    def _connect(self):
        try:
            connection_string = "couchbase://{}/{}".format(self.connection_settings.sever,
                                                           self.connection_settings.bucket)
            self.cb = bucket.Bucket(connection_string, password=self.connection_settings.password)
            return True
        except Exception as e:
            pass
        return False


class ConnectionSettings():
    def __init__(self, body):
        self.sever = body["server"]["name"]
        self.bucket = body["server"]["bucket"]
        self.port = body["server"]["port"]
        self.password = body["server"]["password"]


class ParsingRules():
    def __init__(self, body):
        self.rules = []
        for rule in body["rules"]:
            self.rules.append(ParsingRule(rule))


class ParsingRule():
    def __init__(self, rule):
        self.name = rule["name"]
        self.source = rule["source"]
        self.filter = rule["filter"]
        self.value = rule["value"]

'''
curl -i -H "Content-Type: application/json" -XPOST  http://localhost:5000/api/run -d '{"server": {"name":"localhost", "bucket":"train", "port":"8091", "password":"password"},"rules":[{"name": "city", "source":"city", "value":"*", "filter":"*"},{"name":"position", "source": "position", "value":"any java positions", "filter":"include(java)"},{"name":"position", "source": "position", "value":"any developer position", "filter":"include(developer)"},{"name":"position", "source": "position", "value":"only java developers", "filter":"include(java, developer)"},{"name":"position", "source": "position", "value":"all qa", "filter":"include(qa)"}, {"name":"salary", "source": "salary", "value":"below 150K", "filter":"range(<150)"},{"name":"salary", "source": "salary", "value":"above 150K", "filter":"range(>=150)"},{"name": "experience", "source":"experience", "value":"*", "filter":"*"}]}'



{
"server": {"name":"localhost", "bucket":"train", "port":"8091", "password":"password"}},
"rules":[
            {"name": "city", "source":"city", "value":"*", "filter":"*"},
            {"name":"position", "source": "position", "value":"any java positions", "filter":"include(java)"},
            {"name":"position", "source": "position", "value":"any developer position", "filter":"include(developer)"},
            {"name":"position", "source": "position", "value":"only java developers", "filter":"include(java, developer)"},
            {"name":"position", "source": "position", "value":"all qa", "filter":"include(qa)"},
            {"name":"salary", "source": "salary", "value":"below 150K", "filter":"range(<150)"},
            {"name":"salary", "source": "salary", "value":"above 150K", "filter":"range(>150)"},
            {"name": "experience", "source":"experience", "value":"*", "filter":"*"}
         ]
}



'''