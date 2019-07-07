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
# text-prep-worker
TEXTS_IN_BUCKET  = 'texts-in'
TEXTS_OUT_BUCKET = 'texts-out'

# G2P-worker
G2P_IN_BUCKET  = 'g2p-in'
G2P_OUT_BUCKET = 'g2p-out'

# kaldi-worker
KALDI_IN_BUCKET  = 'kaldi-in'
KALDI_OUT_BUCKET = 'kaldi-out'

def createMinioBucket(minio_client, bucket_name):
    '''
    Create the given bucket if it does not exist.
    '''
    try:
        minio_client.make_bucket(bucket_name)
    except BucketAlreadyOwnedByYou:
        pass
    except BucketAlreadyExists:
        pass
    except ResponseError as e:
        raise e

# Create buckets if they not exist
createMinioBucket(minio_client=minioClient, bucket_name=TEXTS_IN_BUCKET)
createMinioBucket(minio_client=minioClient, bucket_name=TEXTS_OUT_BUCKET)
createMinioBucket(minio_client=minioClient, bucket_name=G2P_IN_BUCKET)
createMinioBucket(minio_client=minioClient, bucket_name=G2P_OUT_BUCKET)
createMinioBucket(minio_client=minioClient, bucket_name=KALDI_IN_BUCKET)
createMinioBucket(minio_client=minioClient, bucket_name=KALDI_OUT_BUCKET)
