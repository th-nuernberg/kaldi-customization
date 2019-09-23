from connector import *
from models import Decoding, DecodingStateEnum

import json


decode_status_mapping = {
    DecodeStatusCode.IN_PROGRESS: DecodingStateEnum.Decoding_InProgress,
    DecodeStatusCode.FAILURE: DecodingStateEnum.Decoding_Failure,
    DecodeStatusCode.SUCCESS: DecodingStateEnum.Decoded
}


def handle_decode_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    status = DecodeStatus(**msg_data)

    db_decoding = db_session.query(Decoding).filter_by(uuid=status.decode_uuid).first()

    if not db_decoding:
        print('[Error] Received invalid decode_uuid from decode')
        return

    try:
        db_decoding.status = decode_status_mapping[status.id]
    except KeyError:
        print('[Error] Received invalid status id from kaldi')
        return

    db_decoding.transcripts = json.dumps(status.transcripts)

    db_session.add(db_decoding)
    db_session.commit()

    # TODO: handle callback
