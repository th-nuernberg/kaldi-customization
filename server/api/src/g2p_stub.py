import redis
import time
import json
redis_conn = redis.Redis(host='localhost', port=6380, password='kalditproject')

while True:
    data = redis_conn.blpop('G2P-Queue', 1)
    print(data)
    '''
    time.sleep(5)

    redis_conn.publish('Status-Queue', json.dumps({
    "type": "g2p",
    "text": "filename",
    "status": 200,
    "msg": "Success"
    }))
    '''