import time
import random
import threading

import requests

endpoints = ('add?a=12&b=23', 'substract?a=112&b=23', 'division?a=46&b=23', 'random', 'readiness', 'liveness')


def run():
    while True:
        try:
            target = random.choice(endpoints)
            requests.get("http://calc-application:5000/%s" % target, timeout=1)

        except:
            pass


if __name__ == '__main__':
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.setDaemon(True)
        thread.start()

    while True:
        time.sleep(1)
