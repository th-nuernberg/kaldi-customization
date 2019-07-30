# Kaldi Customization

***Use the env.cmd or env.sh script in your shell to setup the environment variables for docker-compose!***

* Web Interface: [localhost:8080](http://localhost:8080)
* Web API: [localhost:8080/api](http://localhost:8080/api)

## Requirements
 * [Docker](https://www.docker.com/)
 * [Docker Compose](https://docs.docker.com/compose/)


## Contains

### /server

The server to run the kaldi customization web service.

#### /server/api

This is the api backend. It provides access to the features of the kaldi customization web service and handles authentication.

#### /server/web

This is the web frontend for business users. It offers a user interface to train and test user defined asr.


### /worker

The worker contains the workers used in the backend to process the user requests via the api.

#### /worker/kaldi-worker

This is the general kaldi-worker to process asr training and testing.  
(Could be split into training and testing workers in future)


### Further Docker Images

#### MariaDB Server

A SQL Server for the persistent data.

#### Redis Server

An in memory Redis Server for the task queue.
