import connexion
import os
import six
import uuid
import datetime

from openapi_server.models.binary_resource_object import BinaryResourceObject  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.training import Training  # noqa: E501
from openapi_server.models.resource_status import ResourceStatus
from openapi_server.models.resource_type import ResourceType
from openapi_server.models.resource_reference_object import ResourceReferenceObject  # noqa: E501

from openapi_server import util
from models import db, Resource as DB_Resource, ResourceTypeEnum as DB_ResourceType, ResourceStateEnum as DB_ResourceState, User as DB_User
from werkzeug.utils import secure_filename
from flask import send_file

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from redis_communication import create_textprep_job
from config import minio_client
from mapper import mapper

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'

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
    return 'do some magic!'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in DB_ResourceType.__members__:
            return DB_ResourceType[filetype]
    return None

def create_resource(binary_resource_object):  # noqa: E501
    """Create/Upload a new resource

     # noqa: E501

    :param binary_resource_object: 
    :type binary_resource_object: dict | bytes

    :rtype: Resource
    """

    upfile = binary_resource_object.upfile
    print('Received new file: ' + str(upfile))

    # if user does not select file, browser also
    # submit an empty part without filename
    if upfile is None:
        return ('Invalid input', 405)
    
    filename = secure_filename(upfile.filename)
    filetype = get_filetype(filename)

    if filetype is None:
        return ('Invalid input', 405)
    
    # file is okay: create db entry, store to dfs and create textprep job

    my_user = DB_User.query.get(1)
    print('Set ownership to user 1')

    db_file = DB_Resource(
        name=filename,
        status=DB_ResourceState.Upload_InProgress,
        resource_type=filetype,
        owner=my_user #TODO: wie kann der Benutzer ermittelt werden?
    )
    db.session.add(db_file)
    db.session.commit()

    print('Added database entry: ' + str(db_file))

    # cache file in local file system, then upload to MinIO
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_file.uuid))
    upfile.save(local_file_path)

    minio_file_path = str(db_file.uuid) + '/' + str(db_file.uuid)

    upload_result = upload_to_bucket(
        minio_client=minio_client,
        bucket=minio_buckets["RESOURCE_BUCKET"],
        filename=minio_file_path,
        file_path=local_file_path
    )

    #TODO: delete local file local_file_path

    if upload_result[0]:
        db_file.status = DB_ResourceState.TextPreparation_Ready
    else:
        db_file.status = DB_ResourceState.Upload_Failure

    db.session.add(db_file)
    db.session.commit()

    print('Uploaded file to MinIO: ' + str(db_file))

    if db_file.status == DB_ResourceState.TextPreparation_Ready:
        create_textprep_job(str(db_file.uuid), db_file.resource_type)

        db_file.status = DB_ResourceState.TextPreparation_Pending
        db.session.add(db_file)
        db.session.commit()

        print('Created TextPreparation job: ' + str(db_file))

    return mapper.db_resource_to_front(db_file)

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
    return 'do some magic!'


def get_resource():  # noqa: E501
    """Returns a list of available resources

     # noqa: E501


    :rtype: List[Resource]
    """

    #TODO filter by user
    db_resources = DB_Resource.query.all()

    return [ mapper.db_resource_to_front(r) for r in db_resources ]


def get_resource_by_uuid(resource_uuid):  # noqa: E501
    """Find resource by UUID

    Returns a single resource # noqa: E501

    :param resource_uuid: UUID of resource to return
    :type resource_uuid: str

    :rtype: Resource
    """

    #TODO: check the ownership of the file
    # db_file.owner

    db_file = DB_Resource.query.filter_by(uuid=resource_uuid).first()

    if (db_file is None):
        return ("File not found", 404)

    return mapper.db_resource_to_front(db_file)


def get_resource_data(resource_uuid):  # noqa: E501
    """Returns the resource content

    Returns the resource content # noqa: E501

    :param resource_uuid: UUID of resource to return
    :type resource_uuid: str

    :rtype: file
    """

    #TODO: check the ownership of the file
    db_file = DB_Resource.query.filter_by(uuid=resource_uuid).first()

    if (db_file is None):
        print('Resource {} in DB not found'.format(resource_uuid))
        return ("File not found", 404)
    
    minio_file_path = str(db_file.uuid) + '/' + str(db_file.uuid)
    
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    # use local file system as file cache?
    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_file.uuid))
    
    if not os.path.exists(local_file_path):
        download_result = download_from_bucket(
            minio_client=minio_client,
            bucket=minio_buckets["RESOURCE_BUCKET"],
            filename=minio_file_path,
            target_path=local_file_path
        )

        if not download_result[0]: # means no success
            print('Resource {} in MinIO not found'.format(resource_uuid))
            return ("File not found", 404)

    return send_file(local_file_path, as_attachment=True, attachment_filename=db_file.name)


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
    return 'do some magic!'
