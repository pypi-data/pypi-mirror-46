from dsms.sdk import Api, assert_project_exist_in_config


def get_alarm_post_param(project_id, alarm_id):
  data = assert_project_exist_in_config(project_id)
  data.update({'alarm_id': alarm_id})
  return data


class AlarmCommand:
  def create(self, project_id, alarm_id):
    data = get_alarm_post_param(project_id, alarm_id)
    res = Api.post('alarm/create', data=data)
    print(res.json())
    Api.set_project_config_from_center(project_id)

  def add_email(self, project_id, alarm_id, email):
    data = get_alarm_post_param(project_id, alarm_id)
    data.update({'email': email})
    res = Api.post('alarm/email', data=data)
    # TODO: implement me
    Api.set_project_config_from_center(project_id)

  def add_slack(
        self, project_id, alarm_id, slack_url, slack_channel='general'):
    data = get_alarm_post_param(project_id, alarm_id)
    data.update({
      'slack_url': slack_url,
      'slack_channel': slack_channel
    })
    res = Api.post('alarm/slack', data=data)
    print(res.json())
    Api.set_project_config_from_center(project_id)

  def send(self, project_id, alarm_id, msg):
    data = get_alarm_post_param(project_id, alarm_id)
    data.update({'msg': msg})
    res = Api.post('alarm', data=data)
