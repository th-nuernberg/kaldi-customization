from connector import *
from models import Training, TrainingStateEnum

import uuid


kaldi_status_mapping = {
    KaldiStatusCode.IN_PROGRESS: TrainingStateEnum.Training_In_Progress,
    KaldiStatusCode.FAILURE: TrainingStateEnum.Training_Failure,
    KaldiStatusCode.SUCCESS: TrainingStateEnum.Decodable
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

    try:
        db_training.status = kaldi_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from kaldi')
        return

    db_session.add(db_training)
    db_session.commit()

    # TODO: handle callback
