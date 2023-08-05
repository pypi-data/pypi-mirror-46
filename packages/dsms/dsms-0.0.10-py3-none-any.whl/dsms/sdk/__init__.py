import json
import logging
import os

import requests
from minio import Minio

from dsms.sdk.minio_progress import MinioProgress
from dsms.util import get_config, set_config
from dsms.util import get_id
from dsms.util import set_project_config, get_project_config


class Sdk:
  def __init__(self):
    self.project_id = None
    self.alarm_id = None
    self.bucket_id = None
    self.is_ready = False

  def project(self, project_id):
    self.project_id = project_id
    data = Api.get_project_config(project_id)
    set_project_config(project_id, data)
    return self

  def bucket(self, bucket_id):
    self.bucket_id = bucket_id
    return self

  def push(self, local_dir):
    local_dir = local_dir.rstrip('/') + '/'
    logging.debug('push: dir(%s)' % local_dir)
    pca = get_project_config()
    pc = pca[self.project_id]
    client = Minio(
      'dudaji-cloud.iptime.org',
      access_key=self.project_id,
      secret_key=pc['storage']['storage_secret_key'],
      secure=False)
    files = []
    for r, d, f in os.walk(local_dir):
      for file in f:
        full_file = os.path.join(r, file)
        files.append(full_file)
    progress = MinioProgress(self)
    for f in files:
      file_stat = os.stat(f)
      with open(f, 'rb') as data:
        object_name = f.replace(local_dir, '')
        logging.debug('put_object: %s, %s' % (f, object_name))
        client.put_object(
          self.bucket_id,
          object_name,
          data,
          file_stat.st_size,
          progress=progress)

  def alarm(self, alarm_id='alarm1'):
    self.alarm_id = alarm_id
    return self

  def check(self):
    assert self.project_id, 'Set project id first'
    logging.info('check sdk vars start.')
    logging.info('project is ok')
    project_id = self.project_id
    project_config = Api.get_project_config(self.project_id)
    alarm = project_config['alarm']
    if self.bucket_id:
      buckets = Api.get('buckets/%s' % project_id).json()
      assert self.bucket_id in buckets, 'Bucket is not valid'
      logging.info('bucket is ok')
    else:
      logging.info('bucket_id is None')
    if self.alarm_id:
      assert self.alarm_id in alarm, 'Alarm is not valid'
      logging.info('alarm is ok')
    else:
      logging.info('alarm_id is None')
    logging.info('check sdk vars finish.')
    return True

  def send(self, msg):
    assert self.alarm_id, 'Set alarm first'
    data = assert_project_exist_in_config(self.project_id)
    data.update({
      'alarm_id': self.alarm_id,
      'msg': msg
    })
    res = Api.post('alarm', data=data)
    return res

  def center(self, center_url, center_token):
    Api.init(center_url, center_token)


class ApiConfig:
  def __init__(self):
    self.center_url = ''
    self.center_token = ''
    self.is_ready = False

  def init(self, center_url, center_token):
    self.center_url = center_url
    self.center_token = center_token
    self.is_ready = True
    set_config({
      'kind': 'cli',
      'center_url': self.center_url,
      'center_token': self.center_token,
    })
    return self

  def ready(self):
    if self.is_ready:
      return
    config = get_config()
    self.init(config['center_url'], config['center_token'])
    return self


class Api:
  api_config = ApiConfig()

  @staticmethod
  def init(center_url, center_token):
    Api.api_config.init(center_url, center_token)

  @staticmethod
  def set_project_config_from_center(project_id):
    data = Api.get_project_config(project_id)
    set_project_config(project_id, data)

  @staticmethod
  def get_project_config(project_id):
    res = Api.get('project/config/%s' % project_id)
    assert res.status_code < 300, 'Fail to get project config (%s)' % project_id
    return res.json()

  @staticmethod
  def get(path, params={}):
    Api.api_config.ready()
    url = Api.api_config.center_url
    token = Api.api_config.center_token
    headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Authorization': 'bearer %s' % token
    }
    cookies = {'session_id': 'sorryidontcare'}
    url = url + '/' + path
    res = requests.get(
      url,
      headers=headers,
      cookies=cookies,
      params=json.dumps(params))
    if res.status_code >= 300:
      logging.warning('GET %s - %s:%s' % (url, res.status_code, res.reason))
    else:
      logging.debug('GET %s - %s:%s' % (url, res.status_code, res.reason))
    return res

  @staticmethod
  def post(path, data={}):
    Api.api_config.ready()
    url = Api.api_config.center_url
    token = Api.api_config.center_token
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

  @staticmethod
  def delete(path, data={}):
    Api.api_config.ready()
    url = Api.api_config.center_url
    token = Api.api_config.center_token
    headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Authorization': 'bearer %s' % token
    }
    data['tid'] = get_id()
    cookies = {'session_id': 'sorryidontcare'}
    url = url + '/' + path
    res = requests.delete(
      url,
      headers=headers,
      cookies=cookies,
      data=json.dumps(data))
    if res.status_code >= 300:
      logging.warning('DELETE %s - %s:%s' % (url, res.status_code, res.reason))
    else:
      logging.debug('DELETE %s - %s:%s' % (url, res.status_code, res.reason))
    return res


def is_project_exist_in_config(project_id):
  c = get_project_config()
  return project_id in c


def assert_project_exist_in_config(project_id):
  c = get_project_config()
  assert project_id in c, 'Create project first'
  return c[project_id]
