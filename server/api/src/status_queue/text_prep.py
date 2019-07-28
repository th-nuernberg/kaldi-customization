from models import Resource, ResourceStateEnum, ResourceTypeEnum

def resolve_ResourceState_from_worker(worker_state):
    if worker_state == 200: # 200 means success
        return ResourceStateEnum.TextPreparation_Success
    
    try:
        resource_status = ResourceStateEnum(worker_state)
    except ValueError as e:
        print("[Status][text-prep] WARN: worker status is not valid! " + str(e))
        resource_status = ResourceStateEnum.TextPreparation_Failure
    return resource_status

def handle_text_prep_status(msg_data, db_session):
    '''
    Handle a status message from a text preparation worker.
    '''
    if msg_data['text'] == 'failure':
        error_message = str(msg_data['msg']) if "msg" in msg_data else "-"
        print('[Status] WARN: Failure at Text-Prep-Worker: {}'.format(error_message))
    else:
        # handle bug in current implementation of the text-prep-worker
        # resource_id '4711' is like '4711/4711'
        if '/' in msg_data['text']:
            resource_uuid = (msg_data['text'].split('/'))[0]
        else:
            resource_uuid = msg_data['text']
        
        try:
            this_resource = db_session.query(Resource).filter_by(uuid=resource_uuid).first()
            db_session.commit()
        except Exception as e:
            print('[Status] WARN: did not found resource in db: {}'.format(resource_uuid))
            print("[Status] Exception at status queue: {}".format(type(e).__name__))
            print("[Status] Further information 1: " + e.__str__())
            print("[Status] Further information 2: " + str(e))
            return
            
        print('[Status] found resource in db: ' + this_resource.__repr__())
        resource_status = resolve_ResourceState_from_worker(msg_data['status'])
        print("[Status] new resource status: " + ResourceStateEnum.status_to_string(resource_status))
        
        this_resource.status = resource_status
        print('[Status] after update: ' + this_resource.__repr__())

        db_session.add(this_resource)
        db_session.commit()
