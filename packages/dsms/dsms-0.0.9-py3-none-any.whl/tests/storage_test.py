import os

from minio import Minio

from dsms.controller.storage_controller import StorageController
from dsms.model.storage_model import StorageModel

access_key = 'my-project-id'
secret_key = 'my-secret-key'
bucket_id = 'bucket1'


def test_create_storage():
  project_id = access_key
  model = StorageModel()
  storage = StorageController(model)
  storage.disable_storage(project_id, secret_key)
  success = storage.enable_storage(project_id, secret_key)
  assert success
  success = storage.create_bucket(bucket_id, project_id, secret_key)
  print(model.data)
  assert success


def test_minio_put_get():
  client = Minio(
    'dudaji-cloud.iptime.org',
    access_key='project1',
    secret_key='7746d66ef7d84a7aa0fad3f09bf44c98',
    secure=False)
  for item in client.list_objects(bucket_id):
    print(item)

  filename = 'test-file-for-upload.txt'
  os.system('touch %s' % filename)
  file_stat = os.stat(filename)
  with open(filename, 'rb') as data:
    client.put_object(
      bucket_id, filename, data, file_stat.st_size, 'text/plain')
