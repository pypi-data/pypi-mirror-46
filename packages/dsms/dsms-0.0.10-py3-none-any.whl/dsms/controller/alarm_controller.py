#!/usr/bin/env python3
import json

import requests
import slack

from dsms.model.alarm_model import AlarmModel


def ret_to_dict(result):
  return {
    'success': result[0],
    'msg': result[1]
  }


class AlarmController:
  def __init__(self):
    self.alarm_model = AlarmModel()

  def create(self, project_id, alarm_id):
    return ret_to_dict(
      self.alarm_model.create(project_id, alarm_id))

  def get_config(self, project_id):
    return self.alarm_model.detail(project_id)

  def add_slack(self, project_id, alarm_id, slack_url, slack_channel):
    return ret_to_dict(
      self.alarm_model.add_slack(
        project_id, alarm_id, slack_url, slack_channel))

  def add_email(self, project_id, alarm_id, email):
    return ret_to_dict(
      self.alarm_model.add_email(project_id, alarm_id, email))

  def send(self, project_id, alarm_id, msg):
    model = self.alarm_model
    my_alarm = model.get_my_alarm(project_id, alarm_id)
    model.append_msg(project_id, alarm_id, msg)
    self._send_email(my_alarm['email'], msg)
    self._send_slack(my_alarm['slack'], msg)

  def get_msgs(self, project_id, alarm_id):
    model = self.alarm_model
    return model.get_msgs(project_id, alarm_id)

  def _send_email(self, emails, text):
    for k, v in emails.items():
      print(k, v)

  def _send_slack(self, emails, text):
    result = True, 'ok'
    for v in emails.values():
      url = v['url']
      channel = v['channel']
      res = requests.post(url, data=json.dumps({
        'text': text,
        'channel': channel,
      }))
      if res.status_code >= 300:
        result = False, 'slack fail'
    return result
