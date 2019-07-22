import connexion
import os
import six

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.file_status import FileStatus
from openapi_server.models.file_type import FileType

from openapi_server import util
from models import db, File, FileTypeEnum, FileStateEnum
from werkzeug.utils import secure_filename

from minio_communication import download_from_bucket, upload_to_bucket
from redis_communication import create_textprep_job
from config import minio_client

TEMP_UPLOAD_FOLDER = '/tmp/fileupload'
TEXTS_IN_BUCKET = 'texts-in'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in FileTypeEnum.__members__:
            return FileTypeEnum[filetype]
    return None

def create_file(body):  # noqa: E501
    """Create/Upload a new file

     # noqa: E501

    :param body: File object that needs to be created
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Resource.from_dict(connexion.request.get_json())  # noqa: E501

    if 'file' not in connexion.request.files:
        return ('No file', 405)
    file = connexion.request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return ('No file selected', 405)
    
    filename = secure_filename(file.filename)
    filetype = get_filetype(filename)
    if file and filetype is not None:
        # file is okay: create db entry, store to dfs and create textprep job

        db_file = File(
            name=filename,
            status=FileTypeEnum.Upload_InProgress,
            file_type=filetype,
            owner=0 #TODO: wie kann der Benutzer ermittelt werden?
        )
        db.session.add(db_file)
        db.session.commit()

        # cache file in local file system, then upload to MinIO
        file_path = os.path.join(TEMP_UPLOAD_FOLDER, db_file.id)
        file.save(file_path)

        upload_result = upload_to_bucket(
            minio_client=minio_client,
            #TODO: Wo ist der minio_client definiert?!
            bucket=TEXTS_IN_BUCKET,
            filename=db_file.id,
            file_path=file_path
        )

        if upload_result[0]:
            db_file.status = FileTypeEnum.Upload_Failure
        else:
            db_file.status = FileTypeEnum.TextPreparation_Ready

        db.session.add(db_file)
        db.session.commit()

        create_textprep_job(db_file.id, db_file.file_type)

        db_file.status = FileTypeEnum.TextPreparation_Pending
        db.session.add(db_file)
        db.session.commit()

        return Resource(
            name=db_file.filename,
            status=FileStatus[db_file.status],
            file_type=FileType[db_file.file_type]
        )
    
    return 'do some magic!'


def get_file_by_uuid(file_uuid):  # noqa: E501
    """Find file by UUID

    Returns a single file # noqa: E501

    :param file_uuid: UUID of file to return
    :type file_uuid: str

    :rtype: Resource
    """

    return Resource(name="Hello", status=FileStateEnum.TextPreparation_Success, file_type=FileType.jpg)

    db_file = File.query.get(file_uuid)
    if (db_file is None):
        return ("Page not found", 404)

    # check the ownership of the file
    # db_file.owner

    # retrieve file from MinIO

    # return file
    return File.query.get(file_uuid)
