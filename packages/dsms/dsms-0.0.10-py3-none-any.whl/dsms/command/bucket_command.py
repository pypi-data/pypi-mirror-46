import logging

from dsms.display import Display
from dsms.util import get_project_config
from dsms.sdk import Api, assert_project_exist_in_config


class BucketCommand:
  def create(self, project_id, bucket_id):
    logging.debug('create')
    assert_project_exist_in_config(project_id)
    c = get_project_config()
    data = c[project_id]
    data.update({'bucket_id': bucket_id})
    res = Api.post('bucket', data=data)

  def delete(self, project_id, bucket_id):
    logging.debug('delete')
    assert_project_exist_in_config(project_id)
    c = get_project_config()
    data = c[project_id]
    data.update({'bucket_id': bucket_id})
    res = Api.delete('bucket', data=data)

  def ls(self, project_id):
    logging.debug('ls')
    assert_project_exist_in_config(project_id)
    res = Api.get('buckets/%s' % project_id)
    print(res.json())

  def detail(self, project_id, bucket_id):
    logging.debug('detail')
    assert_project_exist_in_config(project_id)
    res = Api.get('buckets/%s/%s' % (project_id, bucket_id))
    Display().print_bucket_detail(res.json(), bucket_id)
