#!/usr/bin/env python3
# -*- coding:utf-8 -*-

###
# File: command_base.py
# File Created: Sunday, 17th March 2019 9:44:24 pm
# Author: Yin
###

import click
from click import Option

from app import app
import inspect

from library import logger
from library.pipeline.pipeline_manager import PipelineManager
from library.worker.worker_base import BaseWorker


class SameCommandException(Exception):
    def __init__(self, command_name):
        super().__init__("same command not allowed: command name {}".format(command_name))


def _default_args() -> list:
    return [
        Option(['--is_worker'], default=False)
    ]


class BaseCommand(click.Command, BaseWorker):
    # def consume_one(self, item):
    #     pass
    #
    # def get_config_queue_exchange_route_name(self) -> tuple:
    #     pass

    pipelines = {}

    def __init__(self):
        super().__init__('command')
        self.params = self.get_args() + self.get_options() + _default_args()
        self.logger = logger.get_global_logger()

    def get_args(self) -> list:
        # [Argument(['file'], {"nargs": -1})]
        return []

    def get_options(self) -> list:
        # [Option(['--fname'])]
        return []

    def set_app_name(self, app_name):
        self.app_name = app_name

    def invoke(self, ctx):
        self.params = ctx.params
        super().invoke(ctx)
        with app.app_context():
            if inspect.isgeneratorfunction(self.handle):
                # 导入pipeline
                items = self.handle(**ctx.params)
                for item in items:
                    pipe_manager = PipelineManager()
                    pipe_manager.add_pipelines(self.pipelines, self.app_name)
                    pipe_manager.process_item(item)
            else:
                if ctx.params.get('is_worker', False):
                    self.start_worker()
                else:
                    self.handle(**ctx.params)

    def handle(self, *args, **options):
        return []
