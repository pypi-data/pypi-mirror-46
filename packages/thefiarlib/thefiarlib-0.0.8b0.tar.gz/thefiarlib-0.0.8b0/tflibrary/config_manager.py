# coding=utf8
import os

from pika import BlockingConnection

from config.settings import CONFIG_DIR

import redis
from pymongo import MongoClient
import importlib.machinery
from elasticsearch import Elasticsearch
from .tf_oss import TfOss
import pika

redis_client = {}
mongo_client = {}
elasticsearch_client = {}
oss_client = {}
rabitmq_client = {}


def get_config(module_config, config_name):
    """
    根据配置名称返回配置
    :param module_config:
    :param config_name:
    :return:
    """
    path = os.path.join(CONFIG_DIR, module_config + "_cnf.py")
    # print(path)
    module_config = importlib.machinery.SourceFileLoader(module_config, path).load_module()

    if module_config and hasattr(module_config, config_name):
        return getattr(module_config, config_name)
    else:
        raise Exception("没有该配置文件，或者配置名称错误")


def get_redis(name='default', force_new=True) -> redis.StrictRedis:
    """
    获取redis链接
    :param force_new:
    :param name:
    :return:
    :rtype: redis.StrictRedis
    """
    if force_new:
        redis_config = get_config("redis", name)
        return redis.StrictRedis(**redis_config)

    if name not in redis_client:
        redis_config = get_config("redis", name)
        redis_client[name] = redis.StrictRedis(**redis_config)
    return redis_client[name]


def get_elasticsearch(name="default", force_new=False) -> Elasticsearch:
    """
    获取es client
    :param name:
    :param force_new:
    :return:
    :rtype: Elasticsearch
    """
    if force_new:
        elasticsearch_config = get_config("es", name)
        return Elasticsearch(hosts=[elasticsearch_config])

    if name not in elasticsearch_client:
        elasticsearch_config = get_config("es", name)
        elasticsearch_client[name] = Elasticsearch(hosts=[elasticsearch_config])

    return elasticsearch_client[name]


def get_mongo(name='default', force_new=False) -> MongoClient:
    """
    获取 MongoClient
    :param force_new:
    :param name:
    :return:
    :rtype: MongoClient
    """
    mongo_config = get_config("mongo", name)
    if not force_new and name in mongo_client:
        pass
    else:
        mongo_client[name] = MongoClient(**mongo_config)
    return mongo_client[name]


def get_oss_bucket(name='', force_new=False) -> TfOss:
    """
    获取oss对象
    :param name:
    :param force_new:
    :return:
    :rtype: TfOss
    """
    oss_config = get_config("oss", name)
    if not force_new and name in oss_client:
        pass
    else:
        oss_client[name] = TfOss(oss_config)
    return oss_client[name]


def get_mq_client(name='default', force_new=False) -> BlockingConnection:
    """
    获取mq client
    :param name: 配置名称
    :param force_new: 是否强制
    :return:
    """
    rabbitmq_config = get_config("rabbitmq", name)
    if not force_new and name in rabbitmq_config:
        pass
    else:
        credentials = pika.PlainCredentials(rabbitmq_config['user'], rabbitmq_config['pass'])
        rabitmq_client[name] = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmq_config['host'],
            virtual_host=rabbitmq_config['vhost'],
            port=rabbitmq_config['port'],
            credentials=credentials
        )
        )
    return rabitmq_client[name]

def get_cred_path(name=''):
    pass