import asyncio
from contextlib import contextmanager

from .node import Node
from .nodes.flow import Enter
from .exceptions import ReturnException, NotCallableError


class Group(Node):
    def __init__(
        self,
        nodes: [Node] = [],
        *ignore_args,
        **node_options,
    ):
        super().__init__(**node_options)

        for node in nodes:
            node.set_parent(self)

    async def __call__(self, scope: dict = None, **inputs):
        enter_nodes = tuple(self.find_children(Enter))
        if not enter_nodes:
            raise NotCallableError()

        with self.runtime_context(scope):
            await self.set_inputs(inputs)
            try:
                await asyncio.gather(*(
                    enter_node.enter()
                    for enter_node in enter_nodes
                ))
            except ReturnException:
                pass
            return await self.get_output()

    def __iter__(self):
        children = self.get_children()
        for child in children:
            yield child.get_name(), dict(child)

    def get_unique_name(self, name: str) -> str:
        curr_name = name
        count = 0
        while True:
            child = self.find_child(curr_name)
            if not child:
                return curr_name
            count += 1
            curr_name = '{}_{:02}'.format(name, count)

    def group(self, nodes: ['Node'], *ignore_args, **node_options) -> 'Group':
        grp = Group(nodes, parent=self, **node_options)
        return grp

    def ungroup(self):
        parent = self._parent
        if parent:
            for child in list(self.get_children()):
                child.set_parent(parent)
            self.set_parent(None)
            del self

    @contextmanager
    def runtime_context(self, scope: dict = None):
        original_state = self._state
        runtime_state = {
            **original_state,
            'scope': scope or {},
        }
        try:
            self._state = runtime_state
            yield runtime_state
        finally:
            self._state = original_state
