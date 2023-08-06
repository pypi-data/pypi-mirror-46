#!/usr/bin/python3
# encoding=utf-8

import json as json
import os

config = None

'''
获取配置文件

- Mesos集群中自动获取 config.json 文件
- 本地自动加载当前组件目录的 config.json 文件
'''


def get_config():
    global config
    if config is not None:
        return config
    if os.environ.get("MESOS_SANDBOX") is not None:
        path = os.environ.get("MESOS_SANDBOX") + "/config.json"
    else:
        path = 'config.json'
    if path is None:
        print("[base.get_config] path is null")
        return {}
    # print "[base.get_config] path -> %s" % path
    if not os.path.exists(path):
        print("[base.get_config] path not exists")
        return {}
    file = open(path)
    config = json.load(file)
    if 'ENV_HDFS_URI' not in config:
        config['ENV_HDFS_URI'] = 'hdfs://192.168.1.251:8020/'
    if 'ENV_HDFS_ROOT' not in config:
        config['ENV_HDFS_ROOT'] = 'algo/'
    print("[base.get_config] config -> %s" % config)
    return config


'''
获取hdfs的uri
'''


def get_hdfs_uri():
    config = get_config()
    return config['ENV_HDFS_URI']


'''
获取hdfs根路径，固定为 algo/
'''


def get_hdfs_root():
    config = get_config()
    return config['ENV_HDFS_ROOT']


'''
统一处理hdfs路，统一转换为绝对路径，兼容以下几种格式，请务必在所有数据输入输出路径调用

- parquet/somepath
- /algo/parquet/somepath
- hdfs://xxx.xxx.xxx.xxx/algo/parquet/somepath
'''


def hdfs_normal_path(file):
    if file.startswith('/algo/'):
        return file
    elif file.startswith('hdfs://'):
        return file
    elif file.startswith('/'):
        return '/' + get_hdfs_root() + file
    else:
        return '/' + get_hdfs_root() + '/' + file


if __name__ == "__main__":
    get_config('config.test.json')
