from URL import URL

class TestUrl:
	def test_http(self):
		url = URL("http://example.org")
		assert url.scheme == "http"
		assert url.path == "/"
		assert url.host == "example.org"
		assert url.port == 80

	def test_https(self):
		url = URL("https://example.org")
		assert url.scheme == "https"
		assert url.path == "/"
		assert url.host == "example.org"
		assert url.port == 443

	def test_file(self):
		url = URL("file://C:/Users/samue/Documents/Projects/WebBrowser/test_file.txt")
		assert url.path == "C:/Users/samue/Documents/Projects/WebBrowser/test_file.txt"
		assert url.scheme == "file"

	def test_data(self):
		url = URL("data:text/html,<div>Hello world!</div>")
		assert url.scheme == "data"
		assert url.mediatype == "text/html"
		assert url.html_data == "<div>Hello world!</div>"

	def test_viewsource(self):
		url = URL("view-source:http://example.org")
		assert url.scheme == "view-source"
		assert url.path == "/"
		assert url.host == "example.org"
		assert url.port == 80