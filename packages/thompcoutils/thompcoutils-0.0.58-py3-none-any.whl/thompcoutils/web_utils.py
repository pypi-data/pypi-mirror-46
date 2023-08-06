from thompcoutils.log_utils import get_logger
import urllib.request
import json
import ssl
import pprint
from werkzeug.exceptions import BadRequestKeyError


class MissingArgumentException(Exception):
    pass


class Server:
    @staticmethod
    def get_info(args, request):
        if args is None:
            args = []
        values = {}
        for arg in args:
            found = False
            values[arg] = request.form.getlist(arg)
            if len(request.form.to_dict()) > 0:
                try:
                    values[arg] = request.form.getlist(arg)
                    if len(values[arg]) == 1:
                        values[arg] = values[arg][0]
                    found = True
                except BadRequestKeyError:
                    pass
            elif len(request.args) > 0:
                try:
                    values[arg] = str(request.args[arg])
                    found = True
                except BadRequestKeyError:
                    pass
            if not found:
                raise MissingArgumentException("argument '{}' not passed in".format(arg))
        return values


class Client:
    def __init__(self, host, port, page_root="", crt_file=None):
        logger = get_logger()
        self.host = host
        self.application_page = page_root
        self.port = port
        self.crt_file = crt_file
        logger.debug("host:{}, port:{}".format(host, port))
        if self.crt_file:
            http = "https"
        else:
            http = "http"
        if page_root is None:
            page_root = ""
        self.url = '{}://{}:{}/{}'.format(http, host, port, page_root)

    def send_curl(self, command, values):
        logger = get_logger()
        url = "{}/{}".format(self.url, command)
        logger.debug("Accessing URL: {}".format(url))
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        json_data = json.dumps(values)
        json_data_bytes = json_data.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(json_data_bytes))

        if self.crt_file:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.load_verify_locations(self.crt_file)
            rtn = urllib.request.urlopen(req, json_data_bytes, context=context)
        else:
            rtn = urllib.request.urlopen(req, json_data_bytes)
        data = json.load(rtn)
        return data, rtn


def main():
    data = {"username": "ttttt",
            "password": "ttttt"}
    web_comms = Client(host="localhost", port=8082, page_root="licenseServer/app")
    data, rtn = web_comms.send_curl(command="status", values=data)
    message = "Success" if rtn.code == 200 else "Failed"
    pp = pprint.PrettyPrinter()
    print("{}:{}".format(message, rtn.code))
    pp.pprint(data)


if __name__ == '__main__':
    main()
