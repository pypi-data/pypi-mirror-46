from typing import Any, Type, TYPE_CHECKING
import logging

from .library import get_library
from .port import Port
from .schema import generate_schema
from .signal import Signal

if TYPE_CHECKING:
    from .blueprint import Blueprint  # pragma: no cover
    from .group import Group  # pragma: no cover

logger = logging.getLogger(__name__)


class NodeMeta(type):
    """Type definition for a node"""
    def __new__(cls, clsname, supers, attributes):
        if attributes.pop('__abstract__', False):
            return type.__new__(cls, clsname, supers, attributes)

        model = type.__new__(cls, clsname, supers, attributes)
        model.__schema__ = schema = generate_schema(model, attributes)
        library = schema.get('library', get_library())
        if library:
            library.register(model)
        return model


class Node(metaclass=NodeMeta):
    """Base node execution module"""
    __abstract__ = True

    def __init__(
        self,
        *,
        name: str = '',
        parent: 'Node' = None,
        **values,
    ):
        super().__init__()

        self._name = name
        self._state = {}
        self._parent = None
        self._children = set()
        self._runner = None

        self._init_schema(values)
        if parent:
            self.set_parent(parent)

    def _init_schema(self, values: dict):
        schema = getattr(self, '__schema__', None)
        if not schema:
            return

        cls = type(self)
        schema_objs = schema.get('ports', []) + schema.get('signals', [])
        for item in schema_objs:
            name = item['name']
            creator = getattr(cls, name)
            kw = {}
            if name in values:
                kw['value'] = values[name]
            if 'getter_name' in item:
                kw['getter'] = getattr(self, item['getter_name'])
            setattr(self, name, creator(self, name, **kw))

    def __getitem__(self, key):
        parts = key.split('.')
        node = self

        for part in parts[:-1]:
            node = node.find_child(part)
            if not node:
                raise KeyError(key)

        name = parts[-1]
        result = (
            node.get_port(name)
            or node.get_signal(name)
            or node.get_slot(name)
            or node.find_child(name)
        )
        if result:
            return result
        raise KeyError(key)

    def __del__(self):
        if self._parent:
            self._parent._children.remove(self)

        for child in self.get_children():
            del child

    def __iter__(self):
        yield 'type', self.__schema__['type']

        port_info = {
            port_name: dict(port)
            for port_name, port in self.get_ports().items()
            if port.is_modified()
        }
        if port_info:
            yield from port_info.items()

        signal_info = {
            signal_name: dict(signal)
            for signal_name, signal in self.get_signals().items()
            if signal.is_modified()
        }
        if signal_info:
            yield from signal_info.items()

        children = self.get_children()
        if children:
            yield 'children', {
                child.get_name(): dict(child)
                for child in children
            }

    def get_blueprint(self) -> 'Blueprint':
        from .blueprint import Blueprint
        return self.get_first_ancestor(Blueprint)

    def get_children(self) -> ['Node']:
        return self._children

    async def get_data(self) -> dict:
        data_root = self.get_data_root()
        return await data_root.get_state('data') or {}

    def get_data_root(self) -> 'Node':
        return self.get_group() or self

    async def get_data_value(self, key: str, default: Any) -> Any:
        data = await self.get_data()
        return data.get(key, default)

    def get_id(self) -> str:
        node = self._parent
        names = [self.get_name()]
        while node and node._parent:
            names.append(node.get_name())
            node = node._parent
        return '.'.join(reversed(names))

    def get_ports(self) -> ['Port']:
        return {
            port_schema['name']: getattr(self, port_schema['name'])
            for port_schema in self.__schema__.get('ports', [])
        }

    def get_group(self) -> 'Group':
        from .group import Group
        return self.get_first_ancestor(Group)

    def get_first_ancestor(self, node_type: Type['Node']) -> 'Node':
        node = self._parent
        while node and not isinstance(node, node_type):
            node = node._parent
        return node

    def get_name(self) -> str:
        return self._name

    def get_scope_root(self) -> 'Node':
        from .blueprint import Blueprint
        from .group import Group

        node = self
        scope_root = self
        while node:
            if isinstance(node, Blueprint):
                return node
            elif isinstance(node, Group):
                scope_root = node
            node = node._parent
        return scope_root

    def get_root(self) -> 'Node':
        node = self._parent
        while node and node._parent:
            node = node._parent
        return node

    def get_parent(self) -> 'Node':
        return self._parent

    def get_port(self, name: str) -> Port:
        port = getattr(self, name, None)
        return port if isinstance(port, Port) else None

    def get_signal(self, name: str) -> 'Signal':
        signal = getattr(self, name, None)
        return signal if isinstance(signal, Signal) else None

    def get_signals(self) -> ['Signal']:
        return {
            signal_schema['name']: getattr(self, signal_schema['name'])
            for signal_schema in self.__schema__.get('signals', [])
        }

    def get_slot(self, name: str) -> callable:
        slot = getattr(self, name, None)
        return slot if hasattr(slot, '__schema__') else None

    def get_slots(self) -> [callable]:
        return {
            slot_schema['name']: getattr(self, slot_schema['name'])
            for slot_schema in self.__schema__.get('slots', [])
        }

    async def get_inputs(self) -> dict:
        scope_root = self.get_scope_root()
        return await scope_root.get_state('inputs') or {}

    async def get_input_value(self, key: str, default: Any = None) -> Any:
        inputs = await self.get_inputs()
        return inputs.get(key, default)

    async def get_output(self) -> dict:
        scope_root = self.get_scope_root()
        return await scope_root.get_state('output') or {}

    async def get_output_value(self, key: str, default: Any) -> Any:
        output = await self.get_output()
        return output.get(key, default)

    async def get_state(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def find_child(
        self,
        name: str,
        recursive: bool = False,
        node_type: Type['Node'] = None
    ) -> 'Node':
        children = self.get_children()
        for child in children:
            if node_type is None or isinstance(child, node_type):
                if child.get_name() == name:
                    return child

            if recursive:
                found = child.find_child(name, recursive=True)
                if found:
                    return found

        return None

    def find_children(
        self,
        node_type: Type['Node'],
        recursive: bool = False,
    ) -> ['Node']:
        children = self.get_children()
        for child in children:
            if isinstance(child, node_type):
                yield child
            if recursive:
                yield from child.find_children(node_type, recursive=True)

    async def reset_state(self):
        self._state = {}

    async def set_data(self, data: dict):
        data_root = self.get_data_root()
        await data_root.set_state('data', data)

    async def set_data_value(self, key: str, value: Any):
        data = await self.get_data()
        data[key] = value
        await self.set_data(data)

    def set_name(self, name: str):
        self._name = name

    async def set_inputs(self, inputs: dict):
        scope_root = self.get_scope_root()
        await scope_root.set_state('inputs', inputs)

    async def set_input_value(self, key: str, value: Any):
        inputs = await self.get_inputs()
        inputs[key] = value
        await self.set_inputs(inputs)

    async def set_output(self, output: dict):
        scope_root = self.get_scope_root()
        await scope_root.set_state('output', output)

    async def set_output_value(self, key: str, value: Any):
        output = await self.get_output()
        output[key] = value
        await self.set_output(output)

    def set_parent(self, parent: 'Node'):
        if self._parent:
            self._parent._children.remove(self)

        if parent:
            self._parent = parent
            parent._children.add(self)

    async def set_state(self, key: str, value: Any) -> None:
        self._state[key] = value
