class Selector(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.top = self.y - self.height
        self.left = self.x - self.width
        self.right = self.x + self.width
        self.bottom = self.y + self.height

    def __eq__(self, other):
        return (isinstance(other, Selector) and (self.x == other.x) and self.y == other.y and self.color == other.color)

    def __repr__(self):
        return 'Selector %d %d %s' % (self.x, self.y, self.color)


    # def __repr__(self):
    #     return 'Selector %d %d %d %d' % (self.x, self.y, self.width, self.height)

class TextBox(Selector): # round the corners for buttons
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color)
        self.top = self.y - self.height
        self.left = self.x - self.width
        self.right = self.x + self.width
        self.bottom = self.y + self.height
        self.text = text
        self.type = 'textBox'
        self.fontSize = '14'

    def draw(self, canvas, xOffset=0):
        width = (self.right - self.left) / 2
        height = (self.bottom - self.top) / 2
        canvas.create_polygon((self.left + xOffset, self.top), (self.right + xOffset, self.top), (self.right + xOffset, self.bottom),(self.left + xOffset, self.bottom), fill=self.color, outline = 'black', width=2)
        # canvas.create_polygon((self.left + xOffset, self.top), (self.left + width/8 + xOffset, self.top, self.left + xOffset, self.top + height/5), fill='black', outline='black', width=2)
        canvas.create_text(self.x + xOffset, self.y, text = self.text, font = 'Helvetica ' + self.fontSize)
        # canvas.create_text(cx, cy, text = self.text, anchor=anchor)

class Buttonn(TextBox):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        self.type = 'button'
        self.linkedTo = None

    def draw(self, canvas, xOffset=0):
        shadowOffset = 4

        canvas.create_polygon((self.left + shadowOffset + xOffset, self.top + 8+ shadowOffset), (self.left + 1 + shadowOffset + xOffset, self.top + 4.5+ shadowOffset), (self.left + 2 + shadowOffset + xOffset, self.top + 3+ shadowOffset), (self.left + 4.5 + shadowOffset + xOffset, self.top + 1+ shadowOffset), (self.left + 8 + shadowOffset + xOffset, self.top+ shadowOffset),
            (self.right - 8 + shadowOffset + xOffset, self.top), (self.right - 5 + shadowOffset + xOffset, self.top + 1), (self.right - 2 + shadowOffset + xOffset, self.top + 3), (self.right - 1 + shadowOffset + xOffset, self.top + 4.5), (self.right + shadowOffset + xOffset, self.top + 8+ shadowOffset), 
            (self.right + shadowOffset + xOffset, self.bottom - 8+ shadowOffset),(self.right - 1 + shadowOffset + xOffset, self.bottom - 4.5+ shadowOffset),(self.right - 2 + shadowOffset + xOffset, self.bottom - 3+ shadowOffset),(self.right - 4 + shadowOffset + xOffset, self.bottom - 1+ shadowOffset),(self.right - 8 + shadowOffset + xOffset, self.bottom+ shadowOffset),
            (self.left + 8 + shadowOffset + xOffset, self.bottom+ shadowOffset), (self.left + 4.5 + shadowOffset + xOffset, self.bottom - 1+ shadowOffset), (self.left + 2 + shadowOffset + xOffset, self.bottom - 3+ shadowOffset), (self.left + 1 + shadowOffset + xOffset, self.bottom - 4+ shadowOffset), (self.left + shadowOffset + xOffset, self.bottom - 8+ shadowOffset),
            fill='light grey',)
        canvas.create_polygon((self.left + xOffset, self.top + 8), (self.left + 1 + xOffset, self.top + 4.5), (self.left + 2 + xOffset, self.top + 3), (self.left + 4.5 + xOffset, self.top + 1), (self.left + 8 + xOffset, self.top),
            (self.right - 8 + xOffset, self.top), (self.right - 5 + xOffset, self.top + 1), (self.right - 2 + xOffset, self.top + 3), (self.right - 1 + xOffset, self.top + 4.5), (self.right + xOffset, self.top + 8), 
            (self.right + xOffset, self.bottom - 8),(self.right - 1 + xOffset, self.bottom - 4.5),(self.right - 2 + xOffset, self.bottom - 3),(self.right - 4 + xOffset, self.bottom - 1),(self.right - 8 + xOffset, self.bottom),
            (self.left + 8 + xOffset, self.bottom), (self.left + 4.5 + xOffset, self.bottom - 1), (self.left + 2 + xOffset, self.bottom - 3), (self.left + 1 + xOffset, self.bottom - 4), (self.left + xOffset, self.bottom - 8),
            fill=self.color, outline = 'black', width = 2)

        canvas.create_text(self.x + xOffset, self.y, text = self.text)

class Slider(Selector):
    def __init__(self, x, y, width, height, color, radius):
        super().__init__(x, y, width, height, color)
        self.r = radius
        self.type = 'slider'
        self.cx = self.x # have centers for circle independent of the rectangle
        self.cy = self.y
        self.slidColor = 'gray18'

    def draw(self, canvas, xOffset=0):
        shadowOffset = 2.75
        canvas.create_polygon((self.left + xOffset, self.top + 3.5), (self.left + xOffset, self.top + 1.75), (self.left + 0.5 + xOffset, self.top + 0.75), (self.left + 1.75 + xOffset, self.top), (self.left + 3.5 + xOffset, self.top),
            (self.right - 3.5 + xOffset, self.top), (self.right - 2 + xOffset, self.top), (self.right - 0.5 + xOffset, self.top + 1), (self.right + xOffset, self.top + 1.75), (self.right + xOffset, self.top + 3.5), 
            (self.right + xOffset, self.bottom - 3.5),(self.right + xOffset, self.bottom - 1.75),(self.right - 0.5 + xOffset, self.bottom - 1),(self.right - 1.5 + xOffset, self.bottom),(self.right - 3.5 + xOffset, self.bottom),
            (self.left + 3.5 + xOffset, self.bottom), (self.left + 1.75 + xOffset, self.bottom ), (self.left + 0.5 + xOffset, self.bottom - 1), (self.left + xOffset, self.bottom - 1.5), (self.left + xOffset, self.bottom - 3.5),
            fill='white', outline = 'black', width = 2)
        canvas.create_polygon((self.left + xOffset, self.top + 3.5), (self.left + xOffset, self.top + 1.75), (self.left + 0.5 + xOffset, self.top + 0.75), (self.left + 1.75 + xOffset, self.top), (self.left + 3.5 + xOffset, self.top),
            (self.cx - 3.5 + xOffset, self.top), (self.cx - 2 + xOffset, self.top), (self.cx - 0.5 + xOffset, self.top + 1), (self.cx + xOffset, self.top + 1.75), (self.cx + xOffset, self.top + 3.5), 
            (self.cx + xOffset, self.bottom - 3.5),(self.cx + xOffset, self.bottom - 1.75),(self.cx - 0.5 + xOffset, self.bottom - 1),(self.cx - 1.5 + xOffset, self.bottom),(self.cx - 3.5 + xOffset, self.bottom),
            (self.left + 3.5 + xOffset, self.bottom), (self.left + 1.75 + xOffset, self.bottom ), (self.left + 0.5 + xOffset, self.bottom - 1), (self.left + xOffset, self.bottom - 1.5), (self.left + xOffset, self.bottom - 3.5),
            fill=self.slidColor, outline = 'black', width = 2)
        canvas.create_oval(self.cx - self.r + xOffset, self.cy - self.r+ shadowOffset, self.cx + self.r + xOffset, self.cy + self.r+ shadowOffset, fill='light grey', width=0)

        canvas.create_oval(self.cx - self.r + xOffset, self.cy - self.r, self.cx + self.r + xOffset, self.cy + self.r, fill=self.color, width=2)

class DropDown(TextBox):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        self.type = 'dropdown'
        self.opened = False
        self.text = text
        self.shownText = text

    def draw(self, canvas, xOffset=0):
        canvas.create_polygon((self.left + xOffset, self.top + 8), (self.left + 1 + xOffset, self.top + 4.5), (self.left + 2  + xOffset, self.top + 3), (self.left + 4.5  + xOffset, self.top + 1), (self.left + 8  + xOffset, self.top),
                    (self.right - 8  + xOffset, self.top), (self.right - 5  + xOffset, self.top + 1), (self.right - 2  + xOffset, self.top + 3), (self.right - 1  + xOffset, self.top + 4.5), (self.right  + xOffset, self.top + 8), 
                    (self.right  + xOffset, self.bottom - 8),(self.right - 1 + xOffset, self.bottom - 4.5),(self.right - 2  + xOffset, self.bottom - 3),(self.right - 4  + xOffset, self.bottom - 1),(self.right - 8  + xOffset, self.bottom),
                    (self.left + 8 + xOffset, self.bottom), (self.left + 4.5 + xOffset, self.bottom - 1), (self.left + 2  + xOffset, self.bottom - 3), (self.left + 1  + xOffset, self.bottom - 4), (self.left  + xOffset, self.bottom - 8),
                    fill=self.color,width=2, outline='black')
        canvas.create_line(self.right - 20 + xOffset, self.top, self.right + xOffset - 20, self.bottom, width = 2)
        canvas.create_polygon(self.right + xOffset - 17, self.top + 12, self.right + xOffset - 3, self.top + 12, self.right + xOffset - 10, self.bottom - 8, fill=self.color, outline='black', width=1.5)
        p = (self.right - 20 + self.left) / 2
        canvas.create_text(p + xOffset, self.y, text=self.shownText)

class AnimatedBox(Selector): 
    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height, fill=self.color, width=2)
