import connexion
import os
import six
import uuid
import datetime

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.resource_status import ResourceStatus
from openapi_server.models.resource_type import ResourceType

from openapi_server import util
from models import db, Resource as DB_Resource, ResourceTypeEnum as DB_ResourceType, ResourceStateEnum as DB_ResourceState, User as DB_User
from werkzeug.utils import secure_filename
from flask import send_file

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from redis_communication import create_textprep_job
from config import minio_client

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in DB_ResourceType.__members__:
            return DB_ResourceType[filetype]
    return None

def create_resource(upfile):  # noqa: E501
    """Create/Upload a new resource

     # noqa: E501

    :param upfile: File object that needs to be uploaded
    :type upfile: str

    :rtype: Resource
    """

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

    return Resource(
        name=db_file.name,
        status=ResourceStatus.ResourceStateEnum_to_ResourceStatus(db_file.status),
        resource_type=ResourceType.ResourceTypeEnum_to_ResourceType(db_file.resource_type),
        uuid=db_file.uuid
    )


def get_resource():  # noqa: E501
    """Returns a list of available resources

     # noqa: E501


    :rtype: List[Resource]
    """

    #TODO filter by user
    db_resources = DB_Resource.query.all()

    return [ Resource(
        name=r.name,
        status=ResourceStatus.ResourceStateEnum_to_ResourceStatus(r.status),
        resource_type=ResourceType.ResourceTypeEnum_to_ResourceType(r.resource_type),
        uuid=r.uuid
    ) for r in db_resources ]


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

    this_resource = Resource(
        name=db_file.name, 
        status=ResourceStatus.ResourceStateEnum_to_ResourceStatus(db_file.status),
        resource_type=ResourceType.ResourceTypeEnum_to_ResourceType(db_file.resource_type),
        uuid=db_file.uuid
    )

    return this_resource


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
