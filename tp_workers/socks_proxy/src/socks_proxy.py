import mzbench
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

def processors(host):
    start_time = time.time()
    try:
        response = urllib2.urlopen(host)

        if 200 is int(response.code):
            mzbench.notify(('success_requests', 'counter'), 1)
        else:
            print "Failed {0}".format(response.code)
            mzbench.notify(('failed_requests', 'counter'), 1)

        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))
        response.close()
    except Exception as error:
        mzbench.notify(('failed_requests', 'counter'), 1)
        print "Timeout: {0}".format(str(error))


def socks_load(host, proxy, qtd):
    #socks.set_default_proxy(socks.SOCKS5, "127.0.0.1")
    socks.set_default_proxy(socks.SOCKS5, proxy)
    socket.socket = socks.socksocket

    t = []
    for i in range(0, qtd):
        t.append(Process(target=processors, args=[host]))

    for i in t:
        i.start()

    for i in t:
        i.join()
