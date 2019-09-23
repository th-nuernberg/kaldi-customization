import connexion
import six
import redis
import json
import config

from openapi_server.models.acoustic_model import AcousticModel
from openapi_server.models.acoustic_model_type import AcousticModelType
from openapi_server.models.create_project_object import CreateProjectObject  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.models.project_creation import ProjectCreation  # noqa: E501
from openapi_server.models.training_status import TrainingStatus  # noqa: E501
from openapi_server import util

from models import db, Project as DB_Project, TrainingStateEnum as DB_TrainingStateEnum, User as DB_User, AcousticModel as DB_AcousticModel

from mapper import mapper


def create_project(project=None):  # noqa: E501
    """Create a new project

     # noqa: E501

    :param project: Project object that needs to be created
    :type project: dict | bytes

    :rtype: Project
    """
    if connexion.request.is_json:
        project = ProjectCreation.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return ('Invalid input', 405)

    current_user = connexion.context['token_info']['user']

    # Resolve acoustic model
    db_acousticModel = DB_AcousticModel.query.filter_by(
        uuid=project.acoustic_model).first()

    if not db_acousticModel:
        return ("Acoustic Model not found", 404)

    # Resolve optional parent project
    db_parent_proj = None
    if project.parent is not None:
        db_parent_proj = DB_Project.query.filter_by(
            uuid=project.parent, owner_id=current_user.id).first()
        if db_parent_proj is None:
            return ("Parent project not found", 404)

    db_proj = DB_Project(
        name=project.name,
        owner=current_user,
        acoustic_model=db_acousticModel
    )

    if db_parent_proj is not None:
        db_proj.parent = db_parent_proj

    db.session.add(db_proj)
    db.session.commit()

    return mapper.db_project_to_front(db_proj)


def get_project_by_uuid(project_uuid):  # noqa: E501
    """Find project by UUID

    Returns a single project # noqa: E501

    :param project_uuid: UUID of project to return
    :type project_uuid: 

    :rtype: Project
    """
    current_user = connexion.context['token_info']['user']

    db_proj = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if (db_proj is None):
        return ("Project not found", 404)

    return mapper.db_project_to_front(db_proj)


def get_projects():  # noqa: E501
    """Returns a list of available projects

     # noqa: E501


    :rtype: List[Project]
    """
    current_user = connexion.context['token_info']['user']

    db_projects = DB_Project.query.filter_by(owner_id=current_user.id).all()

    return [mapper.db_project_to_front(db_proj) for db_proj in db_projects]
