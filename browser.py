from URL import URL

class Browser:
	def __init__(self):
		self.entities = {"lt": "<", "gt": ">"}

	def show(self, body):
		in_tag = False
		idx = 0
		while idx < len(body):
			char = body[idx]

			if char == "&":
				entity = ""
				idx += 1
				while body[idx] != ";":
					entity += body[idx]
					idx += 1
				assert entity in self.entities
				print(self.entities[entity], end="")
			elif char == "<":
				in_tag = True
			elif char == ">":
				in_tag = False
			elif not in_tag:
				print(char, end="")
			idx += 1

	def load(self, url):
		body = url.request()
		self.show(body)

if __name__ == "__main__":
	browser = Browser()
	browser.load(URL("data:text/html, <div>Hello&lt;div&gt; world</div>"))