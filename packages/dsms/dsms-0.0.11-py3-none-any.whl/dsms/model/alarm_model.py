import collections
import time


class AlarmModel:
  def __init__(self):
    self.meta = {}
    self.msgs = {}

  def append_msg(self, project_id, alarm_id, msg):
    msgs = self.msgs
    if project_id not in msgs:
      msgs[project_id] = {}
    if alarm_id not in msgs[project_id]:
      msgs[project_id][alarm_id] = collections.deque(maxlen=1024)
    msgs[project_id][alarm_id].append((int(time.time()), msg))

  def get_msgs(self, project_id, alarm_id):
    msgs = self.msgs
    if project_id not in msgs:
      return []
    if alarm_id not in msgs[project_id]:
      return []
    return list(msgs[project_id][alarm_id])

  def is_exist(self, project_id, alarm_id):
    meta = self.meta
    if project_id not in meta:
      return False
    if alarm_id not in meta[project_id]:
      return False
    return True

  def get_my_alarm(self, project_id, alarm_id):
    if self.is_exist(project_id, alarm_id):
      return self.meta[project_id][alarm_id]
    return None

  def create(self, project_id, alarm_id):
    meta = self.meta
    if project_id not in meta:
      meta[project_id] = {}
    my_meta = meta[project_id]
    my_meta[alarm_id] = {'slack': {}, 'email': {}}
    return True, 'ok'

  def delete(self, project_id, alarm_id):
    if not self.is_exist(project_id, alarm_id):
      return False, 'project not in alarm model'

    meta = self.meta
    my_meta = meta[project_id]
    del my_meta[alarm_id]
    return True, 'ok'

  def detail(self, project_id):
    if project_id in self.meta:
      return self.meta[project_id]
    return {}

  def add_email(self, project_id, alarm_id, email):
    if not self.is_exist(project_id, alarm_id):
      return False, 'project not in alarm model'
    meta = self.meta
    my_alarm = meta[project_id][alarm_id]
    emails = my_alarm['email']
    if email in emails:
      return True, 'already exist'
    else:
      emails[email] = {
        'email': email
      }
    return True, 'ok'

  def add_slack(self, project_id, alarm_id, slack_url, slack_channel):
    if not self.is_exist(project_id, alarm_id):
      return False, 'project not in alarm model'
    meta = self.meta
    my_alarm = meta[project_id][alarm_id]
    slacks = my_alarm['slack']
    if slack_url in slacks:
      return True, 'already exist'
    else:
      slacks[slack_url] = {
        'url': slack_url,
        'channel': slack_channel,
      }
    return True, 'ok'
