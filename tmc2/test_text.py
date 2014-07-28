__author__ = 'tpuctah'


import gevent
import gevent.monkey
gevent.monkey.patch_all()

import session
import sys
from gevent.socket import wait_read

from termcolor import colored
import pygame

pygame.init()




#print colored('hello', 'red'), colored('world', 'green')


def tick():
    while True:
        sys.stdout.write('\x1b7')
        sys.stdout.write('\x1b[2A')
        sys.stdout.write('\x1b[100D')
        #sys.stdout.write('\x1b[L')
        sys.stdout.write(colored('hello', 'red') + colored('world', 'green'))
        sys.stdout.write('\n')
        sys.stdout.write('\x1b8')
        sys.stdout.flush()
        gevent.sleep(1)

gevent.spawn(tick)


def input():
    while True:
        wait_read(sys.stdin.fileno())
        input_utf8 = sys.stdin.readline()
        input_unicode = input_utf8.decode('utf-8')
        input_unicode = u'{}\n'.format(input_unicode)
        input_cp1251 = input_unicode.encode('cp1251')
        session.send(input_cp1251)


def get_data_from_session():
    while True:
        line = session.get()
        line = line.decode('cp1251', errors='ignore')
        sys.stdout.write(line+'\n')
        sys.stdout.flush()

gevent.spawn(get_data_from_session)

gevent.spawn(input)


def keyboard():
    while True:
        gevent.sleep(0)
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get(): # User did something
            print 1
            if event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so
                # adjust speed.
                if event.key == pygame.K_LEFT:
                    print 'pygame.K_LEFT'
                elif event.key == pygame.K_RIGHT:
                    print 'pygame.K_RIGHT'
                elif event.key == pygame.K_UP:
                    print 'pygame.K_UP'
                elif event.key == pygame.K_DOWN:
                    print 'pygame.K_DOWN'

gevent.spawn(keyboard)

gevent.sleep(1000)