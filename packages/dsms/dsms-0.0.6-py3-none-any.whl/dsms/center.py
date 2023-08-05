#!/usr/bin/env python3

import json
import logging
import socket
import time
from functools import wraps

import jwt
from flask import Flask
from flask import abort, request
from flask import jsonify
from flask_socketio import SocketIO, emit

from .util import get_config

logging.getLogger('werkzeug').setLevel(logging.ERROR)


def validate_token(access_token):
  encoded = access_token.split(' ')[1]
  return jwt.decode(encoded, verify=False)


def authorized(fn):
  @wraps(fn)
  def _wrap(*args, **kwargs):
    if 'Authorization' not in request.headers:
      # Unauthorized
      print("No token in header")
      abort(401)
      return None
    data = validate_token(request.headers['Authorization'])
    if ('user' not in data) or (data['user'] != 'dudaji-23de'):
      abort(401)
      return None
    return fn(*args, **kwargs)

  return _wrap


class Center:
  def __init__(self):
    self.nodes = {}
    self.projects = {}
    self.config = {}
    self.history = {}
    self.history_list = []

  def get_project(self, project):
    return {
      k: v['data'] for k, v in center.projects.items()
      if v['project'] == project
    }

  def get_live_node_list(self):
    return [v for k, v in center.nodes.items() if v['connected'] is True]

  def get_first_dcs_node_key(self):
    candidate = [k for k, v in center.nodes.items()
                 if v['connected'] is True]
    if len(candidate) == 0:
      return None
    return candidate[0]

  def append_history(self, tid, title='', msg='', hostname=None, success=True):
    if not hostname:
      hostname = 'center'
    ts = time.time()
    if tid not in self.history:
      live_node_count = len(self.get_live_node_list())
      item = {
        'tid': tid,
        'ts': ts,
        'success_count': 0,
        'fail_count': 0,
        'live_node_count': live_node_count,
        'title': title,
        'hostname': hostname,
        'details': []
      }
      self.history[tid] = item
      self.history_list.append(item)
    cur = self.history[tid]
    if success:
      cur['success_count'] += 1
    else:
      cur['fail_count'] += 1
    cur['details'].append((success, hostname, title, msg))
    # logging.debug(cur)

  def add_config(self, d):
    key = d['type']
    message = 'ok'
    if key in self.config:
      message = 'duplicated key: %s' % key
    self.config[key] = d
    return {'success': True, 'msg': message}

  def _set_mc_config(self, type, url, access_key, secret_key):
    if type in self.config:
      logging.warning('type(%s) is already exist. url: %s' % (
        type, url))

    self.config[type] = {
      'type': type,
      'url': url,
      'access_key': access_key,
      'secret_key': secret_key
    }

  def load_mc_config(self):
    logging.info('load_mc_config start')
    config = get_config('center')
    type = config['origin']
    url = config['origin_url']
    access_key = config['origin_access_key']
    secret_key = config['origin_secret_key']
    self._set_mc_config(type, url, access_key, secret_key)
    type = config['mirror']
    url = config['mirror_url']
    access_key = config['mirror_access_key']
    secret_key = config['mirror_secret_key']
    self._set_mc_config(type, url, access_key, secret_key)
    logging.error(self.config)

  def add_node_info(self, key, data):
    data['connected'] = True
    data['key'] = key
    self.nodes[key] = data

  def add_project_info(self, key, data):
    self.projects[key] = {
      'project': data['project'],
      'data': data
    }

  def delete_node(self, key):
    if key in self.nodes:
      self.nodes[key]['connected'] = False

  def sync_mirror(self, tid, project, remove=False):
    logging.debug('sync_mirror')
    node_key = self.get_first_dcs_node_key()
    if node_key:
      logging.debug('first dcs node key: %s' % node_key)
      emit('sync_mirror', {
        'tid': tid,
        'project': project,
        'remove': remove,
      }, room=node_key, namespace='/test')
      return {'success': True, 'msg': 'start sync_mirror in chief node'}
    else:
      logging.warning('No first node')
      return {'success': False, 'msg': 'No sync chief node'}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dudaji-secret!'
socketio = SocketIO(
  app,
  logger=False,
  engineio_logger=False)
center = Center()


@app.route('/mc-config', methods=['POST'])
@authorized
def mc_config():
  logging.debug('mc_config')
  ret = jsonify(center.config)
  return ret


@app.route('/')
def index():
  return 'Hello, this is dsms center'


@app.route('/stat', methods=['POST'])
@authorized
def stat():
  req = request.get_json()
  project = req['project']
  nodes = center.get_live_node_list()
  projects = center.get_project(project)
  ret = jsonify({
    'nodes': nodes,
    'projects': projects,
  })
  return ret


@app.route('/pull', methods=['GET', 'POST'])
@authorized
def pull():
  logging.debug('pull')
  req = request.get_json()
  tid = req['tid']
  center.append_history(tid, title='pull', msg='start')
  emit('pull', req, namespace='/test', broadcast=True)
  return json.dumps({'status': 200, 'message': 'ok'})


@app.route('/sync-mirror', methods=['GET', 'POST'])
@authorized
def sync_mirror():
  logging.debug('sync-mirror')
  req = request.get_json()
  tid = req['tid']
  project = req['project']
  sync_result = center.sync_mirror(tid, project)
  if sync_result['success'] is False:
    msg = sync_result['msg']
    center.append_history(tid, title='sync_mirror', msg=msg, success=False)
    return json.dumps({'status': 500, 'message': 'sync error'})
  return json.dumps({'status': 200, 'message': 'ok'})


@app.route('/diff', methods=['GET', 'POST'])
@authorized
def diff():
  req = request.get_json()
  logging.debug('diff')
  center.append_history(req['tid'], title='diff', msg='start', success=True)
  emit('diff', req, namespace='/test', broadcast=True)
  return json.dumps({'msg': 'broadcast diff command'})


@app.route('/config/add', methods=['POST'])
@authorized
def add_config():
  c = request.get_json()
  ret = center.add_config(c)
  logging.debug('config/add: %s' % c['type'])
  return json.dumps(ret)


@app.route('/config/update', methods=['POST'])
@authorized
def update_config():
  logging.debug('config/update')
  emit('update_config', center.config, namespace='/test', broadcast=True)
  return json.dumps({'msg': 'broadcast config update command'})


@app.route('/history', methods=['POST'])
@authorized
def history():
  # logging.debug('history')
  c = request.get_json()
  limit = int(c['limit'])
  if limit < 0:
    return json.dumps(center.history_list)
  else:
    return json.dumps(center.history_list[(-1) * limit:])


@app.route('/history-detail', methods=['POST'])
@authorized
def history_detail():
  logging.debug('history_detail')
  c = request.get_json()
  tid = c['target_tid']
  if tid in center.history:
    return json.dumps({
      'success': True,
      'data': center.history[tid]
    })
  else:
    print(tid)
    print(center.history)
    return json.dumps({'success': False})


@socketio.on('connect', namespace='/test')
def on_connect():
  logging.debug('connect')
  emit('update_config', center.config, namespace='/test')


@socketio.on('node_info')
def on_node_info(data):
  logging.debug('on_node_info')
  center.add_node_info(request.sid, data)


@socketio.on('project_info')
def on_project_info(data):
  logging.debug('on_project_info')
  center.add_project_info(request.sid, data)


@socketio.on('log')
def on_log_from_node(data):
  logging.debug('on_log_from_node')
  title = ''
  if 'title' in data:
    title = data['title']
  center.append_history(
    data['tid'],
    title='node:%s' % title,
    hostname=data['hostname'],
    msg=data['msg'],
    success=bool(data['success']))


@socketio.on('disconnect')
def on_disconnect():
  logging.debug('on_disconnect')
  key = request.sid
  if key in center.nodes:
    del center.nodes[key]
  if key in center.projects:
    del center.projects[key]
  print('Client disconnected')


def run_center(port=30000):
  center.load_mc_config()
  socketio.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
  run_center()
