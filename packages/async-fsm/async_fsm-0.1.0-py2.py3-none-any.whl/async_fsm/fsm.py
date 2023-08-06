

import asyncio
from asyncio import Queue

from .conf import settings
from . import messages


class _Channel(object):

    def __init__(self, from_fsm, to_fsm, tracer, queue=None):
        if queue is None:
            self.queue = Queue()
        else:
            self.queue = queue
        self.from_fsm = from_fsm
        self.to_fsm = to_fsm
        self.tracer = tracer

    async def put(self, item):
        await self.tracer.send_trace_message(messages.ChannelTrace(self.tracer.trace_order_seq(),
                                                                   self.from_fsm.fsm_id if self.from_fsm else None,
                                                                   self.to_fsm.fsm_id if self.to_fsm else None,
                                                                   item.__class__.__name__))
        await self.queue.put(item)

    async def get(self):
        return await self.queue.get()

    receive = get


def Channel(from_fsm, to_fsm, tracer, queue=None):
    if settings.instrumented:
        return _Channel(from_fsm, to_fsm, tracer, queue)
    if queue is not None:
        return queue
    else:
        return Queue()


class _NullChannel(object):

    def __init__(self):
        pass

    async def put(self, item):
        pass


NullChannelSingleton = _NullChannel()


class _NullChannelInstrumented(object):

    def __init__(self, from_fsm, tracer):
        self.from_fsm = from_fsm
        self.tracer = tracer

    async def put(self, item):
        await self.tracer.send_trace_message(messages.ChannelTrace(self.tracer.trace_order_seq(),
                                                                   self.from_fsm.fsm_id,
                                                                   None,
                                                                   item.__class__.__name__))


def NullChannel(from_fsm, tracer):

    if settings.instrumented:
        return _NullChannelInstrumented(from_fsm, tracer)
    else:
        return NullChannelSingleton


async def create_controller(context, name, fsm_id, initial_state, tracer, channel_tracer):

    controller = FSMController(context, name, fsm_id, initial_state, tracer, channel_tracer)
    controller.handling_message_type = 'start'
    await controller.state.start(controller)
    controller.handling_message_type = None
    return controller


class FSMController(object):

    def __init__(self, context, name, fsm_id, initial_state, tracer, channel_tracer):
        self.context = context
        self.name = name
        self.fsm_id = fsm_id
        self.tracer = tracer
        self.channel_tracer = channel_tracer
        self.state = initial_state
        self.inboxes = dict(default=Queue())
        self.outboxes = dict(default=NullChannel(self, channel_tracer))

    async def changeState(self, state):
        if self.state:
            try:
                old_handling_message_type = self.handling_message_type
                self.handling_message_type = 'end'
                await self.state.end(self)
            finally:
                self.handling_message_type = old_handling_message_type
        if settings.instrumented:
            await self.tracer.send_trace_message(messages.FSMTrace(self.tracer.trace_order_seq(),
                                                                   self.name,
                                                                   self.fsm_id,
                                                                   self.state.__class__.__name__[1:],
                                                                   state.__class__.__name__[1:],
                                                                   self.handling_message_type))
        self.state = state
        if self.state:
            try:
                old_handling_message_type = self.handling_message_type
                self.handling_message_type = 'start'
                await self.state.start(self)
            finally:
                self.handling_message_type = old_handling_message_type

    async def handle_message(self, message_type, message):
        try:
            old_handling_message_type = self.handling_message_type
            self.handling_message_type = message_type
            handler_name = "on{0}".format(message_type)
            handler = getattr(self.state, handler_name, self.default_handler)
            await handler(self, message_type, message)
        finally:
            self.handling_message_type = old_handling_message_type

    async def default_handler(self, controller, message_type, message):
        await self.outboxes.get('default', NullChannelSingleton).put(message)

    async def receive_messages(self):

        while True:
            await asyncio.sleep(0)
            if self.inboxes.get('default', None):
                inbox = self.inboxes.get('default')
                message = await inbox.get()
                if isinstance(message, messages.Shutdown):
                    break
                message_type = message.__class__.__name__
                await self.handle_message(message_type, message)
            else:
                break


class State(object):

    async def start(self, controller):
        pass

    async def end(self, controller):
        pass


def transitions(*args):
    def decorator(fn):
        fn.transitions = args
        return fn
    return decorator


class _NullTracer(object):

    def trace_order_seq(self):
        return 0

    async def send_trace_message(self, message):
        pass


NullTracer = _NullTracer()
