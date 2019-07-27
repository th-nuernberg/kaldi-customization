import json
import threading

from .text_prep import handle_text_prep_status
from config import redis_client
from redis_config import redis_queues

def handle_statue_queue(status_queue, app, db):
    '''
    Listens to STATUS_QUEUE and handle the messages.
    '''
    db_session = db.create_scoped_session()
    with app.app_context():
        status_queue_pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
        status_queue_pubsub.subscribe(status_queue)
        print("[Status] Listen to {}".format(status_queue))

        for message in status_queue_pubsub.listen():
            try:
                print("[Status] New pubsub message: " + str(message))
                if message['type'] == 'message':
                    try:
                        msg_data = json.loads(message['data'])
                    except ValueError as e:
                        print("[Status] Error at processing message: " + str(e))
                        continue
                    
                    if msg_data and "type" in msg_data and "text" in msg_data and "status" in msg_data:
                        if msg_data['type'] == 'text-prep':
                            print("[Status] handle text prep status...")
                            handle_text_prep_status(msg_data, db_session)
                            print("[Status] ...handled text prep status")
                        else:
                            print("[Status] unknown type \"{}\" in status queue!".format(msg_data['type']))
            except Exception as e:
                print("[Status] Exception at status queue: {}".format(type(e).__name__))
                print("[Status] Further information 1: " + e.__str__())
                print("[Status] Further information 2: " + str(e))


def start_status_queue_handler(app, db):
    thread = threading.Thread(target=handle_statue_queue, name="Redis-Handler", args=(redis_queues["STATUS_QUEUE"], app, db))
    thread.start()

    return thread
