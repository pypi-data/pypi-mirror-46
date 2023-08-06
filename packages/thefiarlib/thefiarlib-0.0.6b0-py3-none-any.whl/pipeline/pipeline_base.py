#!/usr/bin/env python3
# -*- coding:utf-8 -*-

###
# File: pipeline_base.py
# File Created: Friday, 15th March 2019 11:27:37 am
# Author: Yin
###
import abc

from library.logger import get_pipeline_logger


class DropItemException(Exception):
    pass

class PipelineBase(abc.ABC):
    def __init__(self, *args, **kw):
        super().__init__()
        self.logger = get_pipeline_logger(self.__class__.__name__)

    @abc.abstractmethod
    def process_item(self, item):
        """执行入口

        Args:
            item (mixed): 要处理的数据

        Returns:
            mixed: 要处理的数据
        """

        return item
