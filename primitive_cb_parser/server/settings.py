from optparse import OptionParser


def get_options():
    usage = '%prog -s servername -b bucketname'
    parser = OptionParser(usage)
    parser.add_option('-s', dest='cb_server_name', help='Couchbase server name')
    parser.add_option('-p', dest='cb_server_port', help='Couchbase server port')
    parser.add_option('-b', dest='cb_bucket_name', help='Couchbase server bucket name')
    options, args = parser.parse_args()

    if not options.cb_server_name or not options.cb_bucket_name:
        parser.error('Missing mandatory parameter')
    return options


class ParserSettings(object):

    CB_PORT = "8091"

    def __init__(self):
        options = get_options()
        self.cb_server = options.cb_server_name
        self.cb_bucket_name = options.cb_bucket_name
        self.cb_port = options.cb_server_port or self.CB_PORT
