import logging
import sys
import time
from threading import Thread

from minio.compat import queue, queue_empty

from dsms.util import pretty_file_size

_BAR_SIZE = 20
_KILOBYTE = 1024
_FINISHED_BAR = '#'
_REMAINING_BAR = '-'

_UNKNOWN_SIZE = '?'
_STR_MEGABYTE = ' MB'

_HOURS_OF_ELAPSED = '%d:%02d:%02d'
_MINUTES_OF_ELAPSED = '%02d:%02d'

_RATE_FORMAT = '%5.2f'
_PERCENTAGE_FORMAT = '%3d%%'
_HUMANINZED_FORMAT = '%0.2f'

_DISPLAY_FORMAT = '|%s| %s/%s %s [elapsed: %s left: %s, %s MB/sec]'

_REFRESH_CHAR = '\r'


class AlarmHelper:
  def __init__(self, progress):
    self.last_send_ts = 0
    self.progress = progress

  def send(self, msg, force=False):
    interval = self.progress.interval
    cur = time.time()
    diff = cur - self.last_send_ts
    if diff > interval or force:
      self.progress.sdk.send(msg)
      self.last_send_ts = time.time()


class MinioProgress(Thread):
  def __init__(self, sdk, interval=60 * 5, stdout=sys.stdout):
    Thread.__init__(self)
    self.sdk = sdk
    self.daemon = True
    self.total_length = 0
    self.interval = interval
    self.object_name = None

    self.last_printed_len = 0
    self.current_size = 0
    self.force_send = False

    self.display_queue = queue()
    self.initial_time = time.time()
    self.stdout = stdout

    self.alarm_helper = AlarmHelper(self)

    self.start()

  def set_meta(self, total_length, object_name):
    msg = '''Start put object, project: %s, bucket: %s, size: %s, file: %s''' % (
      self.sdk.project_id,
      self.sdk.bucket_id,
      pretty_file_size(total_length),
      object_name)
    logging.debug(msg)
    self.total_length = total_length
    self.object_name = object_name
    self.prefix = self.object_name + ': ' if self.object_name else ''

    if int(total_length) > 100 * 1000 * 1000:
      self.force_send = True
    self.alarm_helper.send(msg, force=self.force_send)

  def run(self):
    logging.debug('run')
    displayed_time = 0
    while True:
      try:
        # display every interval secs
        task = self.display_queue.get(timeout=self.interval)
      except queue_empty:
        elapsed_time = time.time() - self.initial_time
        if elapsed_time > displayed_time:
          displayed_time = elapsed_time
        self.print_status(current_size=self.current_size,
                          total_length=self.total_length,
                          displayed_time=displayed_time, prefix=self.prefix)
        continue

      current_size, total_length = task
      displayed_time = time.time() - self.initial_time
      self.print_status(current_size=current_size, total_length=total_length,
                        displayed_time=displayed_time, prefix=self.prefix)
      self.display_queue.task_done()
      if current_size == total_length:
        self.done_progress()

  def update(self, size):
    logging.debug('update: size(%s)' % size)
    if not isinstance(size, int):
      raise ValueError('{} type can not be displayed. '
                       'Please change it to Int.'.format(type(size)))

    self.current_size += size
    self.display_queue.put((self.current_size, self.total_length))

  def done_progress(self):
    msg = '''Done put object, project: %s, bucket: %s''' % (
      self.sdk.project_id,
      self.sdk.bucket_id)
    self.alarm_helper.send(msg, force=self.force_send)
    logging.debug(msg)
    self.total_length = 0
    self.object_name = None
    self.last_printed_len = 0
    self.current_size = 0
    self.force_send = False

  def print_status(self, current_size, total_length, displayed_time, prefix):
    logging.debug('print_status (%s, %s, %s, %s)' % (
      current_size, total_length, displayed_time, prefix))

    formatted_str = prefix + format_string(current_size, total_length,
                                           displayed_time)
    self.alarm_helper.send(formatted_str)

    self.stdout.write(_REFRESH_CHAR + formatted_str + ' ' * max(
      self.last_printed_len - len(formatted_str), 0))
    self.stdout.flush()
    self.last_printed_len = len(formatted_str)


def seconds_to_time(seconds):
  minutes, seconds = divmod(int(seconds), 60)
  hours, m = divmod(minutes, 60)
  if hours:
    return _HOURS_OF_ELAPSED % (hours, m, seconds)
  else:
    return _MINUTES_OF_ELAPSED % (m, seconds)


def format_string(current_size, total_length, elapsed_time):
  if current_size <= 0:
    return ''

  n_to_mb = current_size / _KILOBYTE / _KILOBYTE
  elapsed_str = seconds_to_time(elapsed_time)

  rate = _RATE_FORMAT % (
        n_to_mb / elapsed_time) if elapsed_time else _UNKNOWN_SIZE
  frac = float(current_size) / total_length
  bar_length = int(frac * _BAR_SIZE)
  bar = _FINISHED_BAR * bar_length + _REMAINING_BAR * (_BAR_SIZE - bar_length)
  percentage = _PERCENTAGE_FORMAT % (frac * 100)
  left_str = seconds_to_time(
    elapsed_time / current_size * (
          total_length - current_size)) if current_size else _UNKNOWN_SIZE

  humanized_total = _HUMANINZED_FORMAT % (
        total_length / _KILOBYTE / _KILOBYTE) + _STR_MEGABYTE
  humanized_n = _HUMANINZED_FORMAT % n_to_mb + _STR_MEGABYTE
  return _DISPLAY_FORMAT % (
    bar, humanized_n, humanized_total, percentage, elapsed_str, left_str, rate)
