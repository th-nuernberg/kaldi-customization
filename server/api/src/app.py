#!/usr/local/bin/python3
from bootstrap import *

root_project = Project(uuid='root', name='Test Project')
db.session.add(root_project)
root_model = Model(project=root_project)
db.session.add(root_model)

project1 = Project(uuid='project#1', name='Test Project')
db.session.add(project1)

resource1 = Resource(model=root_model, file_name='res0', file_type=ResourceTypeEnum.PNG, status=ResourceStateEnum.Upload_InProgress)
db.session.add(resource1)
print(resource1)

derived_model0 = Model(project=project1, parent=root_model)
db.session.add(derived_model0)

derived_model1 = Model(project=project1, parent=root_model)
db.session.add(derived_model1)

db.session.commit()

print(root_model.children)
print(derived_model0.parent.project.name)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import logging
import json

TEXT_PREP_UPLOAD_FOLDER = '/www/texts/in'
TEXT_PREP_FINISHED_FOLDER = '/www/texts/out'
TEXT_PREP_QUEUE = 'Text-Prep-Queue'

@app.route('/')
def hello():
    return 'API-Server'

def allowed_file_for_textprep(filename):
    '''
    Returns true if the given filetype can be processed by the text preperation worker.
    '''
    text_prep_extensions = set(['txt', 'pdf', 'png', 'jpg', 'html', 'docx'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in text_prep_extensions

def create_textprep_job(filename):
    entry = {
        "text" : filename,
        "type" : filename.rsplit('.')[1].lower()
    }
    redis_conn.rpush(TEXT_PREP_QUEUE, json.dumps(entry))
    return

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
        if file and allowed_file_for_textprep(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(TEXT_PREP_UPLOAD_FOLDER, filename))
            create_textprep_job(filename)
            return 'ok'
    return upload_form

from flask import send_from_directory

@app.route('/texts/in/<filename>')
def download_texts_in_file(filename):
    return send_from_directory(TEXT_PREP_UPLOAD_FOLDER, filename)
    
@app.route('/texts/out/<filename>')
def download_texts_out_file(filename):
    return send_from_directory(TEXT_PREP_FINISHED_FOLDER, 'unique_word_list.txt') # filename)

if __name__ == "__main__":
    print("API-Server is running")
    #infinite_loop()
    print("API-Server stops running")
