import logging
import os

import dsms.sdk as dsdk
from dsms.display import Display
from dsms.sdk import Api
from dsms.util import (
  set_mc_config, set_config, get_diff_list
)
from .admin_command import AdminCommand
from .alarm_command import AlarmCommand
from .bucket_command import BucketCommand
from .project_command import ProjectCommand


class Command:
  def __init__(self):
    self.admin = AdminCommand()
    self.bucket = BucketCommand()
    self.project = ProjectCommand()
    self.alarm = AlarmCommand()

  def _set_mc_config(self):
    logging.debug('_set_mc_config')
    res = Api.post('mc-config')
    data = res.json()
    logging.debug(data)
    set_mc_config(data)

  def init(
        self,
        center_url='http://localhost:30000',
        center_token='my-token'):
    set_config({
      'kind': 'cli',
      'center_url': center_url,
      'center_token': center_token,
    })
    self._set_mc_config()
    logging.info('init finish. check ~/.dsms-config')
    res = Api.post('ping', {})
    logging.info(res)

  def diff(self, project, local='./'):
    dest = 'dcs/%s' % project
    _, _, _, diff_list = get_diff_list(local, dest)
    Display().print_diff_local(diff_list)
    logging.info('diff finish.')

  def pull(self, project, remove=False, local='./'):
    logging.debug('pull')
    src = 'dcs/%s' % project
    dest = local
    remove_option = ''
    if remove:
      remove_option = '--remove'
    command = 'mc mirror --overwrite %s %s %s' % (
      remove_option, src, dest)
    ret = os.system(command)
    if int(ret) == 0:
      logging.info('success')
    else:
      logging.info('fail')
    logging.info('pull finish.')

  def push(self, project, local='./'):
    logging.debug('push')
    logging.info('If it takes long time, check origin network.')
    dest = 'dcs/%s' % project
    src = local
    command = 'mc mirror --overwrite %s %s' % (src, dest)
    ret = os.system(command)
    if int(ret) == 0:
      logging.info('success')
      self.pull(project)
    else:
      logging.info('fail')
    logging.info('push finish.')

  def test_sdk(self):
    sdk = dsdk.Sdk()
    sdk.center(
      os.environ['CENTER_URL'],
      os.environ['CENTER_TOKEN'])
    sdk.project('project1')
    sdk.bucket('bucket1')
    sdk.alarm('alarm1')
    assert sdk.check(), 'sdk is not valid'
    sdk.push('/data/project1/bucket1/')

  def test(self):
    project_id = 'project1'
    alarm_id = 'alarm1'
    res = Api.get('alarm/msg/%s/%s' % (project_id, alarm_id))
    print(res.json())
