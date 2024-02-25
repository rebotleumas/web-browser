from URL import URL
import tkinter

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 20
NEW_LINE = 20

class Browser:
    def __init__(self):
        self.width, self.height = 800, 600
        self.entities = {"lt": "<", "gt": ">"}
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width,
            height=self.height
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.handle_mousewheel)
        self.window.bind("<Configure>", self.resize)

    def resize(self, e):
    	self.canvas.pack(fill=tkinter.BOTH, expand=1)
    	self.width, self.height = e.width, e.height
    	self.display_list = self.layout(self.text)
    	self.draw()

    def scrolldown(self, e):
    	self.scroll += SCROLL_STEP
    	self.draw()

    def scrollup(self, e):
    	self.scroll -= SCROLL_STEP
    	self.scroll = max(self.scroll, 0)
    	self.draw()

    def handle_mousewheel(self, e):
    	self.scroll += e.delta
    	self.scroll = max(self.scroll, 0)
    	self.draw()

    def lex(self, body):
        text = ""
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
                    if idx >= len(body): 
                    	text += entity
                    	break
                if entity in self.entities:
                    text += self.entities[entity]
            elif char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                text += char
            idx += 1

        return text

    def load(self, url):
        body = url.request()
        self.text = self.lex(body)
        self.display_list = self.layout(self.text)
        self.draw()

    def draw(self):
    	self.canvas.delete("all")
    	for x, y, c in self.display_list:
    	    if y - self.scroll > self.height: continue
    	    if y < VSTEP - self.scroll: continue
    	    self.canvas.create_text(x, y - self.scroll , text=c)

    def layout(self, text):
        cursor_x, cursor_y = HSTEP, VSTEP
        display_list = []
        for char in text:
            display_list.append((cursor_x, cursor_y, char))
            
            cursor_x += HSTEP
            if char == '\n':
                cursor_x = HSTEP
                cursor_y += NEW_LINE

            if cursor_x >= self.width - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

        return display_list


if __name__ == "__main__":
    import sys
    browser = Browser()
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()
