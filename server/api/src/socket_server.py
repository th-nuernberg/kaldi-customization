import connexion
import functools

from flask_socketio import SocketIO, send, emit


socketio = SocketIO(async_mode='gevent')


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not connexion.context or not connexion.context['token_info']['user']:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('secret_message')
@authenticated_only
def handle_secret_message(message):
    print('secret message: ' + message)
