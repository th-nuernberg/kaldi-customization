#!/usr/bin/python3

import argparse
import json
import requests
import time

from openapi_client.rest import ApiException
from openapi_client import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser('API Test Script')
    parser.add_argument('client_id')
    parser.add_argument('client_secret')
    parser.add_argument('--username', '-u', default='kaldi')
    parser.add_argument('--password', '-p', default='valid')

    args = parser.parse_args()

    token_url = 'http://localhost:8080/api/oauth/token'
    
    data = {
        'grant_type': 'password',
        'scope': 'decode:projects read:projects train:projects write:projects read:resources write:resources read:user write:user',
        'username': args.username,
        'password': args.password
    }

    print('requesting access token')
    access_token_response = requests.post(token_url,
        data=data,
        verify=False,
        allow_redirects=False,
        auth=(args.client_id, args.client_secret))

    print('response')
    print(access_token_response.headers)
    print('body: ' + access_token_response.text)

    # we can now use the access_token as much as we want to access protected resources.
    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']
    print('access token: ' + access_token)

    configuration = Configuration(
        host='http://localhost:8080/api/v1',
        username=args.username,
        password=args.password
    )

    configuration.access_token = access_token
    api_client = ApiClient(configuration)

    decode_api_instance = DecodeApi(api_client)
    global_api_instance = GlobalApi(api_client)
    project_instance = ProjectApi(api_client)
    resource_instance = ResourceApi(api_client)
    training_instance = TrainingApi(api_client)

    print('Acoustic models:')
    acoustic_models = global_api_instance.get_acoustic_models()
    print(acoustic_models)

    print('Create project:')
    project = project_instance.create_project(CreateProjectObject(
        name='My first project',
        acoustic_model=acoustic_models[0].uuid
    ))
    print(project)

    print('Create training:')
    training = training_instance.create_training(project.uuid)
    print(training)

    print('Upload resource:')
    resource = resource_instance.create_resource('../worker/text-preparation-worker/test/src/test-files/pdf/text_generator.pdf')
    print(resource)

    print('Assign resource to training:')
    training_resource = training_instance.assign_resource_to_training(
        project.uuid, training.version,
        resource_reference_object=ResourceReferenceObject(resource_uuid=resource.uuid))
    print(training_resource)

    print('Start training:')
    started_training = training_instance.start_training_by_version(
        project.uuid, training.version)
    print(started_training)

    training_session = training_instance.get_training_by_version(
        project.uuid, training.version)

    last_status = training_session.status
    print('Training status: ', last_status)

    while last_status != TrainingStatus.Training_Success and last_status != TrainingStatus.Training_Failure:
        if training_session.status != last_status:
            print('Training status: ', last_status)
            last_status = training_session.status
    
        time.sleep(5)

    if last_status != TrainingStatus.Training_Success:
        exit(1)

    print('Start decoding:')
    decode_session = decode_api_instance.start_decode(project.uuid, training.version, '')
    print(decode_session)

    while not decode_session.transcripts:
        time.sleep(5)

        decode_session = decode_api_instance.get_decode_result(
            project.uuid, training.version, decode_session.uuid)

    print(decode_session)
