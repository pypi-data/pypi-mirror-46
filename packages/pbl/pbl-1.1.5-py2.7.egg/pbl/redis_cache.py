import simplejson as json
import redis

r = redis.StrictRedis(host='localhost', port=6380, db=0)
name = 'redis'

def put(type, tid, obj):
    key = get_key(type, tid)
    js = json.dumps(obj)
    r.set(key, js)

def get(type, tid):
    key = get_key(type, tid)
    js = r.get(key)
    if js:
        return json.loads(js)
    else:
        return None

def get_key(type, id):
    return type + '-' + id


if __name__ == '__main__':
    import time

    print 'test', get('test', '1')
    put('test', '1', time.time())
