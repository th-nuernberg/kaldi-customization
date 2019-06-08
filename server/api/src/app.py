#!/usr/local/bin/python3
from bootstrap import *
from flask import logging

root_project = Project(uuid='root', name='Test Project')
db.session.add(root_project)
root_model = Model(project=root_project)
db.session.add(root_model)

project1 = Project(uuid='project#1', name='Test Project')
db.session.add(project1)

resource1 = Resource(model=root_model, file_name='res0', file_type=ResourceTypeEnum.png, status=ResourceStateEnum.Upload_InProgress)
db.session.add(resource1)
app.logger.info(resource1)

derived_model0 = Model(project=project1, parent=root_model)
db.session.add(derived_model0)

derived_model1 = Model(project=project1, parent=root_model)
db.session.add(derived_model1)

db.session.commit()

app.logger.info(root_model.children)
app.logger.info(derived_model0.parent.project.name)

db.session.close()

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json

TEXT_PREP_UPLOAD_FOLDER = '/www/texts/in'
TEXT_PREP_FINISHED_FOLDER = '/www/texts/out'
TEXT_PREP_QUEUE = 'Text-Prep-Queue'

@app.route('/')
def hello():
    return 'API-Server'

def get_filetype(filename):
    '''
    Returns the filetype or None, if it cannot be processed by the text preperation worker.
    '''
    if '.' in filename:
        filetype = filename.rsplit('.', 1)[1].lower()
        if filetype in ResourceTypeEnum.__members__:
            return ResourceTypeEnum[filetype]
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

            db_resource = Resource(model=root_model, file_name=filename, file_type=filetype, status=ResourceStateEnum.Upload_InProgress)
            db.session.add(db_resource)
            db.session.commit()
            db.session.close()
            app.logger.info("db entry created")

            # store file with original file name to dfs.
            #TODO: Change it to db key
            file.save(os.path.join(TEXT_PREP_UPLOAD_FOLDER, new_resource))
            app.logger.info("file saved")

            create_textprep_job(new_resource, filetype)
            return str(new_resource)
    return upload_form

@app.route('/db/resources')
def dbquery():
    app.logger.info("resource query")
    app.logger.info(Resource.query.all())
    return Resource.query.first().__repr__()

from flask import send_from_directory

@app.route('/texts/in/<filename>')
def download_texts_in_file(filename):
    #TODO add original filename with extension
    return send_from_directory(TEXT_PREP_UPLOAD_FOLDER, filename)
    
@app.route('/texts/out/<filename>')
def download_texts_out_file(filename):
    #TODO add original filename with extension
    file_path = TEXT_PREP_FINISHED_FOLDER + '/' + filename
    with open(file_path, "r") as file_handler:
        return file_handler.read()
    return "Error at file " + filename

if __name__ == "__main__":
    app.logger.info("API-Server is running")
    #infinite_loop()
    # listen for finished jobs (pub_sub)
    app.logger.info("API-Server stops running")
    