import mzbench
import urllib2
import socket
import socks
import time
import requests
import json
import numpy as np
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from multiprocessing import Process

def get_random_id():
    return np.random.randint(2147483647, 9223372036854775807, size=1, dtype=np.int64)[0]

def initial_state():
    pass

def metrics():
    return [
        [
            ('success_requests', 'counter'),
            ('failed_requests', 'counter'),
            ('exception_requests', 'counter')
        ],
        ('request_time', 'histogram')
    ]

def nap_processors(host, user, password, topic):
    start_time = time.time()

    try:
        publish.single(topic, "payload", hostname=host, auth={'username': user, 'password': password})
        mzbench.notify(('success_requests', 'counter'), 1)
        
        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))
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


def rest_processors(host, headers):
    start_time = time.time()
    item = { #UPDATE ANTIGO
          "antenna": get_random_id(),
          "manufacturer": "SAMSUNG",
          "model": "J7MOCK",
          "product": "SMART",
          "device": "J7MOCK",
          "hardware": "LALALA",
          "brand": "SAMSUNG",
          "display": "DUNO",
          "host": "DUNO",
          "board": "GREAT",
          "sdk_version": "1.2.8-fake",
          "android_sdk_version": 19
    }

    item = { #UPDATE NOVO
        "id": get_random_id(),
        "tpsdk": "10.0.1",
        "asdk": 24
    }

    try:
        item = json.dumps(item, encoding='utf8')

        r = requests.post(host, data=item, headers=headers, timeout=5)

        if r.status_code not in (200, 201):
            print "Failed {0}".format(r.status_code)
            mzbench.notify(('failed_requests', 'counter'), 1)
        else:
            mzbench.notify(('success_requests', 'counter'), 1)

        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))
    except Exception as error:
        mzbench.notify(('exception_requests', 'counter'), 1)
        print "Timeout: {0}".format(str(error))


def rest_load(host, authorization_token):
    headers = { 
        'Content-Type': 'application/json',
        'x-api-key': authorization_token
    }
    
    process = Process(target=rest_processors, args=[host, headers])
    process.start()
    process.join()


def socks_load(host, proxy):
    #socks.set_default_proxy(socks.SOCKS5, "127.0.0.1")
    socks.set_default_proxy(socks.SOCKS5, proxy)
    socket.socket = socks.socksocket

    process = Process(target=socks_processors, args=[host])
    process.start()
    process.join()


def nap_load(host, user, password, topic):
    #nap_processors(host, user, password, topic)
    process = Process(target=nap_processors, args=[host, user, password, topic])
    process.start()
    process.join()
