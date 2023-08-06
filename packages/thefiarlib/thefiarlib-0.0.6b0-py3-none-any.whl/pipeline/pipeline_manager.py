#!/usr/bin/env python3
# -*- coding:utf-8 -*-

###
# File: pipeline_manager.py
# File Created: Friday, 15th March 2019 11:38:00 am
# Author: Yin
###

from importlib import import_module
from library.logger import get_pipeline_logger


class PipelineManager(object):
    def __init__(self):
        self.methods = {
            'process_item': []
        }

    def _process_chain(self, methodname, item):
        """按顺序执行pipe

        Args:
            methodname (string): 方法名
            item (mixed): 要处理的数据

        Returns:
            mixed: 要处理的数据
        """

        for callback in self.methods[methodname]:
            class_name = callback.__self__.__class__.__name__
            method_name = callback.__name__

            logger = get_pipeline_logger(class_name)
            log = "method<{0}.{1}> get in: {2}".format(class_name, method_name, str(item))
            logger.info(log)

            item = callback(item)

            log = "method<{0}.{1}> get out: {2}".format(class_name, method_name, str(item))
            logger.info(log)

        return item

    def _add_pipe(self, pipe):
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(pipe.process_item)

    def _load_object(self, path):
        """载入

        Args:
            path (string): pipe路径

        Raises:
            ValueError: [description]
            NameError: [description]

        Returns:
            obj: 类名
        """

        try:
            dot = path.rindex('.')
        except ValueError:
            raise ValueError("Error loading object '%s': not a full path" % path)

        module, name = path[:dot], path[dot+1:]
        mod = import_module(module)

        try:
            obj = getattr(mod, name)
        except AttributeError:
            raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

        return obj

    def add_pipelines(self, pipelines, app_name=''):
        """添加pipeline

        Args:
            pipelines (list): [[pipeline, sort, params]
        """

        pipelines.sort(key=lambda x: x[1])

        for pipe_item in pipelines:
            # 排序完成是list
            if len(pipe_item) < 3:
                raise Exception('commander pipeline config error, need [[path, sort, params],...]')

            pipe_path = app_name + '.pipelines.' + pipe_item[0]

            try:
                pipe = self._load_object(pipe_path)
            except ModuleNotFoundError:
                pipe = self._load_object(pipe_item[0])

            self._add_pipe(pipe(params=pipe_item[2]))

    def process_item(self, item):
        """按顺序调用pipe

        Args:
            item (mixed): item

        Returns:
            mixed: item
        """

        return self._process_chain('process_item', item)
