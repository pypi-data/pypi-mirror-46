#!/usr/bin/env python3

import json
import logging
from functools import wraps

from flask import Flask
from flask import jsonify
from flask import request, abort
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from dsms.controller.alarm_controller import AlarmController
from dsms.controller.center_controller import CenterController
from dsms.controller.project_controller import ProjectController
from dsms.controller.storage_controller import StorageController
from dsms.model.auth_model import AuthModel
from dsms.model.storage_model import StorageModel
from dsms.case_converter import (
  snake_to_camel,
  change_key_style,
  camel_to_snake,
)
from .sock import init_sock
from .util import get_id, snake_body, authorized

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
cors = CORS(app, resources={
  r'*': {'origin': '*'},
})
app.config['SECRET_KEY'] = 'dudaji-secret!'
socketio = SocketIO(
  app,
  logger=False,
  engineio_logger=False)
auth_model = AuthModel()
storage_model = StorageModel()
center_controller = CenterController()
project_controller = ProjectController(
  center_controller,
  auth_model)
storage_controller = StorageController(storage_model)
alarm_controller = AlarmController()


def authorized_project(fn):
  @wraps(fn)
  def _wrap(*args, **kwargs):
    j = request.get_json()
    if 'token' not in j:
      abort(401)
    if not auth_model.is_exist(j['token']):
      abort(401)
    return fn(*args, **kwargs)

  return _wrap


def authorized_storage(fn):
  @wraps(fn)
  def _wrap(*args, **kwargs):
    j = change_key_style(request.get_json(), camel_to_snake)
    if 'project_id' not in j:
      abort(401)
    if 'storage' not in j:
      abort(401)
    if 'storage_secret_key' not in j['storage']:
      abort(401)
    if not storage_model.is_valid(
          j['project_id'],
          j['storage']['storage_secret_key']):
      abort(401)
    return fn(*args, **kwargs)

  return _wrap


@app.route('/ping', methods=['POST'])
@authorized
def ping():
  logging.debug('ping')
  return json.dumps({'msg': 'pong'})


@app.route('/storage', methods=['POST'])
@snake_body
def enable_storage(req):
  logging.debug('enable_storage')
  project_id = req['project_id']
  if 'storage_secret_key' in req:
    storage_secret_key = req['storage_secret_key']
  else:
    storage_secret_key = get_id(8)
  success, _ = storage_controller.enable_storage(
    project_id=project_id,
    storage_secret_key=storage_secret_key)
  storage_type = 'dcs'
  data = {
    'project_id': project_id,
    'storage_type': storage_type,
    'storage_secret_key': storage_secret_key,
  }
  data = change_key_style(data, snake_to_camel)
  ret = jsonify(data)
  return ret


@app.route('/bucket', methods=['POST'])
@authorized_storage
@snake_body
def create_bucket(req):
  logging.debug('create_bucket')
  project_id = req['project_id']
  bucket_id = req['bucket_id']
  storage_secret_key = req['storage']['storage_secret_key']
  success, msg = storage_controller.create_bucket(
    project_id=project_id,
    storage_secret_key=storage_secret_key,
    bucket_id=bucket_id)
  return jsonify({'success': success, 'msg': msg})


@app.route('/buckets/<project_id>', methods=['GET'])
def get_bucket_list(project_id):
  logging.debug('get_bucket_list')
  buckets = storage_controller.get_bucket_list(project_id)
  return jsonify(buckets)


@app.route('/buckets/<project_id>/<bucket_id>', methods=['GET'])
def get_bucket_detail(project_id, bucket_id):
  detail = storage_controller.get_bucket_detail(project_id, bucket_id)
  return jsonify(detail)


@app.route('/bucket', methods=['DELETE'])
@authorized_storage
@snake_body
def delete_bucket(req):
  logging.debug('delete_bucket')
  project_id = req['project_id']
  bucket_id = req['bucket_id']
  storage_secret_key = req['storage']['storage_secret_key']
  success, msg = storage_controller.delete_bucket(
    project_id=project_id,
    storage_secret_key=storage_secret_key,
    bucket_id=bucket_id)
  return jsonify({'success': success, 'msg': msg})


@app.route('/mc-config', methods=['POST'])
@authorized
def mc_config():
  logging.debug('mc_config')
  ret = jsonify(center_controller.config)
  return ret


@app.route('/', methods=['GET', 'POST'])
def index():
  return 'Hello, this is dsms center'


@app.route('/stat', methods=['POST'])
@authorized
def stat():
  req = request.get_json()
  project = req['project']
  nodes = center_controller.get_live_node_list()
  diff_data = center_controller.get_diff_data(project)
  ret = jsonify({
    'nodes': nodes,
    'diff_data': diff_data,
  })
  return ret


@app.route('/pull', methods=['GET', 'POST'])
@authorized
def pull():
  logging.debug('pull')
  req = request.get_json()
  tid = req['tid']
  center_controller.append_history(tid, title='pull', msg='start')
  emit('pull', req, namespace='/test', broadcast=True)
  return json.dumps({'status': 200, 'message': 'ok'})


@app.route('/diff', methods=['GET', 'POST'])
@authorized
def diff():
  req = request.get_json()
  logging.debug('diff')
  center_controller.append_history(req['tid'], title='diff', msg='start',
                                   success=True)
  emit('diff', req, namespace='/test', broadcast=True)
  return json.dumps({'msg': 'broadcast diff command'})


@app.route('/config/add', methods=['POST'])
@authorized
def add_config():
  c = request.get_json()
  ret = center_controller.add_config(c)
  logging.debug('config/add: %s' % c['type'])
  return json.dumps(ret)


@app.route('/config/update', methods=['POST'])
@authorized
def update_config():
  logging.debug('config/update')
  emit('update_config', center_controller.config, namespace='/test',
       broadcast=True)
  return json.dumps({'msg': 'broadcast config update command'})


@app.route('/history', methods=['POST'])
@authorized
def history():
  # logging.debug('history')
  c = request.get_json()
  limit = int(c['limit'])
  if limit < 0:
    return json.dumps(center_controller.history_list)
  else:
    return json.dumps(center_controller.history_list[(-1) * limit:])


@app.route('/history-detail', methods=['POST'])
@authorized
def history_detail():
  logging.debug('history_detail')
  c = request.get_json()
  tid = c['target_tid']
  if tid in center_controller.history:
    return json.dumps({
      'success': True,
      'data': center_controller.history[tid]
    })
  else:
    print(tid)
    print(center_controller.history)
    return json.dumps({'success': False})


def _get_project_config(project_id):
  d = project_controller.get_config(project_id)
  if not d:
    abort(400)
  d['storage'] = storage_controller.get_config(project_id)
  d['alarm'] = alarm_controller.get_config(project_id)
  return json.dumps(d)


@app.route('/project', methods=['POST'])
@authorized
@snake_body
def create_project(req):
  logging.debug('create_project')
  project_id = req['project_id']
  user = req['user_id']
  if len(project_id) < 4:
    logging.info('project_id is too short')
    abort(400)
  token = project_controller.create_or_append(project_id, user)
  storage_secret_key = token
  storage_controller.enable_storage(
    project_id=project_id,
    storage_secret_key=storage_secret_key)
  return _get_project_config(project_id)


@app.route('/project/config/<project_id>', methods=['GET'])
def get_project_config(project_id):
  return _get_project_config(project_id)


@app.route('/project', methods=['DELETE'])
@authorized
@snake_body
def delete_project(req):
  logging.debug('delete_project')
  project_id = req['project_id']
  storage_secret_key = req['storage']['storage_secret_key']
  success = storage_controller.disable_storage(
    project_id, storage_secret_key)
  if not success:
    logging.info('disable storage fail (skip)')

  success, msg = project_controller.delete(project_id)
  return json.dumps({'success': success, 'msg': msg})


@app.route('/projects', methods=['GET'])
@authorized
def get_projects():
  logging.debug('get_projects')
  return json.dumps(project_controller.model.data)


@app.route('/project/detail', methods=['POST'])
@authorized
@authorized_project
def get_project_detail():
  logging.debug('get_project_detail')
  return json.dumps(project_controller.model.data)


@app.route('/alarm', methods=['POST'])
@authorized
@authorized_project
@snake_body
def send_alarm(req):
  logging.debug('send_alarm')
  project_id = req['project_id']
  alarm_id = req['alarm_id']
  msg = req['msg']
  return json.dumps(alarm_controller.send(project_id, alarm_id, msg))


@app.route('/alarm/msg/<project_id>/<alarm_id>', methods=['GET'])
@authorized
def get_msgs(project_id, alarm_id):
  logging.debug('get_msgs')
  return json.dumps(alarm_controller.get_msgs(project_id, alarm_id))


@app.route('/alarm/create', methods=['POST'])
@authorized
@authorized_project
@snake_body
def create_alarm(req):
  logging.debug('create_alarm')
  project_id = req['project_id']
  alarm_id = req['alarm_id']
  return json.dumps(alarm_controller.create(project_id, alarm_id))


@app.route('/alarm/email', methods=['POST'])
@authorized
@authorized_project
@snake_body
def add_email_to_alarm(req):
  logging.debug('add_email_to_alarm')
  project_id = req['project_id']
  alarm_id = req['alarm_id']
  email = req['email']
  return json.dumps(alarm_controller.add_email(project_id, alarm_id, email))


@app.route('/alarm/slack', methods=['POST'])
@authorized
@authorized_project
@snake_body
def add_slack_to_alarm(req):
  logging.debug('add_slack_to_alarm')
  project_id = req['project_id']
  alarm_id = req['alarm_id']
  slack_url = req['slack_url']
  slack_channel = req['slack_channel']
  return json.dumps(alarm_controller.add_slack(
    project_id, alarm_id, slack_url, slack_channel))


def run_center(port=30000):
  init_sock(socketio, center_controller)
  center_controller.load_mc_config()
  socketio.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
  run_center()
