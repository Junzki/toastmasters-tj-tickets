# -*- coding: utf-8 -*-
from __future__ import annotations

import os.path
import typing as ty  # noqa: F401
import importlib
import platform
import ntpath
import posixpath

from common.settings import settings
from tickets.loaders.base import AbstractLoader


class LoaderRegistry(object):

    _MODULE_NAME = 'tickets.loaders'

    def __init__(self, loaders: ty.Dict[str, ty.Type[AbstractLoader]] = None):
        if not loaders:
            loaders = dict()

        self.loaders = loaders
        self.autodiscover()

    def autodiscover(self):
        mod = importlib.import_module(self._MODULE_NAME)
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and issubclass(obj, AbstractLoader) and obj is not AbstractLoader:
                self.loaders[obj.OUTPUT_SCHEMA] = obj

    def find_loader(self, loader_name: str, **kwargs) -> ty.Type[AbstractLoader]:
        loader_klass = self.loaders.get(loader_name)
        if not loader_klass:
            raise ValueError(f'No loader found for {loader_name}')

        return loader_klass


class LoadDispatcher(object):

    @staticmethod
    def test_abs_path(path: str) -> str:
        if platform.system() == 'Windows':
            return ntpath.abspath(path)
        else:
            return posixpath.abspath(path)

    def __init__(self):
        self.loader_registry = LoaderRegistry()

    def load_data(self, task_defs: ty.List[ty.Dict[str, str]], base_dir: str = None):
        if not base_dir:
            base_dir = settings.BASE_DIR

        for task in task_defs:
            loader_klass = self.loader_registry.find_loader(task['loader'])
            path = task['path']
            sheet_name = task.get('sheet_name', 'Sheet 1')
            extras = task.get('extras', dict())

            if self.test_abs_path(path) != path:
                path = os.path.join(base_dir, path)

            loader = loader_klass()
            loader.run(path=path, sheet_name=sheet_name, **extras)
