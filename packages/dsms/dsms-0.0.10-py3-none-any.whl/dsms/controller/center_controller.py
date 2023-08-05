#!/usr/bin/env python3

import logging
import time

from dsms.util import get_config


class CenterController:
  def __init__(self):
    self.nodes = {}
    self.diffs = {}
    self.config = {}
    self.history = {}
    self.history_list = []

  def get_diff_data(self, project):
    return {
      k: v['data'] for k, v in self.diffs.items()
      if v['project'] == project
    }

  def get_live_node_list(self):
    return [v for k, v in self.nodes.items() if
            v['connected'] is True]

  def get_first_dcs_node_key(self):
    candidate = [k for k, v in self.nodes.items()
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
    print(self.config)

  def add_node_info(self, key, data):
    data['connected'] = True
    data['key'] = key
    self.nodes[key] = data

  def add_diff_info(self, key, data):
    self.diffs[key] = {
      'project': data['project'],
      'data': data
    }

  def delete_node(self, key):
    if key in self.nodes:
      self.nodes[key]['connected'] = False

