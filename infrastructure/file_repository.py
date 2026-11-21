import json
from pathlib import Path

class FileRepository:

    def __init__(self, filename="requests.json"):
        project_root = Path(__file__).resolve().parent.parent
        data_dir = project_root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        self._file_path = data_dir / filename

    @property
    def file_path(self):
        """Exposed so main.py can print it for verification."""
        return str(self._file_path)

    def load_all(self):
        if not self._file_path.exists():
            return []
        with open(self._file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

    def save_all(self, records):
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)