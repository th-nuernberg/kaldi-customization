import connexion
import six

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.resource_reference_object import ResourceReferenceObject  # noqa: E501
from openapi_server.models.training import Training  # noqa: E501
from openapi_server import util

from models import db
from models.project import Project as DB_Project
from models.user import User as DB_User
from models.acousticmodel import AcousticModel as DB_AcousticModel
from models.resource import Resource as DB_Resource, ResourceStateEnum as DB_ResourceStateEnum
from models.training import Training as DB_Training, TrainingStateEnum as DB_TrainingStateEnum
from models.training_resource import TrainingResource as DB_TrainingResource

from redis_communication import create_dataprep_job
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets, copy_object_in_bucket
from config import minio_client

import os
from mapper import mapper

TEMP_CORPUS_FOLDER = '/tmp/corpus'

def assign_resource_to_training(project_uuid, training_version, resource_reference_object=None):  # noqa: E501
    """Assign a resource to the training

    Assign the specified resource to the training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_reference_object: Resource that needs to be added
    :type resource_reference_object: dict | bytes

    :rtype: Resource
    """
    if connexion.request.is_json:
        resource_reference_object = ResourceReferenceObject.from_dict(connexion.request.get_json())  # noqa: E501

    db_proj = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_proj:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(
        project_id=db_proj.id, version=training_version).first()

    if not db_training:
        return ("Training not found", 404)

    if not db_training.can_assign_resource():
        return ("Training already in progress", 400)

    db_resource = DB_Resource.query.filter_by(
        uuid=resource_reference_object.resource_uuid).first()

    if not db_resource:
        return ("Resource not found", 404)

    if db_resource.has_error():
        return ("Resource has errors", 400)

    #if the resource is already added, return the previous
    db_training_resource = DB_TrainingResource.query.filter_by(
        training_id=db_training.id, origin_id=db_resource.id).first()
    if db_training_resource:
        return mapper.db_training_resource_to_front(db_training_resource)

    db_training_resource = DB_TrainingResource(
        training=db_training, origin=db_resource)
    db.session.add(db_training_resource)
    db.session.commit()

    #if text prep is already done, we should copy corpus to the new training_resource
    if db_resource.status == DB_ResourceStateEnum.TextPreparation_Success:
        copy_object_in_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], db_resource.uuid + "/corpus.txt", minio_buckets["TRAINING_RESOURCE_BUCKET"], db_training_resource.id + "/corpus.txt")

    
    if db_resource.status != DB_ResourceStateEnum.TextPreparation_Success:
        db_training.status = DB_TrainingStateEnum.TextPrep_Pending
    elif db_training.status == DB_TrainingStateEnum.Init:
        db_training.status = DB_TrainingStateEnum.Trainable

    db.session.add(db_training)
    db.session.commit()

    return mapper.db_training_resource_to_front(db_training_resource)


def create_training(project_uuid):  # noqa: E501
    """Create a new training

     # noqa: E501

    :param project_uuid: Project object that needs to be trained
    :type project_uuid: 

    :rtype: Training
    """
    # TODO: check the ownership of the file

    db_proj = DB_Project.query.filter_by(uuid=project_uuid).first()

    if (db_proj is None):
        return ("Project not found", 404)

    db_last_training = DB_Training.query.filter_by(
        project_id=db_proj.id).order_by(DB_Training.version.desc()).first()

    version = db_last_training.id + 1 if db_last_training else 1

    db_training = DB_Training(
        project=db_proj,
        version=version
    )
    db.session.add(db_training)
    db.session.commit()

    return mapper.db_training_to_front(db_training)


def delete_assigned_resource_from_training(project_uuid, training_version, resource_uuid):  # noqa: E501
    """Remove a resource from the training

    Removes the assigned resource from the training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 

    :rtype: None
    """
    return 'do some magic!'


def get_corpus_of_training_resource(project_uuid, training_version, resource_uuid):  # noqa: E501
    """Get the corpus of the resource

    Returns the corpus of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 

    :rtype: str
    """
    if not os.path.exists(TEMP_CORPUS_FOLDER):
        os.makedirs(TEMP_CORPUS_FOLDER)
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    print(db_training)
    print(db_training.status)
    if db_training.status not in (DB_TrainingStateEnum.Init,DB_TrainingStateEnum.Trainable,DB_TrainingStateEnum.TextPrep_Pending, DB_TrainingStateEnum.TextPrep_Failure):
        return ("Training already started or done", 409)
    
    db_resource = DB_Resource.query.filter(DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_resource is None:
        return ("Resource not assigned to this Training", 404)

    target_path = os.path.join(TEMP_CORPUS_FOLDER,"{}".format("tmp.txt"))
    download_from_bucket(minio_client,minio_buckets["TRAINING_RESOURCE_BUCKET"],str(db_training_resource.id) + "/corpus.txt",target_path)
    
    ret_val = "Error!"
    with open(target_path) as f:
        ret_val = f.read()

    os.remove(target_path)
    return ret_val


def get_training_by_version(project_uuid, training_version):  # noqa: E501
    """Find project training results by UUID

    Returns the training object # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: Training
    """
    db_proj = DB_Project.query.filter_by(uuid=project_uuid).first()

    if not db_proj:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(
        project_id=db_proj.id, version=training_version).first()

    if not db_training:
        return ("Training not found", 404)

    return mapper.db_training_to_front(db_training)


def set_corpus_of_training_resource(project_uuid, training_version, resource_uuid, body):  # noqa: E501
    """Set the corpus of the resource

    Updates the corpus of the specified resource for this training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param resource_uuid: UUID of the resource
    :type resource_uuid: 
    :param body: New or updated corpus as plain text
    :type body: str

    :rtype: None
    """
    if not os.path.exists(TEMP_CORPUS_FOLDER):
        os.makedirs(TEMP_CORPUS_FOLDER)
    
    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    if db_training.status not in (DB_TrainingStateEnum.Init,DB_TrainingStateEnum.Trainable,DB_TrainingStateEnum.TextPrep_Pending, DB_TrainingStateEnum.TextPrep_Failure):
        return ("Training already started or done", 409)
    
    db_resource = DB_Resource.query.filter(DB_Resource.uuid == resource_uuid).first()

    if db_resource is None:
        return ("Resource not found", 404)

    db_training_resource = DB_TrainingResource.query.filter_by(origin_id=db_resource.id) \
        .filter_by(training_id=db_training.id).first()

    if db_resource is None:
        return ("Resource not assigned to this Training", 404)


    target_path = os.path.join(TEMP_CORPUS_FOLDER,"{}".format("tmp.txt"))

    with open(target_path,"wb") as f:
        f.write(body)

    upload_to_bucket(minio_client,minio_buckets["TRAINING_RESOURCE_BUCKET"],str(db_training_resource.id) + "/corpus.txt",target_path)
    
    os.remove(target_path)
    return ("Success",200)


def start_training_by_version(project_uuid, training_version):  # noqa: E501
    """Start the specified training

    Start the training process for the specified training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: Training
    """
    db_project = DB_Project.query.filter_by(uuid=project_uuid).first()
    db_training = DB_Training.query.filter_by(
        version=training_version, project=db_project).first()

    if db_training.status != DB_TrainingStateEnum.Trainable:
        return ("training already done or pending", 400)

    db_training.status = DB_TrainingStateEnum.Training_Pending
    db_training_resources = DB_TrainingResource.query.filter(DB_TrainingResource.training_id == db_training.id).all()

    db.session.add(db_training)
    db.session.commit()

    create_dataprep_job(
        acoustic_model_id=db_project.acoustic_model_id,
        corpi=[r.id for r in db_training_resources],
        training_id=db_training.id
    )

    return mapper.db_training_to_front(db_training)
