from asyncio import gather
from collections import defaultdict
from typing import TYPE_CHECKING
import inspect

from .port import Direction, Port
from .signal import Signal
if TYPE_CHECKING:
    from .node import Node


def _port_creator(direction: Direction, options: dict) -> callable:
    def create_port(node: 'Node', name: str, **overrides) -> Port:
        return Port(
            node,
            name=name,
            direction=direction,
            **{**options, **overrides},
        )

    def assign_getter(fn):
        create_port.__schema__['getter_name'] = fn.__name__
        return fn

    create_port.__schema__ = {'group': 'ports', 'direction': direction}
    create_port.getter = assign_getter

    return create_port


def node(*args, name: str = '', output_name: str = 'result'):
    def create_simple_node(fn):
        from .node import Node

        spec = inspect.getfullargspec(fn)
        attributes = {}
        if spec.defaults:
            defaults = dict(zip(*(
                spec.args[len(spec.defaults):], spec.defaults
            )))
        else:
            defaults = {}

        for arg in spec.args:
            annotation = spec.annotations[arg]
            attributes[arg] = input(
                default=defaults.get(arg),
                is_list=getattr(annotation, '_name', '') == 'List',
                is_dict=getattr(annotation, '_name', '') == 'Dict',
            )

        output_port = output()
        attributes[output_name] = output_port

        @output_port.getter
        async def get_output(inst):
            args = await gather(*(getattr(inst, arg)() for arg in spec.args))
            if inspect.iscoroutinefunction(fn):
                return await fn(*args)
            return fn(*args)

        node_group = inspect.getmodule(fn).__name__.split('.')[-1]
        node_name = fn.__name__.title().replace('_', '')
        node_type = '{}.{}'.format(node_group, node_name)

        attributes['get_output'] = get_output
        attributes['__schema__'] = {
            'type': node_type,
        }

        type(node_name, (Node,), attributes)
        return fn

    if len(args) == 1:
        return create_simple_node(args[0])
    return create_simple_node


def input(**options):
    return _port_creator(Direction.Input, options)


def output(**options):
    return _port_creator(Direction.Output, options)


def signal(**signal_options):
    def create_signal(node: 'Node', name: str) -> Signal:
        return Signal(name=name, **signal_options)
    create_signal.__schema__ = {'group': 'signals', **signal_options}
    return create_signal


def slot(*args, name: str = '', default: bool = False):
    def decorated(fn):
        fn.__schema__ = {
            'group': 'slots',
            'name': name or fn.__name__.strip('_')
        }
        if default:
            fn.__schema__['default'] = True
        return fn
    if len(args) == 1:
        return decorated(args[0])
    return decorated


def generate_schema(model, attributes):
    schema = defaultdict(list)

    for prop_name, prop in attributes.items():
        try:
            prop_schema = getattr(prop, '__schema__')
        except AttributeError:
            continue
        else:
            prop_schema.setdefault('name', prop_name)
            schema[prop_schema.pop('group')].append(prop_schema)

    base_schema = attributes.get('__schema__', {})
    model_schema = {**base_schema, **schema}

    default_group = inspect.getmodule(model).__name__.rsplit('.', 1)[-1]
    default_name = model.__name__
    default_type = '{}.{}'.format(default_group, default_name)
    model_schema.setdefault('type', default_type)

    return model_schema
