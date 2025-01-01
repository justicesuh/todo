from argparse import ArgumentParser
from datetime import datetime
from typing import Any

from todo.commands.base import NamespaceCommand
from todo.models import Color, Project
from todo.utils import tabulate


class Command(NamespaceCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('action', nargs='?', default='list')
        parser.add_argument('detail', nargs='*')

    def parse_detail(self, detail: list[str]):
        idx = len(detail)
        if idx == 0:
            return
        
        color = Color.DEFAULT
        last = detail[-1]
        if last.startswith(':'):
            idx = idx - 1
            color = getattr(Color, last[1:])

        name = ' '.join(detail[:idx])
        now = datetime.now()
        return Project(None, name, color, now, now)

    def handle(self, **options: Any) -> None:
        action: str = options['action']
        detail: list[str] = options['detail']
        match action:
            case 'list':
                query = 'SELECT * FROM projects;'
                records = self.db.fetch_all(query)
                data: list[Any] = []
                for record in records:
                    project = Project(*record)
                    data.append([str(project.id), project.name])
                print(tabulate(data, ['ID', 'Name']))
            case 'add':
                person = self.parse_detail(detail)
                if person is not None:
                    query = 'INSERT INTO projects (name, color, created_at, updated_at) VALUES (?, ?, ?, ?);'
                    params: list[Any] = [person.name, person.color.value, person.created_at.isoformat(), person.updated_at.isoformat()]
                    self.db.execute_query(query, params)
            case _:
                pass
