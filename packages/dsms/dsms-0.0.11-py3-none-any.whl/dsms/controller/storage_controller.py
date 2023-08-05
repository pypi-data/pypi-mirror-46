import json
import logging
import re

from dsms.model.storage_model import StorageModel
from dsms.util import run_proc, proc_result_to_dict


class StorageController:
  def __init__(self, model: StorageModel):
    self.model = model

  def get_config(self, project_id):
    return self.model.detail(project_id)

  def _is_policy_exist(self, policy):
    command = 'mc admin policy list dcs'
    success, out, err = run_proc(command)
    assert success
    for line in out.decode('utf-8').strip().split('\n'):
      if policy in line:
        return True
    return False

  def _create_tmp_policy_file(self, policy_context, filename):
    command = "echo '%s' > %s" % (policy_context, filename)
    print(command)
    success, out, err = run_proc(command)
    return success

  def _remove_policy(self, policy):
    command = 'mc admin policy remove dcs %s' % policy
    logging.debug('_remove_policy: (%s)' % command)
    success, out, err = run_proc(command)
    assert success
    return success

  def _update_policy(self, policy, policy_context, filename):
    success = self._create_tmp_policy_file(policy_context, filename)
    assert success
    command = 'mc admin policy add dcs %s %s' % (policy, policy)
    logging.debug('_update_policy: (%s)' % command)
    success, out, err = run_proc(command)
    assert success
    success = self._rm_tmp_policy_file(filename)
    assert success
    return success

  def _create_policy(self, policy):
    policy_context = """{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:*"],"Resource":["arn:aws:s3:::THIS_IS_EMPTY_BUCKET/*"]}]}"""
    filename = policy
    return self._update_policy(policy, policy_context, filename)

  def _rm_tmp_policy_file(self, filename):
    command = 'rm ./%s' % filename
    success, out, err = run_proc(command)
    assert success
    return success

  def _add_user_to_mc(self, access_key, storage_secret_key, policy):
    command = 'mc admin user add dcs %s %s %s' % (
      access_key, storage_secret_key, policy)
    logging.debug('_add_user_to_mc: (%s)' % command)
    success, out, err = run_proc(command)
    assert success
    return success

  def _get_user_policy_context(self, policy):
    command = 'mc admin policy list dcs %s' % policy
    logging.debug('_get_user_policy_context: (%s)' % command)
    success, out, err = run_proc(command)
    assert success
    msg = ''
    for line in out.decode('utf-8').strip().split('\n'):
      msg += line
    try:
      policy = json.loads(msg)
      return success, policy
    except Exception as ex:
      logging.error(ex)
      return False, {}

  def _make_bucket(self, bucket_id):
    command = 'mc mb dcs/%s' % bucket_id
    success, out, err = run_proc(command)
    return success, out, err

  def _rm_bucket(self, bucket_id):
    command = 'mc rb dcs/%s' % bucket_id
    success, out, err = run_proc(command)
    return success, out

  def _append_bucket_to_policy(self, policy, bucket_id):
    success, policy_context = self._get_user_policy_context(policy)
    assert success
    resource = 'arn:aws:s3:::%s/*' % bucket_id
    policy_context['Statement'][0]['Resource'].append(resource)
    new_policy_context = json.dumps(policy_context)
    filename = policy
    return self._update_policy(policy, new_policy_context, filename)

  def _remove_bucket_in_policy(self, policy, bucket_id):
    success, policy_context = self._get_user_policy_context(policy)
    assert success
    target = 'arn:aws:s3:::%s/*' % bucket_id
    new_resource = [k for k in policy_context['Statement'][0]['Resource']
                    if k != target]
    policy_context['Statement'][0]['Resource'] = new_resource
    new_policy_context = json.dumps(policy_context)
    filename = policy
    return self._update_policy(policy, new_policy_context, filename)

  def enable_storage(self, project_id, storage_secret_key):
    logging.debug('enable_storage: (%s)' % project_id)
    access_key = policy = project_id
    success = self._is_policy_exist(policy)
    if not success:
      logging.debug('policy is not exist yet')
      success = self._create_policy(policy)
      assert success
    success = self._add_user_to_mc(access_key, storage_secret_key, policy)
    assert success
    self.model.add(project_id, {
      'project_id': project_id,
      'storage_secret_key': storage_secret_key,
    })
    return success, storage_secret_key

  def _remove_mc_user(self, project_id):
    command = 'mc admin user remove dcs %s' % project_id
    success, out, err = run_proc(command)
    return success

  def disable_storage(self, project_id, storage_secret_key):
    logging.debug('disable_storage: (%s)' % project_id)
    policy = project_id
    bucket_list = self.get_bucket_list(policy)
    for bucket in bucket_list:
      self.delete_bucket(bucket, project_id, storage_secret_key)
    try:
      policy = project_id
      success = self._remove_policy(policy)
      if not success:
        logging.info('_remove_policy fail (%s)' % policy)
      success = self._remove_mc_user(project_id)
      if not success:
        logging.info('_remove_mc_user fail (%s)' % project_id)
      return success
    except Exception as ex:
      logging.exception(ex)
    return False

  def attach_bucket(self, bucket_id, project_id, storage_secret_key):
    policy = project_id
    success = self._append_bucket_to_policy(policy, bucket_id)
    assert success
    return success, 'ok'

  def create_bucket(self, bucket_id, project_id, storage_secret_key):
    access_key = project_id
    policy = access_key
    success, out, err = self._make_bucket(bucket_id)
    if not success:
      return success, json.dumps(proc_result_to_dict(out, err))
    success = self._append_bucket_to_policy(policy, bucket_id)
    assert success
    return success, 'ok'

  def delete_bucket(self, bucket_id, project_id, storage_secret_key):
    access_key = project_id
    policy = access_key
    success, out = self._rm_bucket(bucket_id)
    if not success:
      return success, out.decode('utf-8').strip()
    success = self._remove_bucket_in_policy(policy, bucket_id)
    assert success
    return success, 'ok'

  def get_bucket_detail(self, project_id, bucket_id):
    command = 'mc ls dcs/%s -r --json' % bucket_id
    success, out, err = run_proc(command)
    assert success
    msg = out.decode('utf-8').strip()
    data = [json.loads(line) for line in msg.split('\n') if len(line) > 0]
    return data

  def get_bucket_list(self, policy):
    """
    :param policy:
    policy = access_key = project_id
    :return:
    list of bucket_id
    """
    success, policy_context = self._get_user_policy_context(policy)
    if not success:
      return []

    def _extract(s):
      m = re.search(r':::(.*?)\/\*', s)
      if m:
        return m.group(1)
      else:
        return None

    resource_list = policy_context['Statement'][0]['Resource']
    bucket_list = [_extract(v) for v in resource_list]
    bucket_list = [v for v in bucket_list if v]
    return bucket_list
