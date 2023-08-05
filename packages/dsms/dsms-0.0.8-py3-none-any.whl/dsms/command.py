import json
import logging
import os
import subprocess

import requests

from .center import run_center
from .display import Display
from .node import run_node
from .util import (
  get_id, set_mc_config, get_config, set_config, run_proc,
  get_diff_list
)


class CommandController:
  def __init__(self):
    self.center_url = ''
    self.center_token = ''
    self.ready = False

  def init(self, center_url, center_token):
    self.center_url = center_url
    self.center_token = center_token
    self.ready = True

  def ensure_ready(self):
    if self.ready:
      return
    config = get_config()
    self.init(config['center_url'], config['center_token'])


controller = CommandController()


class Api:
  @staticmethod
  def post(path, data={}):
    controller.ensure_ready()
    url = controller.center_url
    token = controller.center_token
    headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Authorization': 'bearer %s' % token
    }
    data['tid'] = get_id()
    cookies = {'session_id': 'sorryidontcare'}
    url = url + '/' + path
    res = requests.post(
      url,
      headers=headers,
      cookies=cookies,
      data=json.dumps(data))
    if res.status_code >= 300:
      logging.warning('POST %s - %s:%s' % (url, res.status_code, res.reason))
    else:
      logging.debug('POST %s - %s:%s' % (url, res.status_code, res.reason))
    return res


class RunCommand:
  def node(self):
    config = get_config('node')
    controller.init(config['center_url'], config['center_token'])
    run_node(config)

  def center(self):
    run_center(port=30000)


class ProjectCommand:
  def create(self, project):
    for item in ['gcs', 'dcs']:
      cmd = 'mc mb %s/%s' % (item, project)
      logging.info(cmd)
      ret = os.system(cmd)
      if int(ret) == 0:
        logging.info('success')
      else:
        logging.warning('fail')

  def remove(self, project, force=False):
    for item in ['gcs', 'dcs']:
      op = ''
      if force:
        op = '--force'
      cmd = 'mc rb %s %s/%s' % (op, item, project)
      logging.info(cmd)
      ret = os.system(cmd)
      if int(ret) == 0:
        logging.info('success')
      else:
        logging.warning('fail')


class ConfigCommand:
  def add(self,
          access_key='',
          secret_key='',
          type='gcs',
          url='https://storage.googleapis.com'):
    logging.debug('add')
    res = Api.post('config/add', {
      'type': type,
      'url': url,
      'access_key': access_key,
      'secret_key': secret_key,
    })
    data = res.json()
    print(data)

  def update(self):
    logging.debug('add')
    res = Api.post('config/update')
    data = res.json()
    print(data)


class AdminCommand:
  def __init__(self):
    self.run = RunCommand()
    self.config = ConfigCommand()
    self.project = ProjectCommand()

  def init_node(
        self,
        center_url='http://localhost:30000',
        center_token='my-token',
        dataset_dir='/data'):
    set_config({
      'kind': 'node',
      'dataset_dir': dataset_dir,
      'center_url': center_url,
      'center_token': center_token,
    })

  def init_center(
        self,
        center_url='http://localhost:30000',
        center_token='my-token',
        origin='dcs',
        origin_url='',
        origin_access_key='',
        origin_secret_key='',
        mirror='gcs',
        mirror_url='',
        mirror_access_key='',
        mirror_secret_key=''):

    set_config({
      'kind': 'center',
      'center_url': center_url,
      'center_token': center_token,
      'origin': origin,
      'origin_url': origin_url,
      'origin_access_key': origin_access_key,
      'origin_secret_key': origin_secret_key,
      'mirror': mirror,
      'mirror_url': mirror_url,
      'mirror_access_key': mirror_access_key,
      'mirror_secret_key': mirror_secret_key,
    })

  def st(self, project, debug=False):
    logging.debug('st(status)')
    res = Api.post('stat', {'project': project})
    data = res.json()
    nodes = data['nodes']
    projects = data['projects']
    if debug:
      print(json.dumps(data, indent=2, sort_keys=True))

    Display().print_basic_info(nodes)
    Display().print_diff_nodes(project, nodes, projects)
    self.history(5)

  def diff(self, project):
    logging.debug('diff')
    Api.post('diff', {'project': project})

  def env(self):
    logging.debug('env')
    command = 'env | grep DSMS_'
    logging.debug('command: %s' % command)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    for line in out.decode('utf-8').strip().split('\n'):
      if line is None or len(line) == 0:
        continue
      print(line)

  def pull(self, project, remove=False):
    logging.debug('pull')
    Api.post('pull', {
      'project': project,
      'remove': remove
    })

  def detail(self, tid, debug=False):
    logging.debug('detail')
    res = Api.post('history-detail', {
      'target_tid': tid,
    })
    data = res.json()
    details = data['data']['details']
    Display().print_history_detail(tid, details, debug)

  def history(self, limit=-1, debug=False):
    logging.debug('history')
    res = Api.post('history', {
      'limit': limit,
    })
    data = res.json()
    if debug:
      print(data)
    Display().print_history(data)


class BucketCommand:
  def ls(self):
    command = 'mc ls dcs --json'
    success, out, err = run_proc(command)
    assert success
    msg = out.decode('utf-8').strip()
    data = [json.loads(line) for line in msg.split('\n')]
    Display().print_bucket_ls(data)

  def detail(self, bucket_id):
    command = 'mc ls dcs/%s -r --json' % bucket_id
    success, out, err = run_proc(command)
    assert success
    msg = out.decode('utf-8').strip()
    data = [json.loads(line) for line in msg.split('\n')]
    Display().print_bucket_detail(data, bucket_id)


class Command:
  def __init__(self):
    self.admin = AdminCommand()
    self.bucket = BucketCommand()

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
      res = Api.post('sync-mirror', {'project': project})
      logging.info('sync-mirror status: %s' % res.status_code)
    else:
      logging.info('fail')
    logging.info('push finish.')
