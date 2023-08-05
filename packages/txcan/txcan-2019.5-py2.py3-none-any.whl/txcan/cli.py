import logging
import threading

import click
import can
import twisted.internet.defer
import twisted.internet.task

import txcan

logger = logging.getLogger(__name__)


@click.command()
def main():
    root_logger = logging.getLogger()
    log_level = logging.DEBUG

    stderr_handler = logging.StreamHandler()
    root_logger.addHandler(stderr_handler)

    root_logger.setLevel(log_level)
    stderr_handler.setLevel(log_level)

    root_logger.debug('red green blue')

    react_inline_callbacks(inline_callbacks_main)


def react_inline_callbacks_helper(reactor, f, args, kwargs):
    deferred = f(reactor, *args, **kwargs)

    def cancel():
        deferred.cancel()
        return deferred

    reactor.addSystemEventTrigger('before', 'shutdown', cancel)

    return deferred


def react_inline_callbacks(f, *args, **kwargs):
    twisted.internet.task.react(
        react_inline_callbacks_helper,
        (f, args, kwargs),
    )


def sleep(clock, duration):
    return twisted.internet.task.deferLater(clock, duration, lambda: None)


@twisted.internet.defer.inlineCallbacks
def react_for(duration, clock, deferred):
    cancelled = [False]

    def cancel():
        cancelled[0] = True
        deferred.cancel()

    clock.callLater(duration, cancel)

    result = None

    try:
        result = yield deferred
    except twisted.internet.defer.CancelledError:
        if not cancelled[0]:
            raise

    return result


@twisted.internet.defer.inlineCallbacks
def inline_callbacks_main(reactor):
    can_bus = can.interface.Bus(bustype='socketcan', channel='can0')

    txcan_bus = txcan.Bus.build(bus=can_bus, reactor=reactor)

    with txcan_bus.linked():
        yield sleep(clock=reactor, duration=0.2)

        logger.debug('starting loop')

        yield react_for(
            duration=2,
            clock=reactor,
            deferred=read_messages(txcan_bus=txcan_bus),
        )


@twisted.internet.defer.inlineCallbacks
def read_messages(txcan_bus):
    while True:
        message = yield txcan_bus.receive_queue.get()

        logging.debug(
            'inline_callbacks_main %s %s',
            threading.get_ident() == threading.main_thread().ident,
            message,
        )
