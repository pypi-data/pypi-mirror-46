import logging

class StorageModel:
  def __init__(self):
    self.data = {}

  def add(self, project_id, item):
    logging.debug('storage.add:(%s)' % project_id)
    self.data[project_id] = item

  def delete(self, project_id):
    logging.debug('storage.delete:(%s)' % project_id)
    if project_id in self.data:
      del self.data[project_id]
      return True, 'ok'
    else:
      msg = 'project_id(%s) is not exist in storage model' % project_id
      logging.info(msg)
      return False, msg

  def is_valid(self, project_id, storage_secret_key):
    if project_id not in self.data:
      return False
    item = self.data[project_id]
    if item['storage_secret_key'] != storage_secret_key:
      return False
    return True

  def detail(self, project_id):
    if project_id in self.data:
      return self.data[project_id]
    return {}

