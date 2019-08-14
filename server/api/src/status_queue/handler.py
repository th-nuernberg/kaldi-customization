import json
import threading
import traceback

from .data_prep import handle_data_prep_status
from .text_prep import handle_text_prep_status
from config import redis_client
from redis_config import redis_queues


queue_handler = dict(
    data_prep=handle_data_prep_status,
    text_prep=handle_text_prep_status,
)


def handle_statue_queue(status_queue, app, db):
    '''
    Listens to STATUS_QUEUE and handle the messages.
    '''
    with app.app_context():
        status_queue_pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
        status_queue_pubsub.subscribe(status_queue)
        print("[Status] Listen to {}".format(status_queue))

        for message in status_queue_pubsub.listen():
            try:
                print("[Status] New pubsub message: " + str(message))
                if 'data' not in message:
                    print('Invalid message, missing key data')
                    continue

                data = json.loads(message['data'])

                if '__queue__' not in data:
                    print('Invalid message, missing key __queue__ in data')
                    continue

                db_session = db.create_scoped_session()
                queue_handler[data['__queue__']](data, db_session)
            except Exception as e:
                print("[Status] Exception at status queue: {}".format(type(e).__name__))
                print("[Status] Further information 2: " + str(e))
                traceback.print_exc()


def start_status_queue_handler(app, db):
    thread = threading.Thread(target=handle_statue_queue, name="Redis-Handler", args=(redis_queues["STATUS_QUEUE"], app, db))
    thread.start()

    return thread
