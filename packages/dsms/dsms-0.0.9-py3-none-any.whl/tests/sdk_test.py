import dsms.sdk as dsdk

def test_send_alarm():
  sdk = dsdk.Sdk()
  project_id = 'project1'
  alarm_id = 'alarm1'
  bucket_id = 'bucket1'
  local_dir = '/data/project1/bucket1'
  print(sdk.project(project_id).alarm(alarm_id).send('yo'))
  sdk.project(project_id).bucket(bucket_id).push(local_dir)
