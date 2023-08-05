import logging

from dsms.util import set_project_config, get_project_config
from dsms.sdk import Api


class ProjectCommand:
  def create(self, project_id, user_id):
    logging.debug('create')
    res = Api.post('project', {
      'project_id': project_id,
      'user_id': user_id,
    })
    data = res.json()
    logging.info(data)
    set_project_config(project_id, data)

  def delete(self, project_id):
    logging.debug('delete')
    c = get_project_config()[project_id]
    print(c)
    if not c:
      logging.error('No project config (%s)' % project_id)
      return
    res = Api.delete('project', c)
    data = res.json()
    logging.info(data)

  def ls(self):
    logging.debug('ls')
    res = Api.get('projects')
    logging.info(res.json())

  def detail(self, project_id):
    logging.debug('detail')
    c = get_project_config()[project_id]
    token = c['token']
    data = {
      'project_id': project_id,
      'token': token
    }
    res = Api.post('project/detail', data=data)
    print('res detail:', res.json())

  def get(self, project_id):
    data = Api.get_project_config(project_id)
    print(data)
    set_project_config(project_id, data)
