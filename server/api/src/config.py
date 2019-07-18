minio_buckets = dict(
    # MinIO Bucket definitions
    # text-prep-worker
    TEXTS_IN_BUCKET='texts-in',
    TEXTS_OUT_BUCKET='texts-out',

    # G2P-worker
    G2P_IN_BUCKET  = 'g2p-in',
    G2P_OUT_BUCKET = 'g2p-out',

    # acoustic models that are trained by users
    ACOUSTIC_MODELS_BUCKET  = 'acoustic-models',
    # predefined models and stuff for kaldi like vocabular
    LANGUAGE_MODELS_BUCKET  = 'language-models'
)

def more_args(parser):
    # webserver
    parser.add_argument(
        '--host', default='0.0.0.0',
        help='host name/address of webserver [default: 0.0.0.0]')
    parser.add_argument(
        '--port', type=int, default=5000,
        help='port of webserver host [default: 5000]')

    # db config
    parser.add_argument(
        '--db', default='api',
        help='name of database [default: api]'
    )
    parser.add_argument(
        '--db-type', default='sqlite', choices=('sqlite', 'mysql'),
        help='sqlite of database [default: sqlite]'
    )
    parser.add_argument(
        '--db-host', default='localhost',
        help='host name/address of database [default: localhost]'
    )
    parser.add_argument(
        '--db-port', type=int, default=3306,
        help='port of database [default: 3306]'
    )
    parser.add_argument(
        '--db-user',
        help='user of database'
    )
    parser.add_argument(
        '--db-password',
        help='password for user of database'
    )
