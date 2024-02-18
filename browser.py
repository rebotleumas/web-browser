from URL import URL

class Browser:
	def __init__(self):
		pass

	def show(self, body):
		in_tag = False
		for c in body:
			if c == "<":
				in_tag = True
			elif c == ">":
				in_tag = False
			elif not in_tag:
				print(c, end="")

	def load(self, url):
		body = url.request()
		self.show(body)

if __name__ == "__main__":
	browser = Browser()
	browser.load(URL())