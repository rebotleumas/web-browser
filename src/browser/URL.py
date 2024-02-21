import socket
import ssl

class URL:
	def __init__(self, url="file://C:/Users/samue/Documents/Projects/WebBrowser/test_file.txt"): 
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
		body = ''
		if self.scheme == "file":
			try:
				with open(self.path) as f: body = f.read()
			except (FileNotFoundError, IOError):
				return 'Incorrect file or non-existent file path!'
		elif self.scheme == "data":
			body = self.html_data
		else:
			request_headers = {'Host': self.host, 'User-Agent': 'Bowser'}
			request = f"GET {self.path} HTTP/1.0\r\n"
			for header, header_value in request_headers.items():
				request += f"{header}: {header_value}\r\n"
			request += "\r\n\r\n"

			if (self.host + str(self.port)) in self.socket_cache:
				s = self.socket_cache[self.host + str(self.port)]
			else:
				s = socket.socket(
					family=socket.AF_INET,
					type=socket.SOCK_STREAM,
					proto=socket.IPPROTO_TCP,
				)
				if self.scheme == 'https':
					ctx = ssl.create_default_context()
					s = ctx.wrap_socket(s, server_hostname=self.host)

				s.connect((self.host, self.port))
				self.socket_cache[self.host + str(self.port)] = s
			s.send(request.encode('utf8'))

			response = s.makefile("r", encoding="utf8", newline="\r\n")
			statusline = response.readline()
			version, status, explanation = statusline.split(" ", 2)
			response_headers = {}

			while True:
				line = response.readline()
				if line == "\r\n": break
				header, value = line.split(":", 1)
				response_headers[header.casefold()] = value.strip()

				assert "transfer-encoding" not in response_headers
				assert "content-encoding" not in response_headers

				s.close()
			content_length = int(response_headers['content-length'])

			body = response.read()
			if self.scheme == "view-source":
				body.replace("<", "&lt;")
				body.replace(">", "&gt;")

		return body[:content_length]