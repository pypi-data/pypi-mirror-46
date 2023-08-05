import logging
import os
import shutil
import socket
import subprocess
import time

import socketio

from .util import get_id, set_mc_config, get_diff_list

sio = socketio.Client()
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("engineio").setLevel(logging.WARNING)
logging.getLogger("socketio").setLevel(logging.WARNING)


def log_to_center(tid, title='', msg='', success=True):
  logging.debug('log_to_center: %s' % tid)
  hostname = socket.gethostname()
  sio.emit(
    'log', {
      'tid': tid,
      'success': success,
      'title': title,
      'msg': msg,
      'hostname': hostname,
      'ts': time.time(),
    })


class NodeConfig:
  args = None
  diffs = {}
  pulls = {} # project : data


class NodeUtil:
  @staticmethod
  def send_diff_info(project):
    diff_info = NodeConfig.diffs[project]
    sio.emit('diff_info', diff_info)

  @staticmethod
  def get_timestamp(dt):
    if isinstance(dt, str):
      return 0
    try:
      ts = time.mktime(dt.timetuple())
      return ts
    except:
      return 0

  @staticmethod
  def send_info():
    hostname = socket.gethostname()
    sio.emit(
      'node_info', {
        'hostname': hostname,
        'disk_usage': NodeUtil.get_disk_usage(),
      })

  @staticmethod
  def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return {
      'unit': 'byte',
      'total': total,
      'used': used,
      'free': free,
      'used_ratio': float(used) / total,
    }

  @staticmethod
  def set_default_project_info(project):
    if project not in NodeConfig.diffs:
      NodeConfig.diffs[project] = {
        'project': project,
        'diff_list': [],
        'last_diff_ts': 0,
        'last_pull_ts': 0,
        'status': 'idle',
      }

  @staticmethod
  def append_project_diff_info(project, diff_list, last_diff_ts):
    NodeUtil.set_default_project_info(project)
    t = NodeConfig.diffs[project]
    t['diff_list'] = diff_list
    t['last_diff_ts'] = last_diff_ts

  @staticmethod
  def append_project_pull_info(project, status):
    NodeUtil.set_default_project_info(project)
    t = NodeConfig.diffs[project]
    t['status'] = status
    if status == 'idle':
      last_pull_ts = int(time.time())
      t['last_pull_ts'] = last_pull_ts

  @staticmethod
  def refresh_diff_list(tid, project):
    logging.debug('update_diff_list')
    args = NodeConfig.args
    dataset_dir = args['dataset_dir']
    dest = 'dcs/%s' % project
    src = '%s/%s' % (dataset_dir, project)
    # src  = dataset_dir
    _create_folder_if_not_exist(project)
    success, command, msg, diff_list = get_diff_list(src, dest)
    NodeUtil.append_project_diff_info(project, diff_list, int(time.time()))
    log_to_center(tid, title='refresh_diff_list', msg=msg, success=success)
    NodeUtil.send_diff_info(project)

  @staticmethod
  def start_pull(project):
    logging.info('start_pull')
    status = 'ing'
    NodeUtil.append_project_pull_info(project, status)
    NodeUtil.send_info()

  @staticmethod
  def complete_pull(project):
    logging.info('complete_pull')
    status = 'idle'
    NodeUtil.append_project_pull_info(project, status)
    NodeUtil.send_info()

  @staticmethod
  def fail_pull(project):
    logging.info('fail_pull')
    status = 'fail'
    NodeUtil.append_project_pull_info(project, status)
    NodeUtil.send_info()


@sio.on('connect')
def on_connect():
  logging.debug('connection established')
  NodeUtil.send_info()


@sio.on('pull', namespace='/test')
def on_pull(data):
  logging.debug('on_pull')
  tid = data['tid']
  project = data['project']
  remove = data['remove']
  remove_option = ''
  if remove:
    remove_option = '--remove'
  NodeUtil.start_pull(project)
  args = NodeConfig.args
  try:
    src = 'dcs/%s' % project
    dest = '%s/%s' % (args['dataset_dir'], project)
    # dest = args['dataset_dir']
    _create_folder_if_not_exist(project)
    command = 'mc mirror --quiet --overwrite %s %s %s' % (
      remove_option, src, dest)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if int(proc.returncode) == 0:
      NodeUtil.complete_pull(project)
    if proc.returncode != 0:
      logging.warning(out)
      logging.warning(err)
      NodeUtil.fail_pull(project)
    NodeUtil.refresh_diff_list(tid, project)
  except Exception as ex:
    logging.exception(ex)
    NodeUtil.fail_pull(project)
  finally:
    NodeUtil.send_info()


@sio.on('diff', namespace='/test')
def on_diff(data):
  logging.debug('on_diff')
  tid = data['tid']
  project = data['project']
  try:
    NodeUtil.refresh_diff_list(tid, project)
    NodeUtil.send_info()
  except Exception as ex:
    logging.exception(ex)


@sio.on('update_config', namespace='/test')
def on_update_config(data):
  logging.debug('on_update_config')
  if 'tid' in data:
    tid = data['tid']
  else:
    tid = get_id()
  success, msg = set_mc_config(data)
  log_to_center(tid, title='update_config', msg=msg, success=success)


@sio.on('disconnect')
def on_disconnect():
  logging.debug('disconnected from manager')


def _create_folder_if_not_exist(project):
  logging.debug('_create_folder_if_not_exist')
  args = NodeConfig.args
  l = '%s/%s' % (args['dataset_dir'], project)
  if not os.path.exists(l):
    os.makedirs(l)


def run_node(args):
  logging.debug('run_node, %s' % args)
  NodeConfig.args = args
  while True:
    try:
      sio.connect(args['center_url'])
      sio.wait()
    except Exception as ex:
      logging.exception(ex)
      time.sleep(5)
