import redis
redis_conn = redis.Redis(host='localhost', port=6380, password='kalditproject')
pubsub = redis_conn.pubsub()
pubsub.subscribe('Status-Queue')
for msg in pubsub.listen(): print(msg)