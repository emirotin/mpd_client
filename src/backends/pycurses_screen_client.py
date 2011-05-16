'''
Created on May 15, 2011

@author: eugenemirotin
'''
import curses
from base_screen_client import BaseScreenClient

class CursesScreenClient(BaseScreenClient):
    '''
    PyCurses screen backend
    '''

    def __init__(self, width, height):
        '''
        Constructor
        '''        
        super(CursesScreenClient, self).__init__(width, height)
                
        self.col_prefix = self.col_postfix = '|'
        self.top_border = '*' + '=' * self.width + '*'
        self.bottom_border = '*' + '=' * self.width + '*'

        self.help = self.help_lines()
        if not isinstance(self.help, (list, tuple)):
            self.help = (self.help, )           
        self.content_row_offset = 1 + len(self.help)
        self.content_col_offset = len(self.col_prefix)        
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        #curses.curs_set(0)
        self.screen.clear()
        self.screen.refresh()

        for i, line in enumerate(self.help):
            self.write_raw_line(i, line)
        
        self.write_raw_line(self.content_row_offset - 1, self.top_border)
        line = ('{}' + ' ' * self.width + '{}').format(self.col_prefix, self.col_postfix)
        for i in range(self.height):
            self.write_raw_line(self.content_row_offset + i, line)
        self.write_raw_line(self.content_row_offset + self.height, self.bottom_border)                
                                    
    def read_char(self, as_int=False):
        c = self.screen.getch()
        if as_int:
            return c
        return chr(c)
    
    def write_char(self, row, col, char):
        self.screen.addch(row, col, char)
        
    def write_raw_line(self, row, line, col_offset=0):
        if len(line) < self.width:
            line += ' ' * (self.width - len(line))
        for i, c in enumerate(line):
            self.write_char(row, col_offset + i, c)
        self.screen.refresh()
            
    def write_line(self, row, line, marquee_long=True):
        row += self.content_row_offset
        self.write_raw_line(row, line, self.content_col_offset)
        
    def help_lines(self):
        return ['Esc: quit']
    
    @staticmethod
    def cleanup():
        curses.nocbreak() 
        curses.echo() 
        curses.endwin()