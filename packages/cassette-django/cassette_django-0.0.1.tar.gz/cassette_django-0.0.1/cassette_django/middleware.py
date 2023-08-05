import fcntl
import os
import re
import urllib
import errno


class CassetteMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not os.getenv("CASSETTE_RECORDING", "0") == "1":
            return self.get_response(request)
        
        bulk_file_path = os.getenv("CASSETTE_BULK_FILE_PATH")
        bulk_file_separator = os.getenv("CASSETTE_BULK_FILE_SEPARATOR")


        request_body = self.parse_request_body(request)
        response = self.get_response(request)
        response_body = self.parse_response_body(response)

        entry = (
            ("request.path", request.path),
            ("request.method", request.method),
            ("request.body", request_body),
            ("response.status", str(response.status_code)),
            ("response.body", response_body),
        )

        list_values = [
            ("request.query", [ f"{k}={v}" for (k,v) in request.GET.items() ]),
            ("request.cookies", [ f"{k}={v}" for (k,v) in request.COOKIES.items() ]),
            ("request.headers", [ f"{self.normalize_header_key(k)}={str(v)}" for (k,v) in request.META.items() if k == "CONTENT_TYPE" or k.startswith("HTTP_") ]),
            ("response.headers", [ f"{self.normalize_header_key(item[0])}={str(item[1])}" for item in list(response.items()) ]),
        ]

        for each in list_values:
            for value in each[1]:
                entry = (*entry, (each[0], value))

        content = urllib.parse.urlencode(entry)
        try:
            with open(bulk_file_path, "a") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(bulk_file_separator)
                f.write('\n')
                f.write(content)
                f.write('\n')
        except OSError as e:
            if (e.errno == errno.ENOENT):
                print("Could not write request blob to file. If this error persists use --bulk=false")

        return response

    def parse_request_body(self, request):
        try:
            return request.body.decode()
        except:
            return request.body

    def parse_response_body(self, response):
        try:
            return response.content.decode()
        except:
            return response.content

    def normalize_header_key(self, key):
        return re.sub('^http-', '', key.lower().replace("_", "-"))
