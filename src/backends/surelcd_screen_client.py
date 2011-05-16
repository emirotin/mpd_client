'''
Created on May 15, 2011

@author: eugenemirotin
'''
from base_screen_client import BaseScreenClient
import serial

class SureLcdScreenClient(BaseScreenClient):
    '''
    PyCurses screen backend
    '''

    def __init__(self, device, width, height):
        '''
        Constructor
        '''        
        super(SureLcdScreenClient, self).__init__(width, height)
        self.ser = serial.Serial(device, 9600)
                                            
    def write_line(self, row, line):
        row += 1
        self.ser.write('\xFE\x47\x01{0}{1}'.format(chr(row), line))  
        
    def exit(self):
        self.ser.close()
        super(SureLcdScreenClient, self).exit()      
