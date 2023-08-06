import time
from concurrent.futures import thread
from multiprocessing import Process
from pprint import pprint

from library import config_manager
from library.commands.command_base import BaseCommand

PROCESS_COUNT = 2


class MultiCommand(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        worker_num = self.get_worker_num()
        processes = list(range(worker_num))
        for i in range(worker_num):
            worker = self.get_worker(worker_num)
            time.sleep(1)

            processes[i] = Process(target=self.worker_wrapper, args=(i, worker))
            processes[i].start()

    def get_redis_client(self):
        return config_manager.get_redis()

    def get_redis_key(self):
        return "scrapy_word_list"

    def get_worker_num(self):
        return PROCESS_COUNT

    @staticmethod
    def get_word(redis_client, redis_key):
        if not redis_client.scard(redis_key):
            return False

        word = redis_client.spop(redis_key)

        if not word:
            return False

        if not isinstance(word, str):
            word = word.decode("utf-8")
        return word

    def worker_wrapper(self, worker_num, worker):
        print(worker_num)
        worker.init_worker(worker_num)
        redis_client = self.get_redis_client()
        redis_key = self.get_redis_key()

        one_word = self.get_word(redis_client, redis_key)
        while one_word:
            worker.process(one_word, worker_num)
            one_word = self.get_word(redis_client, redis_key)

    def get_worker(self, worker_num):
        """
        :return:
        :rtype: MultiWorker
        """
        raise NotImplemented("需要woker")


class MultiWorker:
    def init_worker(self, worker_num):
        pass

    def finish_worker(self, worker_num):
        pass

    def process(self, word, worker_num):
        raise NotImplemented("实现一下处理过程")
