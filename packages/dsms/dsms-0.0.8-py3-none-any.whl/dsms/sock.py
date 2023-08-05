import logging

from flask import request
from flask_socketio import emit


def init_sock(socketio, center_controller):
  logging.info('init_sock')

  @socketio.on('connect', namespace='/test')
  def on_connect():
    logging.debug('connect')
    emit('update_config', center_controller.config, namespace='/test')

  @socketio.on('node_info')
  def on_node_info(data):
    logging.debug('on_node_info')
    center_controller.add_node_info(request.sid, data)

  @socketio.on('diff_info')
  def on_diff_info(data):
    logging.debug('on_diff_info')
    center_controller.add_diff_info(request.sid, data)

  @socketio.on('log')
  def on_log_from_node(data):
    logging.debug('on_log_from_node')
    title = ''
    if 'title' in data:
      title = data['title']
    center_controller.append_history(
      data['tid'],
      title='node:%s' % title,
      hostname=data['hostname'],
      msg=data['msg'],
      success=bool(data['success']))

  @socketio.on('disconnect')
  def on_disconnect():
    logging.debug('on_disconnect')
    key = request.sid
    if key in center_controller.nodes:
      del center_controller.nodes[key]
    if key in center_controller.diffs:
      del center_controller.diffs[key]
    print('Client disconnected')
