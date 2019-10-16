from connector import *
from models import Training, TrainingStateEnum
from redis_communication import create_kaldi_job
from .requests_util import make_async_request

import json

data_prep_status_mapping = {
    DataPrepStatusCode.IN_PROGRESS: TrainingStateEnum.Training_DataPrep_InProgress,
    DataPrepStatusCode.SUCCESS: TrainingStateEnum.Training_DataPrep_Success,
    DataPrepStatusCode.FAILURE: TrainingStateEnum.Training_DataPrep_Failure
}


def handle_data_prep_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    status = DataPrepStatus(**msg_data)

    db_training = db_session.query(Training).filter_by(id=status.training_id).first()

    if not db_training:
        print('[Error] Received invalid training_id from data-prep')
        return
    
    if(db_training.prepare_callback != "{}"):
        callback = json.loads(db_training.prepare_callback)
        print("Preparing callback")
        make_async_request(method=callback["method"], url=callback["url"], data=str(db_training))

    try:
        db_training.status = data_prep_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from data-prep')
        return

    db_session.add(db_training)
    db_session.commit()