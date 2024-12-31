import importlib
import pkgutil
from argparse import ArgumentParser
from pathlib import Path

from todo.commands.base import BaseCommand
from todo.db import DB, create_db


class TodoCLI:
    def __init__(self):
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(title='commands', dest='command_name')

        self.command_map = {}
        self.process_commands()

        self.db: DB

    def init_data(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        create_db(path, 'todo')
        self.db = DB(path / 'todo.db')

    def run(self):
        self.init_data(Path.home() / '.todo')

        args = self.parser.parse_args().__dict__
        command_name = args.pop('command_name', None)
        if command_name is None:
            return None
        self.command_map[command_name].handle(**args)

    def process_commands(self):
        self.command_map = self.get_commands('todo.commands')
        for name, instance in self.command_map.items():
            command_parser = self.subparsers.add_parser(name)
            instance.add_arguments(command_parser)

    def get_commands(self, module_name: str) -> dict[str, BaseCommand]:
        return {
            command_name: self.load_command_class(f'{module_name}.{command_name}')
            for _, command_name, ispkg in pkgutil.iter_modules(importlib.import_module(module_name).__path__)
            if not ispkg and not command_name.startswith('_') and command_name != 'base'
        }
    
    def load_command_class(self, module_name: str) -> BaseCommand:
        module = importlib.import_module(module_name)
        command_class = getattr(module, 'Command')
        return command_class()
