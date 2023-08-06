from pathlib import Path

import io
import ruamel.yaml
import voluptuous

import EasyCo

yaml = ruamel.yaml.YAML(typ='rt')
yaml.default_flow_style = False
yaml.default_style = False
yaml.width = 1000000
yaml.allow_unicode = True
yaml.sort_base_mapping_type_on_output = False


class ConfigFile(EasyCo.ConfigContainer):

    def __init__(self, path: Path):
        super().__init__()
        if isinstance(path, str):
            path = Path(path)
        self._path = path.resolve()
        if self._path.suffix == '':
            self._path = self._path.with_name(self._path.name + '.yml')

    def load(self):
        cfg = ruamel.yaml.comments.CommentedMap()
        if not self._path.parent.is_dir():
            raise FileNotFoundError(f'Configuration folder {self._path.parent} does not exist!')

        if self._path.is_file():
            with self._path.open('r', encoding='utf-8') as file:
                cfg = yaml.load(file)
            if cfg is None:
                cfg = ruamel.yaml.comments.CommentedMap()

        # add default values
        data_changed = self._update_yaml(cfg, insert_values=False)

        # validate - this also makes it a normal dict
        schema = {}
        self._update_schema(schema, insert_values=False)
        schema = voluptuous.Schema(schema)
        validated_cfg = schema(cfg)

        # update optional keys if we have them and write back to disk
        if data_changed:
            with self._path.open('w', encoding='utf-8') as file:
                yaml.dump(cfg, file)

        self._set_value(validated_cfg)

    def _print_created_cfg(self):
        cfg = ruamel.yaml.comments.CommentedMap()
        self._update_yaml(cfg, insert_values=False)

        tmp = io.StringIO()
        ruamel.yaml.YAML().dump(cfg, tmp)
        output = tmp.getvalue()
        print(output)
