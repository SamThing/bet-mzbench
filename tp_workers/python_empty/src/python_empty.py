import mzbench
import random
import urllib2
import socket
import socks
import time
from multiprocessing import Process

def initial_state():
    pass


def metrics():
    return [
        [
            ('success_requests', 'counter'),
            ('failed_requests', 'counter')
        ],
        ('request_time', 'histogram')
    ]

def my_print(msg):
    mzbench.notify(('success_requests', 'counter'), 1)
    mzbench.notify(('failed_requests', 'counter'), 2)

    print "{0}".format(msg)

mzbench.notify(('request_time', 'histogram'), random.uniform(0, 1000000000)/7)