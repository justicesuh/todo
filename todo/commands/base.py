from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from todo.db import DB


class BaseCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def handle(self, **options: Any) -> None:
        raise NotImplementedError(
            'Subclasses of BaseCommand must implement handle().'
        )


class NamespaceCommand(BaseCommand):
    namespace = None

    def __init__(self):
        self.db = DB(Path.home() / '.todo' / 'todo.db')

    def get_namespace(self):
        assert self.namespace is not None, (
            f'{self.__class__.__name__} must define .namespace or override get_namespace().'
        )
        return self.namespace
