import logging

from dsms.model.project_model import ProjectModel
from dsms.util import get_full_id


class ProjectController:
  def __init__(self, center_controller, auth_model):
    self.center_controller = center_controller
    self.auth_model = auth_model
    self.model = ProjectModel()

  def _create(self, project_id, user):
    logging.debug('create')
    token = get_full_id()
    self.model.add(project_id, token, [user])
    return token

  def get_config(self, project_id):
    if project_id in self.model.data:
      return self.model.data[project_id]
    return None

  def get_projects(self):
    logging.debug('get_projects')
    return self.model.data

  def _is_project_exist(self, project_id):
    if project_id in self.model.data:
      return True
    return False

  def create_or_append(self, project_id, user):
    logging.debug('create_or_append: %s, %s' % (project_id, user))
    if not self._is_project_exist(project_id):
      token = self._create(project_id, user)
    else:
      project = self.model.data[project_id]
      users = project['users']
      if user not in users:
        users.append(user)
      token = project['token']
    self.auth_model.register(token)
    return token

  def delete(self, project_id):
    return self.model.remove(project_id)
