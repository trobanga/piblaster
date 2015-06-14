#!/usr/bin/python
# Example using a character LCD plate.
import math
import time
import threading

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
    def __init__(self, s="", display_length=16, delimiter="   ***   "):
        self.display_length = display_length
        self.length = 0
        self.line = ""
        self.cur_pos = 0
        self.is_scrolling = False
        self.set_line(s)
        self.delimiter = delimiter
        

    def set_line(self, s):
        """If length of s is larger than display length '   ***   ' is added and is_scolling is set to True."""
        if len(s) > self.display_length:
            self.is_scrolling = True
            self.length = len(s) + len(self.delimiter)
            self.line = s
        else:
            self.is_scrolling = False
            self.line = s + (self.display_length - len(s)) * " "
        self.cur_pos = 0

    def step(self, n=1):
        """Steps the line by n (default 1) characters."""
        if self.is_scrolling:
            self.cur_pos += n
            if self.cur_pos >= self.length:
                self.cur_pos = 0

    def current_view(self):
        """Extract substring that fits display starting at cur_pos with length display_length"""
        if self.is_scrolling:
            s = self.line + self.delimiter + self.line
            return s[self.cur_pos:(self.cur_pos + self.display_length)]
        else:
            return self.line
        

class Display(LCD.Adafruit_CharLCDPlate):
    """This is a docstring."""
    def __init__ (self, sleeptime=0.2, display_length=16, delimiter = "   ***   " ):
        super(Display, self).__init__()

        self.top_line = Line(display_length=display_length, delimiter=delimiter)
        self.bottom_line = Line(display_length=display_length, delimiter=delimiter)

        self.sleeptime = sleeptime

        t = threading.Thread(target=self._display_text)
        t.daemon = True
        t.start()


    def set_lines(self, t, b):
        """Update both top and bottom lines"""
        self.top_line.set_line(t)
        self.bottom_line.set_line(b)

    def set_top_line(self, t):
        """Update only top_line"""
        self.top_line.set_line(t)

    def set_bottom_line(self, b):
        """Update only bottom_line"""
        self.bottom_line.set_line(b)


    def _display_text(self):
        while True:
            self.set_cursor(0, 0)
            super(Display, self).message("{}\n{}".format(self.top_line.current_view(), self.bottom_line.current_view()))
            self.top_line.step()
            self.bottom_line.step()
            time.sleep(self.sleeptime)

        

       
if __name__ == "__main__":
    d = Display()
    
    d.set_lines("Hallo Welt alles Klatosdfghj", "Welt machs gut ich bin weg")

