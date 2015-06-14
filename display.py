#!/usr/bin/python
# Example using a character LCD plate.
import math
import time

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins 
# lcd = LCD.Adafruit_CharLCDPlate()

# create some custom characters
# lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
# lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
# lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
# lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
# lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
# lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
# lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])

# Show some basic colors.




class Line(object):
    """Handles line representation for LCD character display of display_length."""
    def __init__(self, s="", display_length=16):
        self.display_length = display_length
        self.length = 0
        self.line = ""
        self.cur_pos = 0
        self.is_scrolling = False
        self.set_line(s)
        self.deliminator = "   ***   "
        

    def set_line(self, s):
        """If length of s is larger than display length '   ***   ' is added and is_scolling is set to True."""
        if len(s) > self.display_length:
            self.is_scrolling = True
            self.length = len(s) + len(self.deliminator)
        else:
            self.is_scrolling = False
        self.cur_pos = 0
        self.line = s

    def step(self, n=1):
        """Steps the line by n (default 1) characters."""
        if self.is_scrolling:
            self.cur_pos += n
            if self.cur_pos >= self.length:
                self.cur_pos = 0

    def current_view(self):
        if self.is_scrolling:
            s = self.line + self.deliminator + self.line
            return s[self.cur_pos:(self.cur_pos + self.display_length)]
        else:
            return self.line
        

class Display(LCD.Adafruit_CharLCDPlate):
    """This is a docstring."""
    def __init__ (self):
        super(Display, self).__init__()

        self.color = (0, 0, 0)
        self.top_line = Line()
        self.bottom_line = Line()

    def message(self, t, b):
        """Update top_line to t and bottom_line to b."""
        self.top_line.set_line(t)
        self.bottom_line.set_line(b)   
        self.clear()
        super(Display, self).message("{}\n{}".format(self.top_line.current_view(), self.bottom_line.current_view()))

    def set_color(self, c):
        """Set background color. c = (R, G, B)"""
        super(Display, self).set_color(c[0], c[1], c[2])

    def set_top_line(self, t):
        """Update only top_line"""
        self.message(t, self.bottom_line.line)

    def set_bottom_line(self, b):
        """Update only bottom_line"""
        self.message(self.top_line.line, b)

    def scroll(self):
        self.top_line.step()
        self.bottom_line.step()
        self.set_cursor(0, 0)
        super(Display, self).message("{}\n{}".format(self.top_line.current_view(), self.bottom_line.current_view()))
        

       
if __name__ == "__main__":
    d = Display()
    
    d.message("Hallo Welt alles Klatosdfghj", "Welt machs gut ich bin weg")



    for i in range(100):
        time.sleep(0.2)
        d.scroll()

    
