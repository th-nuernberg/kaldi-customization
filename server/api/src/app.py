#!/usr/bin/python
import config
import connector
import connexion
import json
import logging.config
import minio
import os
import redis
import threading

from status_queue.handler import start_status_queue_handler
from openapi_server import encoder
from models import *
from oauth2 import config_oauth
from routes.auth import bp as auth_bp


def setup_minio(minio_client, buckets):
    '''Create buckets if they do not exist'''

    for bucket_name in buckets:
        try:
            minio_client.make_bucket(bucket_name)
        except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
            pass
        except minio.error.ResponseError as e:
            raise e


connex_app = connexion.FlaskApp(__name__, specification_dir='openapi_server/openapi',  options={
    'swagger_ui': True
})
connex_app.add_api('openapi.yaml', pythonic_params=True, resolver=connexion.resolver.RestyResolver('api'))

app = connex_app.app
app.json_encoder = encoder.JSONEncoder


##########################################################################################
# TODO: Move to swagger-controllers >>>

from flask import flash, request, Response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

TEXT_PREP_UPLOAD_FOLDER = '/www/texts/in'
TEXT_PREP_FINISHED_FOLDER = '/www/texts/out'


def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in FileTypeEnum.__members__:
            return FileTypeEnum[filetype]
    return None


def create_textprep_job(resourcename, filetype):
    '''
    Creates a new job in the queue for a text preperation worker.
    '''
    entry = {
        "text" : resourcename,
        "type" : filetype.name
    }
    redis_conn.rpush(config.minio_buckets.TEXT_PREP_QUEUE, json.dumps(entry))
    return


def create_g2p_job(uniquewordlists, language_model='Voxforge'):
    '''
    Creates a new job in the queue for a g2p worker.
    '''
    entry = {
        "bucket-in" : G2P_IN_BUCKET,
        "bucket-out" : G2P_OUT_BUCKET,
        "language_model" : language_model,
        "uniquewordlists" : [wl.name for wl in uniquewordlists]
    }
    redis_conn.rpush(config.minio_buckets.G2P_QUEUE, json.dumps(entry))
    return


def get_basename(filename):
    '''
    Returns the basename of a filename, i.e. without extension.
    '''
    if '.' in filename:
        filename = filename.rsplit('.', 1)[0].lower()
    return filename


@app.route('/api/texts/in', methods=['GET', 'POST'])
def upload_file_for_textprep():
    '''
    Implements a POST-request for uploading files.
    After storing the file in the DFS a job for the text preperation worker will be created. 
    '''
    # a simple upload form will be returned if no file was attached
    # replace this later with a status code
    upload_form = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return upload_form
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return upload_form
        filetype = get_filetype(file.filename)
        if file and filetype is not None:
            # file is okay: create db entry, store to dfs and create textprep job
            filename = secure_filename(file.filename)
            app.logger.info("new file arrived!")
            app.logger.info(filename)
            app.logger.info(filetype)

            new_resource = get_basename(filename) #TODO change to DB key

            db_resource = Resource(model=root_model, resource_type=FileTypeEnum.upload, name=new_resource, file_type=filetype, status=FileStateEnum.TextPreparation_Pending)
            db.session.add(db_resource)
            db.session.commit()
            db.session.close()
            app.logger.info("db entry created")

            # store file in the file system, then to MinIO
            file_path = os.path.join(TEXT_PREP_UPLOAD_FOLDER, new_resource)
            file.save(file_path)
            app.logger.info("file saved to file system")

            try:
                resource_key = minioClient.fput_object(bucket_name=TEXTS_IN_BUCKET, object_name=new_resource,
                                    file_path=file_path, content_type=file.content_type)
                app.logger.info(resource_key)
            except Exception as e:
                app.logger.error("Error at saving file to MinIO:")
                app.logger.error(e)
            app.logger.info("file saved to MinIO")

            create_textprep_job(new_resource, filetype)
            return str(new_resource)
    return upload_form


@app.route('/api/db/resources')
def dbquery():
    '''
    For debugging: shows all resources.
    '''
    app.logger.info("resource query")
    Response.content_type = "text/plain"
    def generate():
        for r in Resource.query.all():
            yield r.__repr__() + '<br>'
    return Response(generate())


@app.route('/api/texts/in/<filename>')
def download_texts_in_file(filename):
    '''
    Returns the raw input file.
    '''
    if '/' in filename:
        error_msg = "Do not place / in file names!"
        app.logger.warning(error_msg)
        return (error_msg, 404)
    #TODO add original filename with extension
    Response.content_type = "text/plain"
    return send_from_directory(TEXT_PREP_UPLOAD_FOLDER, filename)


@app.route('/api/texts/out/<filename>')
def download_texts_out_file(filename):
    '''
    Returns the list of words from a processed file.
    '''
    if '/' in filename:
        error_msg = "Do not place / in file names!"
        app.logger.warning(error_msg)
        return (error_msg, 404)
    file_path = TEXT_PREP_FINISHED_FOLDER + '/' + filename

    try:
        with open(file_path, "r") as file_handler:
            Response.content_type = "application/json"
            words = file_handler.read().split('\n')
            return json.dumps(list(filter(bool, words)))
    except FileNotFoundError:
        error_msg = "File not found: " + filename
        app.logger.warning(error_msg)
        return (error_msg, 404)
    except IOError as e:
        error_msg = "Error while reading file: " + filename
        app.logger.error(error_msg)
        app.logger.error(e)
        return (error_msg, 500)


@app.route('/api/g2p')
def start_g2p():
    '''
    Enqueues a g2p worker task.
    '''

    app.logger.info("Starts g2p...")

    # copy text-prep-worker results
    unique_word_lists = Resource.query.filter_by(
        resource_type=FileTypeEnum.unique_word_list, 
        status=FileStateEnum.G2P_Ready).all()

    for uwl in unique_word_lists:
        app.logger.info("copy resoure to g2p bucket: " + uwl.name)
        minioClient.copy_object(bucket_name=G2P_IN_BUCKET,
                                object_name=uwl.name,
                                object_source= "/" + TEXTS_OUT_BUCKET + "/" + uwl.name,
                                conditions=None,
                                metadata=None)
        uwl.status = FileStateEnum.G2P_Pending
        db.session.add(uwl)

    app.logger.info("Create task for g2p-worker")
    create_g2p_job(uniquewordlists=unique_word_lists, language_model='Voxforge')
    
    db.session.commit()
    db.session.close()

    return "OK"


@app.route('/api/stats')
def show_stats():
    return 'TODO: stats'


# <<< TODO: Move to swagger-controllers
##########################################################################################


if __name__ == "__main__":
    conf, _, status_queue, minio_client = connector.parse_args(
        'Kaldi Customization API Server', more_args=config.more_args)

    if conf.verbose:
        print(conf)

    app.config['SECRET_KEY'] = conf.secret_key

    logging.config.dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG' if conf.verbose else 'INFO',
            'handlers': ['wsgi']
        }
    })

    # configure databse connection
    if conf.db_type == 'mysql':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
            conf.db_user, conf.db_password, conf.db_host, conf.db_port, conf.db)
    elif conf.db_type == 'sqlite':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://{}'.format(conf.db)
    else:
        raise Exception('Invalid database type given')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 50

    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(auth_bp, url_prefix='/api')

    start_status_queue_handler(status_queue, db, app.logger)
    setup_minio(minio_client, config.minio_buckets.values())

    connex_app.run(host=conf.host, port=conf.port, debug=conf.verbose)
