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

from models import db
from models import Resource as DB_Resource
from models import ResourceTypeEnum as DB_ResourceType
from models import ResourceStateEnum as DB_ResourceState
from models import User as DB_User
from models import Project as DB_Project
from models import Training as DB_Training
from models import TrainingResource as DB_TrainingResource
from models import TrainingStateEnum as DB_TrainingStateEnum

from sqlalchemy import and_

from werkzeug.utils import secure_filename
from flask import stream_with_context, Response

from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
from redis_communication import create_textprep_job
from config import minio_client
from mapper import mapper

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'


def get_db_project_training(project_uuid, training_version):
    """
    Queries the database and returns the specified project / training.
    Returns None if not found
    """
    current_user = connexion.context['token_info']['user']

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()
    if db_proj is None:
        return None, None

    db_train = DB_Training.query.filter_by(
        and_(project=db_proj, version=training_version))

    return db_proj, db_train


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
    current_user = connexion.context['token_info']['user']

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

    print('Set ownership to user 1')

    db_resource = DB_Resource(
        name=filename,
        status=DB_ResourceState.Upload_InProgress,
        resource_type=filetype,
        owner=current_user
    )
    db.session.add(db_resource)
    db.session.commit()

    print('Added database entry: ' + str(db_resource))

    # cache file in local file system, then upload to MinIO
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_resource.uuid))
    upfile.save(local_file_path)

    minio_file_path = str(db_resource.uuid) + '/source'

    status, message = upload_to_bucket(
        minio_client=minio_client,
        bucket=minio_buckets["RESOURCE_BUCKET"],
        filename=minio_file_path,
        file_path=local_file_path
    )

    os.remove(local_file_path)

    if status:
        db_resource.status = DB_ResourceState.TextPreparation_Ready
    else:
        db_resource.status = DB_ResourceState.Upload_Failure

    db.session.add(db_resource)
    db.session.commit()

    print('Uploaded file to MinIO: ' + str(db_resource))

    if db_resource.status == DB_ResourceState.TextPreparation_Ready:
        create_textprep_job(str(db_resource.uuid), db_resource.resource_type)

        db_resource.status = DB_ResourceState.TextPreparation_Pending
        db.session.add(db_resource)
        db.session.commit()

        print('Created TextPreparation job: ' + str(db_resource))

    return mapper.db_resource_to_front(db_resource)


def get_resource():  # noqa: E501
    """Returns a list of available resources

     # noqa: E501


    :rtype: List[Resource]
    """
    current_user = connexion.context['token_info']['user']

    db_resources = DB_Resource.query.filter_by(owner_id=current_user.id).all()

    return [mapper.db_resource_to_front(r) for r in db_resources]


def get_resource_by_uuid(resource_uuid):  # noqa: E501
    """Find resource by UUID

    Returns a single resource # noqa: E501

    :param resource_uuid: UUID of resource to return
    :type resource_uuid: str

    :rtype: Resource
    """
    current_user = connexion.context['token_info']['user']

    db_resource = DB_Resource.query.filter_by(
        uuid=resource_uuid, owner_id=current_user.id).first()

    if (db_resource is None):
        return ("File not found", 404)

    return mapper.db_resource_to_front(db_resource)


def get_resource_data(resource_uuid):  # noqa: E501
    """Returns the resource content

    Returns the resource content # noqa: E501

    :param resource_uuid: UUID of resource to return
    :type resource_uuid: str

    :rtype: file
    """
    current_user = connexion.context['token_info']['user']

    db_resource = DB_Resource.query.filter_by(
        uuid=resource_uuid, owner_id=current_user.id).first()

    if not db_resource:
        print('Resource {} in DB not found'.format(resource_uuid))
        return ("File not found", 404)

    status, stream = download_from_bucket(minio_client,
        bucket=minio_buckets["RESOURCE_BUCKET"],
        filename='{}/source'.format(db_resource.uuid)
    )

    if not status:  # means no success
        print('Resource {} in MinIO not found'.format(resource_uuid))
        return ("File not found", 404)

    response = Response(response=stream, content_type=db_resource.mimetype(), direct_passthrough=True)
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(db_resource.name)
    return response
