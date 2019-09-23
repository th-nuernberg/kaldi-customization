import importlib.machinery
importlib.machinery.SourceFileLoader('minio_communication','shared/minio_communication.py').load_module()

from minio_communication import *

importlib.machinery.SourceFileLoader('models','server/api/src/models/__init__.py').load_module()
from models import *

import minio
import logging

from flask import Flask

MINIO_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
MINIO_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

MYSQL_USER="api"
MYSQL_PASSWORD="api-server-password"
MYSQL_DATABASE="api"


minio_client = minio.Minio("localhost:9001",access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=False)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, "127.0.0.1", 3307, MYSQL_DATABASE)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['SQLALCHEMY_POOL_RECYCLE'] = 50

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    german = Language(name="German")
    db.session.add(german)

    english = Language(name="English")
    db.session.add(english)

    Voxforge_RNN = AcousticModel(name='Voxforge-RNN', language=german, model_type=ModelType.HMM_RNN)
    db.session.add(Voxforge_RNN)

    db.session.commit()
    db.session.close()

'''Create buckets if they do not exist'''
for bucket_name in minio_buckets.values():
    try:
        minio_client.make_bucket(bucket_name)
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.error.ResponseError as e:
        raise e


voxfore_rnn_id = 1
#UPLOAD MODELS
# Voxforge-RNN
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/model.zip"  , "initialization/acoustic-models/voxforge-rnn/model.zip")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/final.mdl"  , "initialization/acoustic-models/voxforge-rnn/final.mdl")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/lexicon.txt"  , "initialization/acoustic-models/voxforge-rnn/lexicon.txt")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/tree"  , "initialization/acoustic-models/voxforge-rnn/tree")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/phones.txt"  , "initialization/acoustic-models/voxforge-rnn/phones.txt")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/g2p_model.fst"  , "initialization/acoustic-models/voxforge-rnn/g2p_model.fst")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/cmvn_opts"  , "initialization/acoustic-models/voxforge-rnn/cmvn_opts")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.dubm"  , "initialization/acoustic-models/voxforge-rnn/extractor/final.dubm")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie"  , "initialization/acoustic-models/voxforge-rnn/extractor/final.ie")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie.id"  , "initialization/acoustic-models/voxforge-rnn/extractor/final.ie.id")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.mat"  , "initialization/acoustic-models/voxforge-rnn/extractor/final.mat")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/global_cmvn.stats"  , "initialization/acoustic-models/voxforge-rnn/extractor/global_cmvn.stats")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/online_cmvn.conf"  , "initialization/acoustic-models/voxforge-rnn/extractor/online_cmvn.conf")
upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/splice_opts"  , "initialization/acoustic-models/voxforge-rnn/extractor/splice_opts")
