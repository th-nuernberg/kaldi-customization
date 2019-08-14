from connector import *
from models import Resource, ResourceStateEnum, ResourceTypeEnum, Training, TrainingStateEnum, TrainingResource
from redis_communication import create_kaldi_job

import uuid


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

    try:
        db_training.status = data_prep_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from data-prep')
        return

    db_session.add(db_training)
    db_session.commit()

    if db_training.status == TrainingStateEnum.Training_DataPrep_Success:
        db_training.status = TrainingStateEnum.Training_Pending
        db_session.add(db_training)
        db_session.commit()

        create_kaldi_job(
            training_id=db_training.id,
            acoustic_model_id=db_training.project.acoustic_model_id)
