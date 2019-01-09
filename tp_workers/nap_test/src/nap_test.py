import mzbench
import urllib2
import time
#import paho.mqtt.client as mqtt
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
    try:
        start_time = time.time()
        response = urllib2.urlopen(host)

        if 200 is int(response.code):
            mzbench.notify(('success_requests', 'counter'), 1)
        else:
            print "{0}".format(response.code)
            mzbench.notify(('failed_requests', 'counter'), 1)

        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))
        response.close()
    except Exception as error:
        mzbench.notify(('failed_requests', 'counter'), 1)
        print "{0}".format(str(error))


def nap_load(host, proxy):
    #client = mqtt.Client("P1") #create new instance
    #client.connect("iot.eclipse.org") #connect to broker
    #client.publish("house/main-light","OFF")#publish

    processor = Process(target=processors, args=[host])
    processor.start()
    processor.join()
