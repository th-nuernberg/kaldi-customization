import json
import threading

from .text_prep import handle_text_prep_status


def handle_statue_queue(status_queue, db, logger):
    '''
    Listens to STATUS_QUEUE and handle the messages.
    '''

    for message in status_queue.listen():
        try:
            logger.info("new pubsub message:")
            logger.info(message)
            if message['type'] == 'message':
                try:
                    msg_data = json.loads(message['data'])
                except ValueError as e:
                    logger.warning(e)
                    continue
                
                if msg_data and "type" in msg_data and "text" in msg_data and "status" in msg_data:
                    if msg_data['type'] == 'text-prep':
                        logger.info("handle text prep status...")
                        handle_text_prep_status(msg_data, db, logger)
                        logger.info("...handled text prep status")
                    else:
                        logger.warning('unknown type in status queue!')
        except Exception as e:
            logger.error("Exception at status queue: {}".format(type(e).__name__))
            logger.error(e.__str__())


def start_status_queue_handler(status_queue, db, logger):
    thread = threading.Thread(target=handle_statue_queue, name="Redis-Handler", args=(status_queue, db, logger))
    thread.start()

    return thread
