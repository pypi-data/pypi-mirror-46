# -*- coding: utf-8 -*-
import multiprocessing
from pika.adapters.blocking_connection import BlockingChannel
from pika.compat import xrange

from library import config_manager, logger
from library.logger import get_global_logger

PROCESS_COUNT = 1


class BaseWorker(object):
    def __init__(self):
        pass


    def consume_one(self, item):
        """
        处理队列条目
        :param item:
        :return:
        """
        raise NotImplementedError('need queue name')

    def get_config_queue_exchange_route_name(self) -> tuple:
        """
        获取队列名,交换器，路由名
        :return:
        """
        raise NotImplementedError('need queue name')

    def start_consume(self):
        config, queue, exchange, route_key = self.get_config_queue_exchange_route_name()
        mq_client = config_manager.get_mq_client(config)
        channel: BlockingChannel = mq_client.channel()
        channel.queue_declare(queue, False, True, False, False)
        channel.exchange_declare(exchange, 'topic', False, True, False)
        channel.queue_bind(queue, exchange, route_key)
        # channel.queue_declare(queue)
        # channel.queue_bind(queue, exchange, route_key)
        channel.basic_consume(self.consumer, queue)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            pass

    def consumer(self, channel: BlockingChannel, method_frame, header_frame, body):
        try:
            body_json = body.decode("utf-8")
            self.consume_one(body_json)
        except Exception as ex:
            get_global_logger().error('处理失败{}, msg_info:{}'.format(str(ex), body))

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def start_worker(self):
        self.start_consume()
        try:
            while True:
                continue
        except KeyboardInterrupt:
            print(' [*] Exiting...')
