from URL import URL
from Tag import Tag
from Text import Text
from Layout import Layout

import tkinter
import tkinter.font

SCROLL_STEP = 20

class Browser:
    def __init__(self):
        self.width, self.height = 800, 600
        self.entities = {"lt": "<", "gt": ">"}
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.handle_mousewheel)
        self.window.bind("<Configure>", self.resize)

    def resize(self, e):
        self.canvas.pack(fill=tkinter.BOTH, expand=1)
        self.width, self.height = e.width, e.height
        self.display_list = Layout(self.tokens).display_list
        self.draw()

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        bottom = self.display_list[-1][1]
        self.scroll = min(bottom - self.height, self.scroll)
        self.draw()

    def scrollup(self, e):
        self.scroll -= SCROLL_STEP
        self.scroll = max(self.scroll, 0)
        self.draw()

    def handle_mousewheel(self, e):
        self.scroll += e.delta
        bottom = self.display_list[-1][1]
        if e.delta < 0:
            self.scroll = max(self.scroll, 0)
        else:
            self.scroll = min(self.scroll, bottom - self.height)
        self.draw()

    def lex(self, body):
        out = []
        buffer = ""
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
                        out.append(Text(entity))
                        break
                if entity in self.entities:
                    out.append(Text(self.entities[entity]))
            elif char == "<":
                in_tag = True
                if buffer: out.append(Text(buffer))
                buffer = ""
            elif char == ">":
                in_tag = False
                out.append(Tag(buffer))
                buffer = ""
            else:
                buffer += char
            idx += 1

        if not in_tag and buffer:
            out.append(Text(buffer))

        return out

    def load(self, url):
        body = url.request()
        self.tokens = self.lex(body)
        self.display_list = Layout(self.tokens).display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if len(self.display_list) > 0:
            for i, (x, y, c, font) in enumerate(self.display_list):
                if y > self.height + self.scroll:
                    continue
                if y < self.scroll:
                    continue
                self.canvas.create_text(x, y - self.scroll, text=c, anchor="nw", font=font)

            if self.display_list[-1][1] > self.height:
                self.draw_scrollbar()

    def draw_scrollbar(self):
        bottom = self.display_list[-1][1]
        self.canvas.create_rectangle(
            self.width - 10,
            0,
            self.width,
            self.display_list[-1][1],
            width=10,
            outline="blue"
        )

        self.canvas.create_rectangle(
            self.width - 10,
            ((self.scroll) / bottom) * self.height,
            self.width,
            ((self.scroll + self.height) / bottom) * self.height,
            width = 10,
            outline="black"
        )

if __name__ == "__main__":
    import sys

    browser = Browser()
    try:
        browser.load(URL(sys.argv[1]))
    except E:
        browser.load(URL())
    tkinter.mainloop()
