# Text-Preparation-Worker

This README-file will provide all necessary information about the Text-Preparation-Worker (**TPW**).

## Functionality and Workflow of the TPW

This section will describe the functionality of the **TPW**. This is done by explaining the workflow of this worker. With this explanation, the following questions will be answered:

1. What does the **TPW** do?
2. What kind of files does the **TPW** need?
3. What kind of files does the **TPW** produce?
4. Which MinIO-buckets does the **TPW** use?

At the end of this section, there is an image of the workflow.

Main goal of the **TPW** is to create a **corpus.txt** file which is afterwards needed by the **data-preparation-worker**. How the **corpus.txt** file is generated is now explained.

Before the actual processing is explained, it is necessary to know that the **TPW** is attached to the `text_prep_queue` and is waiting for a task. As soon as a task is placed within the `text_prep_queue`, the **TPW** is triggered.

In order to process a task correctly, the following information needs to be provided:

1. `resource_uuid`
2. `file_type`

If the received task is valid, the **TPW** starts to process the task.

The first important processing step is to download the needed file which is located within the `RESOURCE_BUCKET` of the MinIO-server.

The needed file is saved within the MinIO-server with the following path: `RESOURCE_BUCKET/resource_uuid/source`

After downloading the needed file, it is necessary to check whether the given `file_type` is supported or not. If the `file_type` is supported, its corresponding parser function is called and the processing continues. If the `file_type` is not supported, the API-server will be updated that the received task contained an unsupported `file_type`.

The following file types are supported by the **TPW**:

1. PDF
2. HTML
3. PNG
4. JPG
5. txt
6. docx

All the parsers are doing one thing. They try to retrieve all the text out of the downloaded file. After the text is retrieved, the **corpus.txt** file is created.

The structure of the **corpus.txt** file will not be explained within this README-file, because this is part of the **kaldi-worker** README.

After creating the **corpus.txt** file, it is uploaded within the `RESOURCE_BUCKET` of the MinIO-server.

The path which is used for uploading the **corpus.txt** file looks as follows:
`RESOURCE_BUCKET/resource_uuid/corpus.txt`

After uploading the **corpus.txt** file, the processing of the task finished officially.

[Sequence diagram of the Text-Preparation-Worker](https://git.informatik.fh-nuernberg.de/kaldi/kaldi-customization/blob/master/worker/text-preparation-worker/tpwsequenz.png)  
[Image of the Text-Preparation-Worker workflow](https://git.informatik.fh-nuernberg.de/kaldi/kaldi-customization/blob/master/worker/text-preparation-worker/tpwablauf.png)

## Structure of the TPW directory

The structure of the **TPW** is quite simple. On the top level there are three subdirectories, a Dockerfile and a requirements.txt file.

Looking at the Dockerfile, this file is actually used by the docker-compose to start the **TPW**.

Within the requirements.txt file all needed Python libraries are defined. In order to test the **TPW** properly, it is recommended to install all libraries which are defined within the requirements.txt file locally.

In order to install the libraries execute one of the following commands (Unix/Linux environment):

1. `sudo pip install -r requirements.txt`
2. `sudo pip3 install -r requirements.txt`

### out-directory

This subdirectory contains all test-files which were used to test the functionality of the **TPW**.

At the beginning of this project, all of these files were used. Currently, only one file of each type is used to test the functionality. More information about testing is provided within the `test` section.

### src-directory

This subdirectory contains the complete implementation of the **TPW**. `text_preparation.py`-file contains the implementation of the workers workflow. The `file_parser.py`-file contains the implementation of all parsers and the **corpus.txt** creation.

### test-directory

This subdirectory contains the test environment for the **TPW**. Therefore, it consits of an own `docker-compose.yml`-file which defines the environment.

In addition to the `docker-compose.yml`-file, a `Dockerfile` is available. This `Dockerfile` creates the **test_text_preparation_worker** which is used to test the **TPW**.

The implementation of all tests is located within the *src* directory.

In order to test the **TPW**, the following commands need to be executed, assuming you are at the top level of the **TPW**:

1. `cd test`
2. `docker-compose up --build`

**Before** executing these commands, make sure that all environmental variables are set. An explanation on how to set the environmental variables for this project can be found within the main README-file of this repository.
