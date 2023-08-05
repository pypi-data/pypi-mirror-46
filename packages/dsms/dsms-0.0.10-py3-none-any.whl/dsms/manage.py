#!/usr/bin/env python3

import os
import logging

import colorlog
import fire

from dsms.command import Command


def set_driver_logger(log_dir, level=logging.INFO):
  logging.debug('_set_logger : %s', level)
  import os
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
  filename = os.path.join(log_dir, 'cun_driver.log')
  fmt = '%(asctime)s - %(levelname)s %(name)s %(filename)s::%(funcName)s(%(lineno)d)\t%(message)s'
  handler = colorlog.StreamHandler()
  handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s' + fmt))

  logging.basicConfig(
    format=fmt,
    level=level,
    handlers=[handler, logging.FileHandler(filename)])


def main():
  debug = os.environ.get('DEBUG')
  if debug:
    level = logging.DEBUG
    set_driver_logger(log_dir='/tmp', level=level)
  else:
    level = logging.INFO
    logging.basicConfig(level=level)
  # logging.info('main')
  fire.Fire(Command)


if __name__ == '__main__':
  main()
