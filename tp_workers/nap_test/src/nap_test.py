import mzbench
import urllib2
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


def processors(client):
    start_time = time.time()

    try:
        client.publish("pos/cwb","") #publish

        mzbench.notify(('success_requests', 'counter'), 1)

    except Exception as error:
        print "{0}".format(str(error))
        mzbench.notify(('failed_requests', 'counter'), 1)

        mzbench.notify(('request_time', 'histogram'), (time.time() - start_time))



def nap_load(host):
    #broker_address="iot.eclipse.org" #use external broker
    client = mqtt.Client("P1") #create new instance
    client.connect(host) #connect to broker

    processor = Process(target=processors, args=[client])
    processor.start()
    processor.join()
