import socket
import ssl

class URL:
	def __init__(self, url): 
		self.scheme, url = url.split("://", 1)
		assert self.scheme in ["http", "https", "file"]
		if "/" not in url:
			url = url + "/"

		self.host, url = url.split("/", 1)
		self.path = "/" + url if self.scheme != "file" else url

		if self.scheme == "http":
			self.port = 80
		elif self.scheme == "https":
			self.port = 443

		if ":" in self.host: 
			self.host, port = self.host.split(":", 1)
			self.port = int(port)

	def __init__(self):
		self.scheme = "file"
		self.path = "C:/Users/samue/Documents/Projects/WebBrowser/test_file.txt"

	def request(self) -> str:
		body = ''
		if self.scheme == "file":
			print(f"Reading file {self.path}")
			try:
				with open(self.path) as f: body = f.read()
			except (FileNotFoundError, IOError):
				return 'Incorrect file or non-existent file path!'

		else:
			request_headers = {'Host': self.host, 'Connection': 'close', 'User-Agent': 'Bowser'}
			request = f"GET {self.path} HTTP/1.0\r\n"
			for header, header_value in request_headers.items():
				request += f"{header}: {header_value}\r\n"
			request += "\r\n\r\n"

			s = socket.socket(
				family=socket.AF_INET,
				type=socket.SOCK_STREAM,
				proto=socket.IPPROTO_TCP,
			)
			if self.scheme == 'https':
				ctx = ssl.create_default_context()
				s = ctx.wrap_socket(s, server_hostname=self.host)
			s.connect((self.host, self.port))
			s.send(request.encode('utf8'))

			response = s.makefile("r", encoding="utf8", newline="\r\n")
			statusline = response.readline()
			version, status, explanation = statusline.split(" ", 2)
			response_headers = {}
			body = response.read()

			while True:
				line = response.readline()
				if line == "\r\n" or line == "": break
				header, value = line.split(":", 1)
				response_headers[header.casefold()] = value.strip()

				assert "transfer-encoding" not in response_headers
				assert "content-encoding" not in response_headers

				s.close()

		return body