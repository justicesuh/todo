from pathlib import Path


class TodoCLI:
    def init_data(self, path: Path):
        if path.exists():
            return
        path.mkdir(parents=True, exist_ok=True)

    def run(self):
        self.init_data(Path.home() / '.todo')
