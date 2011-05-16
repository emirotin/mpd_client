'''
Created on May 15, 2011

@author: eugenemirotin
'''

import threading

class BaseScreenClient(object):
    '''
    Base Screen Client
    '''

    def __init__(self, width, height):
        '''
        Constructor
        '''
        self.rotators = {}      
        self.width = width
        self.height = height
        
    def clear_line(self, row):
        self.write_line(row, '')
    
    def clear_screen(self):
        for i in range(self.height):
            self.clear_line(i)
        
    def rotate_lines(self, row, lines, interval):
        self.stop_rotation(row)
        if not isinstance(lines, (list, tuple)):
            lines = (lines,)
        norm_lines = []
        for line in lines:
            if len(line) < self.width:
                line += ' ' * (self.width - len(line))
            elif len(line) > self.width:
                line = line[:self.width]
            norm_lines.append(line)
        def inner(func, i, client):
            if not client.rotators.get(row, None):
                return
            client.write_line(row, norm_lines[i])
            i = (i + 1) % len(lines)
            timer = threading.Timer(interval, func, [func, i, client])
            self.rotators[row] = timer
            timer.start()        
        self.rotators[row] = True
        inner(inner, 0, self)
        
    def marquee_line(self, row, line, interval):
        if len(line) <= self.width:
            self.write_line(row, line)
            return
        lines = [(line[i:] + ' ' + line)[:self.width]
                 for i in range(len(line))]
        self.rotate_lines(row, lines, interval)
        
    
    def stop_rotation(self, row):
        timer = self.rotators.get(row, None)
        if timer:
            timer.cancel()
            del self.rotators[row]  
        
    def stop_all_rotations(self):        
        for i in range(self.height):
            self.stop_rotation(i)
        
    def exit(self):
        self.stop_all_rotations()
        self.clear_screen()
        self.__class__.cleanup()
        
    @staticmethod
    def cleanup():
        pass

    def write_line(self, row, line):
        raise NotImplementedError()
    
    def show_line(self, row, line, marquee_long=True, marquee_interval=1):
        if len(line) < self.width:
            line += ' ' * (self.width - len(line))
        if len(line) > self.width and marquee_long:
            self.marquee_line(row, line, marquee_interval)
        else:
            self.write_line(row, line)

