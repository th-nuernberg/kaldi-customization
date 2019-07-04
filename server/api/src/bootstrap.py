# Import and configure Flask / DB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://api:api-server-password@db:3306/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['SQLALCHEMY_POOL_RECYCLE'] = 50
db = SQLAlchemy(app)

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

# Import and configure Redis
import redis
redis_conn = redis.Redis(host='redis', port=6379, password='kalditproject')

# Import and configure MinIO
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

minioClient = Minio('minio:9000',
                    access_key='AKIAIOSFODNN7EXAMPLE',
                    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                    secure=False)

# Bucket definitions
# files for the text-prep-worker
TEXTS_IN_BUCKET = 'texts-in'

# unique word list
TEXTS_OUT_BUCKET = 'texts-out'
# some other files
#TEXTS_OUT_BUCKET = 'texts-out'

# Create buckets if they not exist
try:
    minioClient.make_bucket(TEXTS_IN_BUCKET)
except BucketAlreadyOwnedByYou as err:
    pass
except BucketAlreadyExists as err:
    pass
except ResponseError as err:
    raise

try:
    minioClient.make_bucket(TEXTS_OUT_BUCKET)
except BucketAlreadyOwnedByYou as err:
    pass
except BucketAlreadyExists as err:
    pass
except ResponseError as err:
    raise
