from bootstrap import db
from .resource import *
from .project import *
from .acousticmodel import *
from .file import *
from .language import *
from .user import *


db.drop_all()
db.create_all()

from sqlalchemy import inspect
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
            