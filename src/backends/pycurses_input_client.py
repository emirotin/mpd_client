'''
Created on May 16, 2011

@author: eugenemirotin
'''

import threading
import signal
import sys


class CursesInputClient(object):
    '''
    Curses Keyboard Listener
    '''

    def __init__(self, screen_client, keys_mapping):
        '''
        Constructor
        '''
        self.screen_client = screen_client
        self.keys_mapping = keys_mapping
        self.listener = threading.Thread(target=self.listener_target)
        self.condition = threading.Condition()
        self.halt = False
        self.cleanup_callback = None
            
    def listener_target(self):        
        while True:
            self.condition.acquire()
            if not self.halt:
                res = self.handle_key()
                self.condition.release()
                if res == False:
                    self.cleanup_callback()
                    break
            else:
                self.condition.release()
                break
            
    def handle_key(self):
        key = self.screen_client.read_char(True)        
        if not key in self.keys_mapping:
            return
        if self.keys_mapping[key] == 'exit':
            return False
        self.keys_mapping[key](self.screen_client)
        return True
    
    def listen(self, cleanup_callback):
        self.cleanup_callback = cleanup_callback
        self.listener.start()
    
    def exit(self):
        self.halt = True
        if self.listener != threading.current_thread() and self.listener.is_alive():
            self.listener.join()
