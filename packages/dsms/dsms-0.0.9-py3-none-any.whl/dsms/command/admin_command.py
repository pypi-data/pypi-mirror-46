import json
import logging
import subprocess

from dsms.display import Display
from dsms.node import run_node
from dsms.router import run_center
from dsms.sdk import Api
from dsms.util import (
  set_config, get_config
)


class RunCommand:
  def node(self):
    config = get_config('node')
    Api.init(config['center_url'], config['center_token'])
    run_node(config)

  def center(self):
    run_center(port=30000)


class ConfigCommand:
  def add(self,
          access_key='',
          secret_key='',
          type='dcs',
          url='http://dudaji-cloud.iptime.org'):
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
        origin_secret_key=''):

    set_config({
      'kind': 'center',
      'center_url': center_url,
      'center_token': center_token,
      'origin': origin,
      'origin_url': origin_url,
      'origin_access_key': origin_access_key,
      'origin_secret_key': origin_secret_key,
    })

  def st(self, project, debug=False):
    logging.debug('st(status)')
    res = Api.post('stat', {'project': project})
    data = res.json()
    nodes = data['nodes']
    diff_data = data['diff_data']
    if debug:
      print(json.dumps(data, indent=2, sort_keys=True))

    Display().print_basic_info(nodes)
    Display().print_diff_nodes(project, nodes, diff_data)
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
