from models import Resource, FileStateEnum, FileTypeEnum


def handle_text_prep_status(msg_data, db):
    '''
    Handle a status message from a text preparation worker.
    '''
    if msg_data['text'] == 'failure':
        print('Status: ERROR: Failure at Text-Prep-Worker: ')
        if "msg" in msg_data:
            print("Status: ERROR: Error message: " + msg_data['msg'])
    else:
        this_resource = Resource.query.filter_by(name=msg_data['text']).first()
        if this_resource is not None:
            print('Status: found resource in db: ' + this_resource.__repr__())
            try:
                resource_status = FileStateEnum(msg_data['status'])
                print("Status: resource status: " + FileStateEnum.status_to_string(resource_status))
            except ValueError as e:
                print("Status: WARN: status is not valid!")
                print(e)
                resource_status = FileStateEnum.TextPreparation_Failure
            
            this_resource.status = resource_status
            print('Status: after update: ' + this_resource.__repr__())
            db.session.add(this_resource)

            if resource_status == FileStateEnum.Success:
                # add new db entry for g2p resource file
                try:
                    #TODO handle corpus and uwl!
                    db_resource = Resource(model=this_resource.model,
                                            name=this_resource.name,
                                            resource_type=FileTypeEnum.unique_word_list,
                                            status=FileStateEnum.G2P_Ready)
                    print('Status: added db entry for g2p resource file: ' + db_resource.__repr__())
                    db.session.add(db_resource)
                except Exception as e:
                    print("Status: ERROR: Error at adding entry for g2p!")
                    raise e

            db.session.commit()
            db.session.close()
        else:
            print('Status: WARN: did not found resource in db: ' + msg_data['text'] + '!')
