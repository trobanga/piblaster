#!/usr/bin/python
import math
import time
import threading

import Adafruit_CharLCD as LCD



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
    """Main display class. Initializes Adafruit LCD Display and a thread that controls 
    the content on the display and scrolls individual lines if necessary."""
    def __init__ (self, sleeptime=0.2, display_length=16, delimiter = "   ***   ", debug=False):
        super(Display, self).__init__()

        self.top_line = Line(display_length=display_length, delimiter=delimiter)
        self.bottom_line = Line(display_length=display_length, delimiter=delimiter)

        self.sleeptime = sleeptime
        self.debug = debug

        self.start()
            

    def set_lines(self, t, b):
        """Update both top and bottom lines"""
        self.top_line.set_line(t)
        self.bottom_line.set_line(b)
        if self.debug:
            self._stdout_print()

    def set_top_line(self, t):
        """Update only top_line"""
        self.top_line.set_line(t)
        if self.debug:
            self._stdout_print()

    def set_bottom_line(self, b):
        """Update only bottom_line"""
        self.bottom_line.set_line(b)
        if self.debug:
            self._stdout_print()

    def start(self):
        """Starts the daemon thread that updates the display"""
        self.run = True
        if self.debug:
            self._stdout_print()
        else:
            t = threading.Thread(target=self._display_print)
            t.daemon = True
            t.start()


    def stop(self):
        """Stops the daemon thread that updates the display"""
        self.run = False


    def _display_print(self):
        """Continuously prints to LCD display and scrolls if necessary"""
        while self.run:
            self.set_cursor(0, 0)
            super(Display, self).message("{}\n{}".format(self.top_line.current_view(), self.bottom_line.current_view()))
            self.top_line.step()
            self.bottom_line.step()
            time.sleep(self.sleeptime)
        

    def _stdout_print(self):
        """For debug purposes. Instead of printing to the LCD display, it prints to stdout."""
        maximum_length = 0
        if self.top_line.is_scrolling:
            maximum_length = len(self.top_line.line + self.top_line.delimiter)
        if self.bottom_line.is_scrolling:
            maximum_length = max(maximum_length, len(self.bottom_line.line + self.bottom_line.delimiter))
        steps = 0
        while self.run:
            print(self.top_line.current_view())
            print(self.bottom_line.current_view())
            self.top_line.step()
            self.bottom_line.step()
            steps += 1
            if maximum_length - self.top_line.display_length < steps:
                self.run = False
            time.sleep(self.sleeptime)

        

       
if __name__ == "__main__":
    d = Display()
    
    d.set_lines("Hallo Welt alles Klatosdfghj", "Welt machs gut ich bin weg")

