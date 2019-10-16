from connector import *
from models import Training, TrainingStateEnum
from .requests_util import make_async_request

import uuid
import json

kaldi_status_mapping = {
    KaldiStatusCode.IN_PROGRESS: TrainingStateEnum.Training_In_Progress,
    KaldiStatusCode.SUCCESS: TrainingStateEnum.Training_Success,
    KaldiStatusCode.FAILURE: TrainingStateEnum.Training_Failure
}


def handle_kaldi_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    status = KaldiStatus(**msg_data)

    db_training = db_session.query(Training).filter_by(id=status.training_id).first()

    if not db_training:
        print('[Error] Received invalid training_id from kaldi')
        return

    if(db_training.train_callback != "{}"):
        callback = json.loads(db_training.train_callback)
        print("Preparing callback")
        make_async_request(method=callback["method"], url=callback["url"], data=str(db_training))


    try:
        db_training.status = kaldi_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from kaldi')
        return

    db_session.add(db_training)
    db_session.commit()
