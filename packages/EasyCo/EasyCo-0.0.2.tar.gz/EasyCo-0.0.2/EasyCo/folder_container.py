from pathlib import Path
from . import ConfigContainer


class FolderContainer(ConfigContainer):
    def __init__(self):
        self.parent_folder: Path = None
        super().__init__()

    def get_value_validator(self, var_name: str, var_type):
        return super().get_value_validator(var_name, var_type)

    def set_value_from_file(self, var_name: str, new_value):
        if not isinstance(new_value, str):
            return new_value

        path = Path(new_value)
        if not path.is_absolute():
            path = self.parent_folder / path
        return path.resolve()

    def _set_default_path(self, path: Path):
        if self.parent_folder is None:
            self.parent_folder = path
        super()._set_default_path(path)
