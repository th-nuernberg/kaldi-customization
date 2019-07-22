import json
import threading

from .text_prep import handle_text_prep_status


def handle_statue_queue(status_queue, db):
    '''
    Listens to STATUS_QUEUE and handle the messages.
    '''

    for message in status_queue.listen():
        try:
            print("Status: new pubsub message:")
            print(message)
            if message['type'] == 'message':
                try:
                    msg_data = json.loads(message['data'])
                except ValueError as e:
                    print(e)
                    continue
                
                if msg_data and "type" in msg_data and "text" in msg_data and "status" in msg_data:
                    if msg_data['type'] == 'text-prep':
                        print("Status: handle text prep status...")
                        handle_text_prep_status(msg_data, db)
                        print("Status: ...handled text prep status")
                    else:
                        print('unknown type in status queue!')
        except Exception as e:
            print("Exception at status queue: {}".format(type(e).__name__))
            print(e.__str__())


def start_status_queue_handler(status_queue, db):
    thread = threading.Thread(target=handle_statue_queue, name="Redis-Handler", args=(status_queue, db))
    thread.start()

    return thread
