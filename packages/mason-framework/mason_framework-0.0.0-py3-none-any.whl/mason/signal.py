from asyncio import gather
from weakref import ref as WeakRef, WeakMethod
from inspect import ismethod


def make_ref(fn: callable) -> WeakRef:
    return WeakMethod(fn) if ismethod(fn) else WeakRef(fn)


class Signal:
    def __init__(
        self,
        *,
        name: str = '',
        default: bool = False,
    ):
        self._name = name
        self._slots = set()
        self._default = default

    def __iter__(self):
        slot_ids = []
        for slot_ref in self._slots:
            slot = slot_ref()
            if slot:
                slot_id = '{}.{}'.format(slot.__self__.get_id(), slot.__name__)
                slot_ids.append(slot_id)
        yield 'connect', slot_ids

    def connect(self, slot: callable) -> None:
        self._slots.add(make_ref(slot))

    def disconnect(self, slot: callable = None) -> None:
        if slot is not None:
            self._slots.remove(make_ref(slot))
        else:
            self._slots.clear()

    def get_default(self) -> bool:
        return self._default

    def get_slots(self):
        self._slots = set(slot for slot in self._slots if slot())
        return [slot() for slot in self._slots]

    async def emit(self):
        await gather(*(slot()() for slot in self._slots if slot()))

    def get_name(self) -> str:
        return self._name

    def is_modified(self) -> bool:
        return len(self._slots)

    default = property(get_default)
    name = property(get_name)
