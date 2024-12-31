from pathlib import Path

from todo.db import create_db


class TodoCLI:
    def init_data(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        create_db(path, 'todo')


    def run(self):
        self.init_data(Path.home() / '.todo')
