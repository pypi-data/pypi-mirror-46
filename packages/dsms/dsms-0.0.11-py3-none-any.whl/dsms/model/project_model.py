import logging


class ProjectModel:
  def __init__(self):
    self.data = {}

  def add(self, project_id, token, users):
    logging.debug('project.add:(%s)' % project_id)
    self.data[project_id] = {
      'project_id': project_id,
      'token': token,
      'users': users,
    }

  def remove(self, project_id):
    logging.debug('project.remove:(%s)' % project_id)
    if project_id in self.data:
      del self.data[project_id]
      return True, 'ok'
    else:
      msg = 'project_id(%s) is not exist in project model' % project_id
      logging.info(msg)
      return False, msg
