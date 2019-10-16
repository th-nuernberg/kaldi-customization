# Kaldi Customization Frontend

Tasks:
- graphical user interface to use Kaldi
- user can create projects to start a training and a decode to transform audio to text
- user can register, login or logoff off
- displayed elements are related to one user

## Structure

- e2e
- projects/swagger-client - interface to API functions
- src - holds front end components to display features, functions and data

## Components

- _guards
- _services
- cover
- dashboard
- login
- project
- register
- upload

#### _guards

The guards folder contains functionality for the authentication guard.

#### _services

The services folder contains support functions and features for authentication, language type mapping, status code mapping and type code mapping.

#### cover

The cover defines the behavior and look of the cover page.
It displays the license information and the project information.

#### dashboard

The dashboard defines the behavior and look of the dashboard page.
The dashboard shows an overview of all existing projects of the logged in user.
The projects are order to their creation time. The latest project is on top.
Each project is represented as a tile with the information of: project name, acoustic model, last training with creation date and route to training.
The dashboard allows to create a new project by entering a project name and selecting an existing acoustic model.
The dashboard allows to open an existing project.
The dashboard allows to create a new training or to open the latest created training.

#### login

The login defines the behavior and look of the login page.
The user can log into the Kaldi Customization front end to use functions of Kaldi by entering the email address and the password.
The login allows a not registered user to create a new account.


#### project

The project defines the behavior and look of the project page.
The project displays an overview of all existing training sessions and decoding sessions.
The project allows to create a new training session.

All training sessions are represented in a list.
Each training shows the training version, the training status and allows, if the training was successful, to create a decoding session and to download the created graphs of the training.

All decode sessions are represented in a expansion panel.
Each decoding session is related to a training and shows the decoded audio files with the transformed transcripts.
The audio file can be played.
The transcripts can be copied to clipboard or downloaded in a text file.

It is only possible to create a decoding session of a training, if no decoding session is already active! (One decoding session for a training at a time)

#### register

The register defines the behavior and look of the register page.
A user can register to the front end by entering a user name, an email address and a password.
The register automatically creates a new user account with authentication.

#### upload/decoding

The decoding defines the behavior and look of the decoding page.
The decoding page supports the user to upload a new audio file or copy an already existing audio file to the decoding session.
The user can see all copied and uploaded audio files in a list.
Each audio file can be played in a media player to check if everything is fine.
Before the decoding starts, the user sees an overview of all data of the decoding session.
Start decode executes the decoding process of Kaldi and forwards the user to the decoding overview page.

##### upload/decoding/overview

The decoding overview page defines the behavior and look of the decoding overview page.
The decoding overview page displays the data of a running or successful decoding session.
The overview displays the project name, acoustic model, acoustic model type, model language, training version, training status, decoding status, creation date, number of decoded audio files and each audio file with the audio name, audio status and the transcript-ed text.
Each audio file can be played and the transcript-ed text can be copied to clipboard or downloaded as a text file.

For more information it is possible to download the log of the decoding session.

#### upload/training
The training page defines the behavior and look of the training page.
The training page supports the user to upload a new resource file or copy and already existing resource file to the training session.
The user can see all all copied or uploaded resource files in list.
Each resource shows the corpus content in a text area.
Before the training starts, the user sees an overview of all data of the training session.
Start decode executes the training process of Kaldi and forwards the user to the training overview page.

##### upload/training/overview
The training overview page defines the behavior and look of the training overview page.
The training overview page displays all data of a running, successful or failed training session.
The overview displays the project name, acoustic model, acoustic model type, model language, training version, creation date, training status, number of resources and each resource file with the resource name, resource type, resource status and the possibility to download the log of the resource.

The training overview page also shows statistic values about the training like: number of resources, number of text lines, number of words and number of unique words.
The training overview page shows all unique words in a text area.

For more information it is possible to download the log of the data preparation and training.
