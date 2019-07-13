#!/usr/local/bin/python3
from bootstrap import *
from db import *
from flask import logging
from connector import *

german = Language(name="German")
db.session.add(german)

acoustic_model = AcousticModel(name='Voxforge', language=german.id, model_type=ModelType.HMM_RNN)
db.session.add(acoustic_model)
"""
root_model = Model(project=root_project)
db.session.add(root_model)

project1 = Project(uuid='project#1', name='Test Project')
db.session.add(project1)

resource1 = Resource(model=root_model, name='res0', resource_type=ResourceTypeEnum.modelresult , file_type=ResourceFileTypeEnum.png, status=ResourceStateEnum.Upload_InProgress)
db.session.add(resource1)
app.logger.info(resource1)

derived_model0 = Model(project=project1, parent=root_model)
db.session.add(derived_model0)

derived_model1 = Model(project=project1, parent=root_model)
db.session.add(derived_model1)
"""
db.session.commit()

#app.logger.info(root_model.children)
#app.logger.info(derived_model0.parent.project.name)

db.session.close()

import os
from flask import Flask, flash, request, Response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import json
import threading

TEXT_PREP_UPLOAD_FOLDER = '/www/texts/in'
TEXT_PREP_FINISHED_FOLDER = '/www/texts/out'
TEXT_PREP_QUEUE = 'Text-Prep-Queue'
G2P_QUEUE = 'G2P-Queue'
STATUS_QUEUE = 'Status-Queue'


status_queue = StatusQueue(redis=redis_conn, key=STATUS_QUEUE)
kaldi_task_queue = TaskQueue(redis=redis_conn, key='Kaldi-Queue')


def handle_statue_queue():
    '''
    Listens to STATUS_QUEUE and handle the messages.
    '''
    pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(STATUS_QUEUE)

    for message in pubsub.listen():
        try:
            app.logger.info("new pubsub message:")
            app.logger.info(message)
            if message['type'] == 'message':
                try:
                    msg_data = json.loads(message['data'])
                except ValueError as e:
                    app.logger.warning(e)
                    continue
                
                if msg_data and "type" in msg_data and "text" in msg_data and "status" in msg_data:
                    if msg_data['type'] == 'text-prep':
                        app.logger.info("handle text prep status...")
                        handle_text_prep_status(msg_data)
                        app.logger.info("...handled text prep status")
                    else:
                        app.logger.warning('unknown type in status queue!')
        except Exception as e:
            app.logger.error("Exception at status queue: {}".format(type(e).__name__))
            app.logger.error(e.__str__())

def handle_text_prep_status(msg_data):
    '''
    Handle a status message from a text preparation worker.
    '''
    if msg_data['text'] == 'failure':
        app.logger.error('Failure at Text-Prep-Worker: ')
        if "msg" in msg_data:
            app.logger.error("Error message: " + msg_data['msg'])
    else:
        this_resource = Resource.query.filter_by(name=msg_data['text']).first()
        if this_resource is not None:
            app.logger.info('found resource in db: ' + this_resource.__repr__())
            try:
                resource_status = ResourceStateEnum(msg_data['status'])
                app.logger.info("resource status: " + ResourceStateEnum.status_to_string(resource_status))
            except ValueError as e:
                app.logger.warning("status is not valid!")
                app.logger.warning(e)
                resource_status = ResourceStateEnum.TextPreparation_Failure
            
            this_resource.status = resource_status
            app.logger.info('after update: ' + this_resource.__repr__())
            db.session.add(this_resource)

            if resource_status == ResourceStateEnum.Success:
                # add new db entry for g2p resource file
                try:
                    #TODO handle corpus and uwl!
                    db_resource = Resource(model=this_resource.model,
                                            name=this_resource.name,
                                            resource_type=ResourceTypeEnum.unique_word_list,
                                            status=ResourceStateEnum.G2P_Ready)
                    app.logger.info('added db entry for g2p resource file: ' + db_resource.__repr__())
                    db.session.add(db_resource)
                except Exception as e:
                    app.logger.error("Error at adding entry for g2p!")
                    raise e

            db.session.commit()
            db.session.close()
        else:
            app.logger.warning('did not found resource in db: ' + msg_data['text'] + '!')


redis_handler_thread = threading.Thread(target=handle_statue_queue, name="Redis-Handler")
redis_handler_thread.start()

@app.route('/')
def hello():
    return 'API-Server'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in ResourceFileTypeEnum.__members__:
            return ResourceFileTypeEnum[filetype]
    return None

def create_textprep_job(resourcename, filetype):
    '''
    Creates a new job in the queue for a text preperation worker.
    '''
    entry = {
        "text" : resourcename,
        "type" : filetype.name
    }
    redis_conn.rpush(TEXT_PREP_QUEUE, json.dumps(entry))
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
    redis_conn.rpush(G2P_QUEUE, json.dumps(entry))
    return

def get_basename(filename):
    '''
    Returns the basename of a filename, i.e. without extension.
    '''
    if '.' in filename:
        filename = filename.rsplit('.', 1)[0].lower()
    return filename


@app.route('/texts/in', methods=['GET', 'POST'])
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

            db_resource = Resource(model=root_model, resource_type=ResourceTypeEnum.upload, name=new_resource, file_type=filetype, status=ResourceStateEnum.TextPreparation_Pending)
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

@app.route('/db/resources')
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

@app.route('/texts/in/<filename>')
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
    
@app.route('/texts/out/<filename>')
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

@app.route('/g2p')
def start_g2p():
    '''
    Enqueues a g2p worker task.
    '''

    app.logger.info("Starts g2p...")

    # copy text-prep-worker results
    unique_word_lists = Resource.query.filter_by(
        resource_type=ResourceTypeEnum.unique_word_list, 
        status=ResourceStateEnum.G2P_Ready).all()

    for uwl in unique_word_lists:
        app.logger.info("copy resoure to g2p bucket: " + uwl.name)
        minioClient.copy_object(bucket_name=G2P_IN_BUCKET,
                                object_name=uwl.name,
                                object_source= "/" + TEXTS_OUT_BUCKET + "/" + uwl.name,
                                conditions=None,
                                metadata=None)
        uwl.status = ResourceStateEnum.G2P_Pending
        db.session.add(uwl)

    app.logger.info("Create task for g2p-worker")
    create_g2p_job(uniquewordlists=unique_word_lists, language_model='Voxforge')
    
    db.session.commit()
    db.session.close()

    return "OK"

@app.route('/test-model')
def test_model():
    task = KaldiTask(
        acoustic_model='acoustic_voxforge',
        base_model='model-1',
        new_model='model-2')

    kaldi_task_queue.submit(task)

    return task
# It is not possible to run a endless loop here...
# There is a thread for this task
app.logger.info("API-Server is running and listening to status queue")
