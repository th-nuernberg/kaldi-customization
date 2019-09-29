# Data-Preparation-Worker

This README-file will provide all necessary information about the Data-Preparation-Worker (**DPW**).

## Functionality and Workflow of the DPW

This section will describe the functionality of the **DPW**. This is done by explaining the workflow of this worker. With this explanation, the following questions will be answered:

1. What does the **DPW** do?
2. What kind of files does the **DPW** need?
3. What kind of files does the **DPW** produce?
4. Which MinIO-buckets does the **DPW** use?

At the end of this section, there is an image of the workflow.

Main goal of the **DPW** is to create a **lexicon.txt** file which is afterwards needed by the **kaldi-worker**. A **lexicon.txt** file contains information about words and their phones. In order to retrieve the phones for a word, the Phonetisaurus is executed.

Before the actual processing is explained, it is necessary to know that the **DPW** is attached to the `data_prep_queue` and is waiting for a task. As soon as a task is placed within the `data_prep_queue`, the **DPW** is triggered.

In order to process a task correctly, the following information needs to be provided:

1. `training_id`
2. `resources`
3. `acoustic_model_id`

If the received task is valid, the **DPW** starts to process the task.

The first important processing step is to download all needed files which are located within the `ACOUSTIC_MODEL_BUCKET` and the `TRAINING_RESOURCE_BUCKET` of the MinIO-server.

The following files need to be downloaded from the `ACOUSTIC_MODEL_BUCKET`:

1. `ACOUSTIC_MODEL_BUCKET/acoustic_model_id/g2p_model.fst`
2. `ACOUSTIC_MODEL_BUCKET/acoustic_model_id/lexicon.txt`

The following files need to be downloaded from the `TRAINING RESOURCE_BUCKET`:

1. `TRAINING_RESOURCE_BUCKET/resource/corpus.txt`

**Important note**: The `resource`-field contains a list of resources and each resource has one **corpus.txt**-file which needs to be downloaded.


After successfully downloading every needed file, all corpus-files are merged into one.

As soon as this step finishes, the merged corpus is saved locally. In addition to that, the merged corpus is used to retrieve all words from its text. These words are saved within a list. Every word within this list occurs exactly once.

After creating the word list, this list is compared with all words from the downloaded **lexicon.txt**-file. Each word that appears within the word list and not within the lexicon.txt list is used for further processing.

Therefore, after comparing both lists, every word which is new for the **lexicon.txt**-file is stored within a new list. This list is called `unique_word_list`.

The `unique_word_list` is saved locally, before the processing continues. As soon as the `unique_word_list` is saved locally, this list is used with the Phonetisaurus in order to retrieve the phones for each word.

After executing the **Phonetisaurus** the words of the `unique_word_list` and their phones are appended to the downloaded **lexicon.txt**-file.

Finally, all files which are needed for further processing are uploaded into the `TRAINING_BUCKET` of the MinIO-server.

The following files are saved:

1. `TRAINING_BUCKET/training_id/lexicon.txt`
2. `TRAINING_BUCKET/training_id/corpus.txt`
3. `TRAINING_BUCKET/training_id/unique_word_list.txt`

**INSERT SEQUENCE DIAGRAM FOR THE DPW**  
**INSERT WORKFLOW FOR THE DPW**

## Structure of the DPW directory

The structure of the **DPW** is quite simple. On the top level there are two subdirectories, a Dockerfile and a requirements.txt file.

Looking at the Dockerfile, this file is actually used by the docker-compose to start the **DPW**.

Within the requirements.txt file all needed Python libraries are defined. In order to test the **DPW** properly, it is recommended to install all libraries which are defined within the requirements.txt file locally.

In order to install the libraries execute one of the following commands (Unix/Linux environment):

1. `sudo pip install -r requirements.txt`
2. `sudo pip3 install -r requirements.txt`

### src-directory

This subdirectory contains the complete implementation of the **DPW**. The `data_preparation.py`-file contains the implementation of the workers workflow. The `data_processing.py`-file implements all functions which are used for processing a **DPW** task.

### test-directory

This subdirectory contains the test environment for the **DPW**. Therefore, it consits of an own `docker-compose.yml`-file which defines the environment.

In addition to the `docker-compose.yml`-file, a `Dockerfile` is available. This `Dockerfile` creates the **test_data_preparation_worker** which is used to test the **DPW**.

The implementation of all tests is located within the *src* directory.

In order to test the **DPW**, the following commands need to be executed, assuming you are at the top level of the **DPW**:

1. `cd test`
2. `docker-compose up --build`

**Before** executing these commands, make sure that all environmental variables are set. An explanation on how to set the environmental variables for this project can be found within the main README-file of this repository.
