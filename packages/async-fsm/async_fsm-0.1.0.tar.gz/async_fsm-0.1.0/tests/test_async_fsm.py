#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `async_fsm` package."""

import pytest


from asyncio import Queue
from async_fsm import fsm
from async_fsm import messages
from async_fsm.conf import settings
from collections import namedtuple

class _Start(fsm.State):

    @fsm.transitions('A')
    async def onInput1(self, controller, *args):
        await controller.changeState(A)

    async def onInput3(self, controller, *args):
        await controller.outboxes['default'].put(Hello())

Start = _Start()


class _A(fsm.State):

    pass

A = _A()


Input1 = namedtuple('Input1', [])
Input2 = namedtuple('Input2', [])
Input3 = namedtuple('Input3', [])
Hello = namedtuple('Hello', [])


@pytest.mark.asyncio
async def test_no_inbox():
    fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
    fsm1.inboxes['default'] = None
    await fsm1.receive_messages()
    assert fsm1.state is Start


@pytest.mark.asyncio
async def test_shutdown():
    fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
    await fsm1.inboxes['default'].put(messages.Shutdown())
    await fsm1.receive_messages()
    assert fsm1.state is Start

@pytest.mark.asyncio
async def test_change_state():
    fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
    await fsm1.inboxes['default'].put(Input1())
    await fsm1.inboxes['default'].put(Input2())
    await fsm1.inboxes['default'].put(messages.Shutdown())
    await fsm1.receive_messages()
    assert fsm1.state is A

@pytest.mark.asyncio
async def test_change_state_instrumented():
    settings.instrumented = True
    try:
        fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
        await fsm1.inboxes['default'].put(Input1())
        await fsm1.inboxes['default'].put(Input2())
        await fsm1.inboxes['default'].put(messages.Shutdown())
        await fsm1.receive_messages()
        assert fsm1.state is A
    finally:
        settings.instrumented = False

@pytest.mark.asyncio
async def test_channels():
    fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
    fsm2 = await fsm.create_controller(dict(), 'foo', 2, Start, fsm.NullTracer, fsm.NullTracer)
    fsm1.outboxes['default'] = fsm.Channel(fsm1, fsm2, fsm.NullTracer)
    await fsm1.inboxes['default'].put(Input3())
    await fsm1.inboxes['default'].put(messages.Shutdown())
    await fsm1.receive_messages()
    assert fsm1.state is Start

@pytest.mark.asyncio
async def test_channels_with_queue():
    fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
    fsm2 = await fsm.create_controller(dict(), 'foo', 2, Start, fsm.NullTracer, fsm.NullTracer)
    fsm1.outboxes['default'] = fsm.Channel(fsm1, fsm2, fsm.NullTracer, Queue())
    await fsm1.inboxes['default'].put(Input3())
    await fsm1.inboxes['default'].put(messages.Shutdown())
    await fsm1.receive_messages()
    assert fsm1.state is Start

@pytest.mark.asyncio
async def test_channels_instrumented():
    settings.instrumented = True
    try:
        fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
        fsm2 = await fsm.create_controller(dict(), 'foo', 2, Start, fsm.NullTracer, fsm.NullTracer)
        fsm1.outboxes['default'] = fsm.Channel(fsm1, fsm2, fsm.NullTracer)
        await fsm1.inboxes['default'].put(Input3())
        await fsm1.inboxes['default'].put(messages.Shutdown())
        await fsm1.receive_messages()
        assert fsm1.state is Start
    finally:
        settings.instrumented = False

@pytest.mark.asyncio
async def test_channels_instrumented_with_queue():
    settings.instrumented = True
    try:
        fsm1 = await fsm.create_controller(dict(), 'foo', 1, Start, fsm.NullTracer, fsm.NullTracer)
        fsm2 = await fsm.create_controller(dict(), 'foo', 2, Start, fsm.NullTracer, fsm.NullTracer)
        fsm1.outboxes['default'] = fsm.Channel(fsm1, fsm2, fsm.NullTracer, Queue())
        fsm2.inboxes['default'] = fsm1.outboxes['default']
        await fsm1.inboxes['default'].put(Input3())
        await fsm1.inboxes['default'].put(messages.Shutdown())
        await fsm1.receive_messages()
        assert fsm1.state is Start
        assert isinstance(await fsm2.inboxes['default'].get(), Hello)
    finally:
        settings.instrumented = False
