from typing import TYPE_CHECKING
import copy
import os

from .group import Group
from .library import Library, get_library
from .exceptions import UnknownExtensionError

if TYPE_CHECKING:
    from .node import Node  # pragma: no cover


class Blueprint(Group):
    def __init__(
        self,
        library: Library = None,
        *ignore_args,
        **group_options,
    ):
        super().__init__(**group_options)
        self._library = library

    def create(self, node_type: str, *node_args, **node_kwargs) -> 'Node':
        node_kwargs.setdefault('parent', self)
        if 'name' not in node_kwargs:
            basename = node_type.split('.')[-1].lower()
            node_kwargs['name'] = self.get_unique_name(basename)

        library = self.get_library()
        return library.create(node_type, *node_args, **node_kwargs)

    def get_library(self) -> Library:
        return self._library or get_library()

    def set_library(self, library: Library):
        self._library = library

    @classmethod
    def from_dict(cls, data: dict) -> 'Blueprint':
        _data = copy.deepcopy(data)
        inst = cls()
        connections = {}

        # load nodes
        for node_name, node_properties in _data.items():
            node_type = node_properties['type']
            inst.create(node_type, name=node_name)
            for prop_name, prop_values in node_properties.items():
                if type(prop_values) == dict:
                    prop_connect = prop_values.pop('connect', None)
                    if prop_connect:
                        key = '{}.{}'.format(node_name, prop_name)
                        connections[key] = prop_connect

        # setup connections
        for source_id, target_ids in connections.items():
            source = inst[source_id]
            for target_id in target_ids:
                target = inst[target_id]
                source.connect(target)

        return inst

    @classmethod
    def load(cls, filename: str) -> 'Blueprint':
        _, ext = os.path.splitext(filename)

        if ext in ('.yaml', '.yml'):
            import yaml
            with open(filename) as f:
                text = f.read()
            data = yaml.safe_load(text)

        elif ext in ('.json',):
            import json
            with open(filename) as f:
                data = json.load(f)

        else:
            raise UnknownExtensionError(ext)

        return cls.from_dict(data)
