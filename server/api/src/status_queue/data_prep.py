from connector import *
from models import Training, TrainingStateEnum
from redis_communication import create_kaldi_job


data_prep_status_mapping = {
    DataPrepStatusCode.IN_PROGRESS: TrainingStateEnum.DataPrep_InProgress,
    DataPrepStatusCode.FAILURE: TrainingStateEnum.DataPrep_Failure,
    DataPrepStatusCode.SUCCESS: TrainingStateEnum.Trainable
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

    # TODO: trigger callback
