import re

camel_pat = re.compile(r'([A-Z])')
under_pat = re.compile(r'_([a-z])')


def camel_to_snake(name):
  return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)


def snake_to_camel(name):
  return under_pat.sub(lambda x: x.group(1).upper(), name)


def change_key_style(d, convert):
  new_d = {}
  for k, v in d.items():
    new_d[convert(k)] = change_key_style(v, convert) \
      if isinstance(v, dict) else v
  return new_d
