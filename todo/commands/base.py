from argparse import ArgumentParser
from typing import Any


class BaseCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def handle(self, **options: dict[str, Any]) -> None:
        raise NotImplementedError(
            'Subclasses of BaseCommand must implement handle().'
        )
