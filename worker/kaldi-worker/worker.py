#!/usr/bin/python
import os
import shutil
import redis_config
import json
import subprocess

from connector import *
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets


acoustic_model_bucket = minio_buckets['ACOUSTIC_MODELS_BUCKET']
training_bucket = minio_buckets["TRAINING_BUCKET"]

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')
base_model_path = os.path.join(workspace_path, 'base-model.zip')

lexicon_path = os.path.join(workspace_path, 'lexicon.txt')
corpus_path = os.path.join(workspace_path, 'corpus.txt')
acoustic_model_folder = os.path.join(script_root_path, "acc_models")

downloaded_acoustic_models = set()
if os.path.exists(acoustic_model_folder):
    shutil.rmtree(acoustic_model_folder)
os.makedirs(acoustic_model_folder)



def finish_logging(log_file_handler, minio_client, task):
    log_file_handler.close()
    logfile_result = upload_to_bucket(minio_client, minio_buckets["LOG_BUCKET"], "kaldi_worker/{}/{}".format(task.training_id, "log.txt"), "/log.txt")
    if not logfile_result[0]:
        print("An error occurred during the upload of the logfile.")
    print("Logfile was successfully uploaded")


if __name__ == "__main__":
    try:
        conf, tasks, status_queue, minio_client = parse_args(
            'Kaldi Worker Connector', task_queue=redis_config.redis_queues["KALDI_QUEUE"])

        for task in tasks.listen():
            print("Received the following task from Kaldi-Queue:")
            print(task)

            task = KaldiTask(**task)

            log_file_handler = open("/log.txt", "w")
            log_file_handler.write("Starting to process the received task \n")
            log_file_handler.write("{}\n".format(task))

            if not os.path.exists(acoustic_model_folder):
                os.makedirs(workspace_path)
                log_file_handler.write("Workspace directory did not exist. Therefore, the needed directory was created. \n")
            log_file_handler.write("Workspace directory already exists. Processing continues. \n")


            # cache models when used once and reduce download
            try:
                log_file_handler.write("Starting to download all needed files from the corresponding MinIO-bucket! \n")
                cur_acoustic_model_path = os.path.join(acoustic_model_folder, str(task.acoustic_model_id))
                phone_symbol_table = os.path.join(cur_acoustic_model_path,"phones.txt")
                if task.acoustic_model_id not in downloaded_acoustic_models:
                    os.makedirs(cur_acoustic_model_path)
                    download_from_bucket(minio_client, acoustic_model_bucket, "{}/final.mdl".format(task.acoustic_model_id), os.path.join(cur_acoustic_model_path, "final.mdl"))
                    download_from_bucket(minio_client, acoustic_model_bucket, "{}/tree".format(task.acoustic_model_id), os.path.join(cur_acoustic_model_path, "tree"))
                    download_from_bucket(minio_client, acoustic_model_bucket, "{}/phones.txt".format(task.acoustic_model_id), phone_symbol_table)

                    downloaded_acoustic_models.add(task.acoustic_model_id)

                # load resources
                download_from_bucket(minio_client, training_bucket, "{}/lexicon.txt".format(task.training_id), lexicon_path)
                download_from_bucket(minio_client, training_bucket, "{}/corpus.txt".format(task.training_id), corpus_path)
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to download all needed files for this worker, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("At least one download failed! It is not possible to retrieve all needed files. Therefore, the task fails!\n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(KaldiStatus(id=KaldiStatusCode.FAILURE, training_id=task.training_id))
            log_file_handler.write("Successfully downloaded all needed files! \n")

            # train resources
            try:
                log_file_handler.write("Processing continues by creating a new graph with the given training resources! \n")
                new_graph_dir = os.path.join(script_root_path, "new_graph")
                os.chdir("/opt/kaldi/scripts/")
                subprocess.call("/opt/kaldi/scripts/create_new_graph.sh {} {} {} {} {} {}".format(lexicon_path, corpus_path,
                                                                                          cur_acoustic_model_path, new_graph_dir, workspace_path, phone_symbol_table), shell=True)
                os.chdir("/")
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to create the new graph an error occurred. \n")
                log_file_handler.write("Therefore, it was not possible to create a new graph for this training. That means this task failed! \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(KaldiStatus(id=KaldiStatusCode.FAILURE, training_id=task.training_id))
            log_file_handler.write("Successfully created a new graph with the given training resources!\n")

            # Upload new model
            try:
                log_file_handler.write("Starting to compress all files which will be uploaded!\n")
                new_graph_archive = os.path.join(script_root_path, "graph")
                archive_format = "zip"
                shutil.make_archive(base_name=new_graph_archive,
                                    format=archive_format, root_dir=new_graph_dir, base_dir="./")
            except Exception as e:
                print(e)

                log_file_handler.write("While trying to compress all needed files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("Compressing failed! Task failed! \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(KaldiStatus(id=KaldiStatusCode.FAILURE, training_id=task.training_id))
            log_file_handler.write("Successfully compressed files. Ready for upload! \n")

            try:
                log_file_handler.write("Final step: Upload of the ZIP archive into its corresponding MinIO-bucket! \n")
                upload_to_bucket(minio_client, training_bucket, "{}/graph.zip".format(task.training_id), new_graph_archive + "." + archive_format)
            except Exception as e:
                print(e)

                log_file_handler.write("While trying to upload the ZIP archive, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("The upload failed! Therefore, the task failed too! \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)
                status_queue.submit(KaldiStatus(id=KaldiStatusCode.FAILURE, training_id=task.training_id))

            log_file_handler.write("Successfully uploaded the ZIP archive! \n")

            # unload resources
            shutil.rmtree(workspace_path)

            # uploading created log-file
            finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

            # write in status queue
            status_queue.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS, training_id=task.training_id))

    except KeyboardInterrupt:
        shutil.rmtree(acoustic_model_folder)
        shutil.rmtree(workspace_path)
        pass
