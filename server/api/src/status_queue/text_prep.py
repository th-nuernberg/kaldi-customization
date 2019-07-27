from models import Resource, ResourceStateEnum, ResourceTypeEnum

def handle_text_prep_status(msg_data, app, db):
    '''
    Handle a status message from a text preparation worker.
    '''
    if msg_data['text'] == 'failure':
        error_message = str(msg_data['msg']) if "msg" in msg_data else "-"
        print('[Status] ERROR: Failure at Text-Prep-Worker: {}'.format(error_message))
    else:
        # handle bug in current implementation of the text-prep-worker
        # resource_id '4711' is like '4711/4711'
        if '/' in msg_data['text']:
            resource_uuid = (msg_data['text'].split('/'))[0]
        else:
            resource_uuid = msg_data['text']
        
        try:
            with app.app_context():
                this_resource = db.query(Resource).filter_by(uuid=resource_uuid).first()
        except Exception as e:
            print('[Status] WARN: did not found resource in db: {}'.format(resource_uuid))
            print("[Status] Exception at status queue: {}".format(type(e).__name__))
            print("[Status] Further information 1: " + e.__str__())
            print("[Status] Further information 2: " + str(e))
            return
            
        print('[Status] found resource in db: ' + this_resource.__repr__())
        try:
            resource_status = ResourceStateEnum(msg_data['status'])
            print("[Status] resource status: " + ResourceStateEnum.status_to_string(resource_status))
        except ValueError as e:
            print("[Status] WARN: status is not valid! " + str(e))
            resource_status = ResourceStateEnum.TextPreparation_Failure
        
        this_resource.status = resource_status
        print('[Status] after update: ' + this_resource.__repr__())
        with app.app_context():
            db.session.add(this_resource)

        if resource_status == ResourceStateEnum.Success:
            # add new db entry for g2p resource file
            try:
                #TODO handle corpus and uwl!
                with app.app_context():
                    db_resource = Resource(model=this_resource.model,
                                            name=this_resource.name,
                                            resource_type=ResourceTypeEnum.unique_word_list,
                                            status=ResourceStateEnum.G2P_Ready)
                print('[Status] added db entry for g2p resource file: ' + db_resource.__repr__())
                with app.app_context():
                    db.session.add(db_resource)
            except Exception as e:
                print("[Status] ERROR: Error at adding entry for g2p!")
                raise e

        with app.app_context():
            db.session.commit()
            db.session.close()
