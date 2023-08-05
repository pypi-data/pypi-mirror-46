from terminaltables import AsciiTable

from .util import (
  pretty_date, pretty_file_size
)


class Display:
  def print_bucket_detail(self, data, bucket_id):
    header = ['key',
              'size',
              'last_modified']
    table_data = [
      [
        v['key'],
        pretty_file_size(v['size']),
        v['lastModified'],
      ]
      for v in data
    ]

    total_size = sum([int(v['size']) for v in data])
    table_data.insert(0, header)
    table_data.append([
      '# total file size in buckets',
      pretty_file_size(total_size),
      ''])
    table = AsciiTable(table_data)
    print('\n# Bucket detail: %s' % bucket_id)
    print(table.table)

  def print_bucket_ls(self, data):
    header = ['bucket_id',
              'last_modified']
    table_data = [
      [
        v['key'],
        v['lastModified'],
      ]
      for v in data
    ]
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print('\n# Bucket list')
    print(table.table)

  def print_history_detail(self, tid, data, debug=False):
    print('\n# History detail: tid(%s)' % tid)
    if debug:
      header = ['success',
                'hostname',
                'title',
                'msg']
      table_data = data
      table_data.insert(0, header)
      table = AsciiTable(table_data)
      print(table.table)
    else:
      header = ['success',
                'hostname',
                'title']
      table_data = [
        [
          v[0],
          v[1],
          v[2],
        ]
        for v in data
      ]
      table_data.insert(0, header)
      table = AsciiTable(table_data)
      print(table.table)

  def print_history(self, data):
    header = ['tid',
              'hostname',
              'title',
              'live_node_count',
              'success',
              'fail',
              'start_at']
    table_data = [
      [
        v['tid'],
        v['hostname'],
        v['title'],
        v['live_node_count'],
        v['success_count'],
        v['fail_count'],
        pretty_date(int(v['ts']))
      ]
      for v in data
    ]
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print('\n# History')
    print(table.table)

  def print_basic_info(self, nodes):
    header = ['hostname', 'free_disk_gb']
    table_data = [
      [
        v['hostname'],
        '%.2f G' % (v['disk_usage']['free'] / (1024 * 1024 * 1024))
      ]
      for v in nodes
    ]

    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print('\n# Basic info')
    print(table.table)

  def print_diff_local(self, data):
    data = [x for x in data if x['diff'] != 2]
    print('\n# Diff list')
    header = ['local', 'remote']
    table_data = [[x['first'], x['second']] for x in data]
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print(table.table)

    header = ['local only #', 'remote only #', 'size diff #']
    table_data = [[
      len([x for x in data if x['diff'] == 4]),
      len([x for x in data if x['diff'] == 5]),
      len([x for x in data if x['diff'] == 1]),
    ]]
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print('\n# Diff summary')
    print(table.table)

  def _get_hostname(self, nodes, k):
    f = [v for v in nodes if v['key'] == k]
    if len(f) == 0:
      return ''
    return f[0]['hostname']

  def print_diff_nodes(self, project, nodes, diff_data):
    # https://docs.min.io/docs/minio-client-complete-guide.html
    # -1 Error
    # 0 Does not differ
    # 1 Differs in size
    # 2 Differs in time
    # 3 Differs in type exfile / directory
    # 4 Only in source(FIRST)
    # 5 Only in target(SECOND)
    header = ['hostname', 'node only #', 'remote only #', 'size diff #',
              'diff_at']
    table_data = [
      [
        self._get_hostname(nodes, k),
        len([x for x in v['diff_list'] if x['diff'] == 4]),
        len([x for x in v['diff_list'] if x['diff'] == 5]),
        len([x for x in v['diff_list'] if x['diff'] == 1]),
        pretty_date(v['last_diff_ts'])
      ]
      for k, v in diff_data.items()
    ]
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    print('\n# Diffs: %s' % project)
    print(table.table)
