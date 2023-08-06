import weakref

from typing import Any
from enum import Enum

from .exceptions import ConnectionError
from .signal import Signal


class Direction(Enum):
    Input = 'input'
    Output = 'output'


class Port:
    """Data link class."""

    def __init__(
        self,
        node,
        *,
        name: str,
        direction: Direction,
        enum: Enum = None,
        title: str = '',
        value: Any = None,
        default: Any = None,
        is_list: bool = False,
        is_dict: bool = False,
        getter: callable = None,
        setter: callable = None,
    ):
        self.node = node
        self.enum = enum
        self.is_dict = is_dict
        self.is_list = is_list
        self.title = title

        self._cached_value = None
        self._connections = []
        self._direction = direction
        self._name = name
        self._value = None
        self._default = default
        self._getter = getter
        self._setter = setter

        if value is not None:
            if isinstance(value, Port):
                self.connect(value)
            else:
                self._value = value
        elif default is not None:
            self._value = default

        self.changed = Signal()

    def __iter__(self):
        if self.title:
            yield 'title', self.title
        if self._value is not None:
            yield 'value', self._value

        if self.get_direction() == Direction.Input:
            conns = self.get_connections()
            if conns:
                yield 'connect', [port.get_id() for port in conns]

    async def __call__(self):
        return await self.get_value()

    async def _calculate_value(self) -> Any:
        conn = self.get_connections()
        if self._direction == Direction.Output:
            return await self._getter() if self._getter else self._value
        elif conn and self.is_list:
            return [await port.get_value() for port in conn]
        elif conn and self.is_dict:
            return {p.get_name(): await p.get_value() for p in conn}
        elif conn:
            return await conn[0].get_value()
        else:
            return await self._getter() if self._getter else self._value

    def can_connect(self, other: "Port") -> None:
        """Return whether or not this port can connect to the other"""
        if self._direction == Direction.Output:
            return other.can_connect(self)
        return (
            len(self.get_connections()) == 0
            or self.is_list
            or self.is_dict
        )

    def connect(self, other: "Port") -> None:
        """Creates a connection between this and another port."""
        if self._direction == Direction.Output:
            other.connect(self)
        elif self.can_connect(other):
            self._connections.append(weakref.ref(other))
            other._connections.append(weakref.ref(self))
        else:
            raise ConnectionError()

    def disconnect(self, other: "Port" = None) -> None:
        """Removes connection between this port and another."""
        if other:
            self._connections.remove(weakref.ref(other))
            other._connections.remove(weakref.ref(self))
        else:
            for other in self._connections:
                other._connections.remove(weakref.ref(self))
            self._connections = []

    def get_connections(self) -> ["Port"]:
        self._connections = [conn for conn in self._connections if conn()]
        return [conn() for conn in self._connections]

    def get_id(self) -> str:
        return '.'.join((self.node.get_id(), self.get_name()))

    def get_name(self) -> str:
        """Return the name of this node."""
        return self._name

    def get_direction(self) -> Direction:
        return self._direction

    async def get_value(self) -> Any:
        """Returns the value for this port"""
        return await self._calculate_value()

    def is_modified(self) -> bool:
        return (
            self._value is not None
            or (self._connections and self.get_direction() == Direction.Input)
        )

    async def reset(self) -> None:
        self._value = self._default

    def set_getter(self, method: callable) -> None:
        """Sets the default getter method for this port."""
        self._getter = method

    async def set_value(self, value: Any) -> None:
        """Sets the local value for this port."""
        if value != self._value:
            await self.changed.emit()
        self._value = value
