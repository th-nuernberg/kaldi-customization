from bootstrap import db
from .resource import Resource, ResourceStateEnum, ResourceTypeEnum
from .project import Project
from .model import Model


db.drop_all()
db.create_all()

# Auto Increment resources.id, start for each model by 1
db.engine.execute('''
CREATE TRIGGER resource_id_counter BEFORE INSERT ON resources
FOR EACH ROW BEGIN
    SET NEW.id = (
       SELECT IFNULL(MAX(id), 0) + 1
       FROM resources
       WHERE model_id  = NEW.model_id
    );
END''')

from sqlalchemy import inspect
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
            