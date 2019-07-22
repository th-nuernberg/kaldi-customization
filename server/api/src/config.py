import secrets
import redis
from minio import Minio

def more_args(parser):
    # webserver
    parser.add_argument(
        '--host', default='0.0.0.0',
        help='host name/address of webserver [default: 0.0.0.0]'
    )
    parser.add_argument(
        '--port', type=int, default=5000,
        help='port of webserver host [default: 5000]'
    )
    parser.add_argument(
        '--secret-key', default=secrets.token_urlsafe(16),
        help='secret key for user authentication [default is random]'
    )

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

redis_client = redis.Redis(host='redis', port=6379, password='kalditproject')

# Import and configure MinIO
minio_client = Minio(
    'minio:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False
)
