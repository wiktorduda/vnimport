import urllib
import urllib2
import os
import json
import tempfile
import uuid
import time
import threading

rate = 1.0
per_second = 5.0

def rate_limit(rate, per_second, **kwargs):
    now_func = kwargs.get('now_func', time.time)
    sleep_func = kwargs.get('sleep_func', time.sleep)
    lock = threading.Lock()
    rate = float(rate)
    per_second = float(per_second)
    if rate < 1.0:
        rate = 1.0 / rate
        per_second = per_second * (rate * rate)
    def decorate(func):
        last_check = [now_func()]
        allowance = [rate]
        def rate_limit_func(*args,**kwargs):
            lock.acquire()
            now_epoch = now_func()
            elapsed = now_epoch - last_check[0]
            last_check[0] = now_epoch
            allowance[0] += elapsed * (rate / per_second)
            if allowance[0] > rate:
                allowance[0] = rate
            if allowance[0] < 1.0:
                sleep_time = (1.0 - allowance[0]) * (per_second / rate)
                sleep_func(sleep_time)
            allowance[0] -= 1.0
            lock.release()
            return func(*args,**kwargs)
        return rate_limit_func
    return decorate

@rate_limit(rate, per_second)
def search_erogetrailers(keyword):
    payload = {
        'md': 'search_game',
        'sw': keyword.encode('utf-8')
    }
    url_payload = urllib.urlencode(payload)
    url = 'http://erogetrailers.com/api?{}'
    r = urllib2.urlopen(url.format(url_payload))
    return json.loads(r.read().decode('utf-8'))

@rate_limit(rate, per_second)
def dowload_getchu_cover_image(getchu_id):
    return DownloadGetchuCoverImage(getchu_id)

class DownloadGetchuCoverImage:
    def __init__(self, getchu_id):
        self.getchu_id = getchu_id

    def __enter__(self):
        id = str(uuid.uuid4())
        filename = os.path.join(tempfile.gettempdir(), '{}.jpg'.format(id))
        url = 'http://www.getchu.com/brandnew/{0}/rc{0}package.jpg'
        with open(filename, 'wb') as f:
            f.write(urllib2.urlopen(url.format(self.getchu_id)).read())
        self.filename = filename
        return (id, filename)

    def __exit__(self, type, value, traceback):
        os.remove(self.filename)