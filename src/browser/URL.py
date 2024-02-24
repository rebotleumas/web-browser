import socket
import ssl
import time


class URL:
    def __init__(
        self, url="file://C:/Users/samue/Documents/Projects/WebBrowser/test_file.txt"
    ):
        self.scheme, new_url = url.split(":", 1)
        assert self.scheme in ["http", "https", "file", "data", "view-source"]

        if self.scheme in ["http", "https"]:
            self.parse_http(url)

        if self.scheme == "file":
            _, self.path = url.split("://")

        if self.scheme == "data":
            self.mediatype, self.html_data = new_url.split(",", 1)
            assert self.mediatype == "text/html"

        if self.scheme == "view-source":
            self.parse_http(new_url)

        self.socket_cache = {}
        self.response_cache = {}
        self.redirects = 0
        self.MAX_REDIRECTS = 5
        self.cache_max_age = 100

    def parse_http(self, url):
        scheme, url = url.split("://", 1)
        if "/" not in url:
            url = url + "/"

        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if scheme == "http":
            self.port = 80
        elif scheme == "https":
            self.port = 443

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self) -> str:
        body = ""
        if self.scheme == "file":
            try:
                with open(self.path) as f:
                    body = f.read()
            except (FileNotFoundError, IOError):
                return "Incorrect file or non-existent file path!"
        elif self.scheme == "data":
            body = self.html_data
        else:
            request_headers = {
                "Host": self.host,
                "User-Agent": "Bowser",
                "Connection": "Keep-Alive",
                "Keep-Alive": "timeout=1, max=1",
                "Cache-Control": f"max-age: {self.cache_max_age}"
            }
            request = f"GET {self.path} HTTP/1.0\r\n"
            for header, header_value in request_headers.items():
                request += f"{header}: {header_value}\r\n"

            request += "\r\n\r\n"
            request = request.encode("utf8")
            request_hash = hash(request)

            if request_hash in self.response_cache:
            	time_elapsed = time.time() - self.response_cache[request_hash][1]
            	if time_elapsed <= self.cache_max_age:
            		return self.response_cache[request_hash]
            else:
	            if (self.host + str(self.port)) in self.socket_cache:
	                s = self.socket_cache[self.host + str(self.port)]
	            else:
	                s = socket.socket(
	                    family=socket.AF_INET,
	                    type=socket.SOCK_STREAM,
	                    proto=socket.IPPROTO_TCP,
	                )
	                if self.scheme == "https":
	                    ctx = ssl.create_default_context()
	                    s = ctx.wrap_socket(s, server_hostname=self.host)

	                s.connect((self.host, self.port))
	                self.socket_cache[self.host + str(self.port)] = s

	            s.send(request)
	            response = s.makefile("r", encoding="utf8", newline="\r\n")
	            s.close()
	            body = self.parse_response(response, request_hash)

	            return body

    def parse_response(self, response, request_hash):
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers

        if 300 <= int(status) < 400:
            assert "location" in response_headers
            self.redirects += 1
            assert self.redirects <= self.MAX_REDIRECTS
            redirect_url = response_headers["location"]
            self.scheme, _ = redirect_url.split(":", 1)
            self.parse_http(redirect_url)
            return self.request()
        elif int(status) > 400:
        	raise Exception
        else:
            content_length = (
                int(response_headers["content-length"])
                if "content-length" in response_headers
                else -1
            )

            body = response.read(content_length)
            if self.scheme == "view-source":
                body.replace("<", "&lt;")
                body.replace(">", "&gt;")

            self.response_cache[request_hash] = (body, time.time())

            return body
