import mzbench
import urllib2
import socket
import socks
import time
import paho.mqtt.client as mqtt
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

def nap_processors(host, user, password, topic):
    start_time = time.time()
    try:
        client = mqtt.Client("P1") #create new instance
        client.username_pw_set(user, password)
        
        client.connect(host) #connect to broker

        client.publish(topic,"OFF")#publish
        mzbench.notify(('success_requests', 'counter'), 1)
        
        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))
        client.close()
    except Exception as error:
        mzbench.notify(('failed_requests', 'counter'), 1)
        print "Timeout: {0}".format(str(error))


def socks_processors(host):
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


def socks_load(host, proxy):
    #socks.set_default_proxy(socks.SOCKS5, "127.0.0.1")
    socks.set_default_proxy(socks.SOCKS5, proxy)
    socket.socket = socks.socksocket

    process = Process(target=socks_processors, args=[host])
    process.start()
    process.join()


def nap_load(host, user, password, topic):
    nap_processors(host, user, password, topic)
    #process = Process(target=nap_processors, args=[host, user, password, topic])
    #process.start()
    #process.join()
