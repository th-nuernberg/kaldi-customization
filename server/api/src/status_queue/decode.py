from connector import *
from models import Decoding, DecodingStateEnum, DecodingAudio, AudioResource

import json
from .requests_util import make_async_request


decode_status_mapping = {
    DecodeStatusCode.IN_PROGRESS: DecodingStateEnum.Decoding_InProgress,
    DecodeStatusCode.SUCCESS: DecodingStateEnum.Decoding_Success,
    DecodeStatusCode.FAILURE: DecodingStateEnum.Decoding_Failure
}


def handle_decode_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    status = DecodeStatus(**msg_data)

    db_decoding_session = db_session.query(Decoding).filter_by(uuid=status.decode_uuid).first()

    if not db_decoding_session:
        print('[Error] Received invalid decode_uuid from decode')
        return

    try:
        db_decoding_session.status = decode_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from decode')
        return

    if(db_decoding_session.callback != "{}"):
        callback = json.loads(db_decoding_session.callback)
        print("Preparing callback")
        make_async_request(method=callback["method"], url=callback["url"], data=str(db_decoding_session))

    #read all transcripts and write them to database
    for key in status.transcripts:
        audio = AudioResource.query.filter_by(uuid=key).first()
        decoding_audio = DecodingAudio.query.filter_by(audioresource_id=audio.id,decoding_id=db_decoding_session.id).first()
        decoding_audio.transcripts = json.dumps(status.transcripts[key])
        db_session.add(decoding_audio)
        db_session.commit()

    db_session.add(db_decoding_session)
    db_session.commit()
