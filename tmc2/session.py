__author__ = 'tpuctah'

import socket
import gevent
import gevent.queue

_SOCKET = None
_INPUT = gevent.queue.Queue()
_OUTPUT = gevent.queue.Queue()
_INPUT_STRING = gevent.queue.Queue()

def connect():
    global _SOCKET
    if _SOCKET:
        _SOCKET.close()
    _SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _SOCKET.setblocking(True)
    print 'connect'
    _SOCKET.connect(('arda.pp.ru', 4000))


def telnet():
    while True:
        try:
            data = _SOCKET.recv(4096)
            if data:
                _INPUT.put(data)
            else:
                print 'disconnected'
                connect()
        except socket.error as msg:
            print msg
            gevent.sleep(5)
            connect()


def _input_worker():
    while True:
        string = _INPUT.get()
        #if string.endswith('\n\r'):
        for s in string.split('\n\r'):
            _INPUT_STRING.put(s)
        gevent.sleep(0)


def _output_worker():
    while True:
        print '+send'
        string = _OUTPUT.get()
        _SOCKET.send(string)
        print '-send'
        gevent.sleep(0)


def send(string):
    _OUTPUT.put(string)


def get():
    return _INPUT_STRING.get()


connect()
telnet = gevent.spawn(telnet)
input_worker_task = gevent.spawn(_input_worker)
output_worker_task = gevent.spawn(_output_worker)


#telnet.join()