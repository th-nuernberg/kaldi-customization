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
from socket_server import socketio

connex_app = connexion.FlaskApp(__name__, specification_dir='openapi_server/openapi',  options={
    'swagger_ui': True
})
connex_app.add_api('openapi.yaml', pythonic_params=True, resolver=connexion.resolver.RestyResolver('api'))

app = connex_app.app
app.json_encoder = encoder.JSONEncoder


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
    socketio.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/api')

    start_status_queue_handler(app, db)

    connex_app.run(host=conf.host, port=conf.port, debug=conf.verbose)
