from contextlib import contextmanager
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node  # pragma: no cover

_library = None


class Library:
    def __init__(self):
        self._node_types = {}

    def create(self, type_name: str, *args, **options) -> 'Node':
        node_type = self._node_types[type_name]
        return node_type(*args, **options)

    def get_type(self, type_name: str) -> Type['Node']:
        return self._node_types[type_name]

    def register(self, model: Type['Node']) -> None:
        self._node_types[model.__schema__['type']] = model


def get_library() -> Library:
    global _library
    if not _library:
        _library = Library()
    return _library


def set_library(library: Library) -> None:
    global _library
    _library = library


@contextmanager
def library_context(library: Library):
    global _library
    orig_library = _library
    try:
        _library = library
        yield library
    finally:
        _library = orig_library
