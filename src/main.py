'''
Created on May 15, 2011

@author: eugenemirotin
'''

import sys, traceback
import signal
from settings import *

def print1(screen_client):
    screen_client.show_line(1, '123')
KEYS_MAPPING = {
            27: 'exit',
            32: print1
}

    
def main():    
    screen_client = None
    input_client = None

    def cleanup():
        input_client and input_client.exit()
        screen_client and screen_client.exit() or screen_client.__class__.cleanup()

    if screen_mode == 'curses':
        from backends.pycurses_screen_client import CursesScreenClient as ScreenClient
        screen_params = [screen_width, screen_height]        
    elif screen_mode == 'sure':
        from backends.surelcd_screen_client import SureLcdScreenClient as ScreenClient
        screen_params = [screen_device, screen_width, screen_height]
    else:
        print 'Unknown screen mode {0}'.format(screen_mode)
        sys.exit(1)    
    try:        
        screen_client = ScreenClient(*screen_params)
    except:
        cleanup()        
        traceback.print_exc()    
        sys.exit(1)
   
    if input_mode == 'curses':
        from backends.pycurses_input_client import CursesInputClient as InputClient
        input_params = [screen_client, KEYS_MAPPING]
    else:
        print 'Unknown input mode {0}'.format(input_mode)
        sys.exit(1)    
    try:
        input_client = InputClient(*input_params)
    except:
        cleanup()
        traceback.print_exc()
        sys.exit(1)
    
    input_client.listen(cleanup)

if __name__ == '__main__':
    main()
    