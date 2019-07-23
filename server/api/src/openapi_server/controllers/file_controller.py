import connexion
import os
import six

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.file_status import FileStatus
from openapi_server.models.file_type import FileType

from openapi_server import util
from models import db, Resource, ResourceTypeEnum, ResourceStateEnum, User
from werkzeug.utils import secure_filename

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
        if filetype in FileTypeEnum.__members__:
            return FileTypeEnum[filetype]
    return None

def create_file(upfile):  # noqa: E501
    """Create/Upload a new file

     # noqa: E501

    :param upfile: File object that needs to be created
    :type upfile: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = Resource.from_dict(connexion.request.get_json())  # noqa: E501

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

    my_user = User.query.get(1)
    print('Set ownership to user 1')

    db_file = File(
        name=filename,
        status=FileStateEnum.Upload_InProgress,
        file_type=filetype,
        owner=my_user #TODO: wie kann der Benutzer ermittelt werden?
    )
    db.session.add(db_file)
    db.session.commit()

    print('Added database entry: ' + str(db_file))

    # cache file in local file system, then upload to MinIO
    if not os.path.exists(TEMP_UPLOAD_FOLDER):
        os.makedirs(TEMP_UPLOAD_FOLDER)

    local_file_path = os.path.join(TEMP_UPLOAD_FOLDER, str(db_file.id))
    upfile.save(local_file_path)

    minio_file_path = str(db_file.id) + '/' + str(db_file.id)

    upload_result = upload_to_bucket(
        minio_client=minio_client,
        bucket=minio_buckets["RESOURCE_BUCKET"],
        filename=minio_file_path,
        file_path=local_file_path
    )

    #TODO: delete local file local_file_path

    if upload_result[0]:
        db_file.status = ResourceStateEnum.TextPreparation_Ready
    else:
        db_file.status = ResourceStateEnum.Upload_Failure

    db.session.add(db_file)
    db.session.commit()

    print('Uploaded file to MinIO: ' + str(db_file))

    if db_file.status == ResourceStateEnum.TextPreparation_Ready:
        create_textprep_job(str(db_file.id), db_file.file_type)

        db_file.status = ResourceStateEnum.TextPreparation_Pending
        db.session.add(db_file)
        db.session.commit()

        print('Created TextPreparation job: ' + str(db_file))

    return Resource(
        name=db_file.name,
        status=FileStatus.FileStateEnum_to_FileStatus(db_file.status),
        file_type=FileType.FileTypeEnum_to_FileType(db_file.file_type)
    )

def get_file_by_uuid(file_uuid):  # noqa: E501
    """Find file by UUID

    Returns a single file # noqa: E501

    :param file_uuid: UUID of file to return
    :type file_uuid: str

    :rtype: Resource
    """

    #TODO: check the ownership of the file
    # db_file.owner
    # retrieve file from MinIO vs. File information only

    db_file = Resource.query.get(file_uuid)

    if (db_file is None):
        return ("File not found", 404)

    this_resource = Resource(
        name=db_file.name, 
        status=ResourceStateEnum(db_file.status),
        file_type=ResourceTypeEnum(db_file.file_type)
    )

    return this_resource
