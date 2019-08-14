from connector import *
from models import Resource, ResourceStateEnum, ResourceTypeEnum, Training, TrainingStateEnum, TrainingResource
import uuid


text_prep_status_mapping = {
    TextPrepStatusCode.IN_PROGRESS: ResourceStateEnum.TextPreparation_InProgress,
    TextPrepStatusCode.SUCCESS: ResourceStateEnum.TextPreparation_Success,
    TextPrepStatusCode.FAILURE: ResourceStateEnum.TextPreparation_Failure
}


def handle_text_prep_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    status = TextPrepStatus(**msg_data)

    db_resource = db_session.query(Resource).filter(Resource.uuid == status.resource_uuid).first()

    if not db_resource:
        print('[Error] Received invalid Uuid from text-prep')
        return

    try:
        db_resource.status = text_prep_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from text-prep')
        return

    print('[Status] ' + status.message)

    db_session.add(db_resource)
    db_session.commit()

    if db_resource.status == ResourceStateEnum.TextPreparation_Success:
        db_trainings = db_session.query(Training) \
            .join(TrainingResource, Training.id == TrainingResource.training_id) \
            .join(Resource, TrainingResource.origin_id == Resource.id) \
            .all()

        for db_training in db_trainings:
            db_resources = db_session.query(Resource) \
                .join(TrainingResource, Resource.id == TrainingResource.origin_id) \
                .join(Training, Training.id == TrainingResource.training_id) \
                .all()

            training_status = TrainingStateEnum.Trainable
            for db_resource in db_resources:
                if db_resource.status == ResourceStateEnum.TextPreparation_Failure:
                    training_status = TrainingStateEnum.Training_DataPrep_Failure
                elif db_resource.status == ResourceStateEnum.TextPreparation_InProgress:
                    training_status = TrainingStateEnum.Training_DataPrep_Pending

            db_training.status = training_status
            db_session.add(db_training)

    db_session.commit()
