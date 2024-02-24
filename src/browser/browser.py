from URL import URL
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 20
NEW_LINE = 20

class Browser:
    def __init__(self):
        self.entities = {"lt": "<", "gt": ">"}
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def scrolldown(self, e):
    	self.scroll += SCROLL_STEP
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
        text = self.lex(body)
        self.display_list = self.layout(text)
        self.draw()

    def draw(self):
    	self.canvas.delete("all")
    	for x, y, c in self.display_list:
    	    if y - self.scroll > HEIGHT: continue
    	    if y < VSTEP - self.scroll: continue
    	    self.canvas.create_text(x, y - self.scroll, text=c)

    def layout(self, text):
        cursor_x, cursor_y = HSTEP, VSTEP
        display_list = []
        for char in text:
            display_list.append((cursor_x, cursor_y, char))
            
            cursor_x += HSTEP
            if char == '\n':
                cursor_x = HSTEP
                cursor_y += NEW_LINE

            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

        return display_list


if __name__ == "__main__":
    import sys
    browser = Browser()
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()
