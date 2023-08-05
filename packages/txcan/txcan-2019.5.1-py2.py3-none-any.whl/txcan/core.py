import contextlib
import logging
import queue
import threading

import attr
import can
import twisted.internet.defer
import twisted.internet.interfaces

logger = logging.getLogger(__name__)


@attr.s
class Listener(can.Listener):
    callable = attr.ib()

    def __attrs_post_init__(self):
        super(Listener, self).__init__()

    def on_message_received(self, msg):
        self.callable(message=msg)


@attr.s
class Bus:
    bus = attr.ib(default=None)
    notifier = attr.ib(default=None)
    listener = attr.ib(default=None)
    reactor = attr.ib(default=None)
    receive_queue = attr.ib(factory=twisted.internet.defer.DeferredQueue)
    send_queue = attr.ib(factory=queue.Queue)
    send_thread = attr.ib(default=None)

    @classmethod
    def build(cls, bus, reactor):
        self = cls(bus=bus, reactor=reactor)
        self.listener = Listener(callable=self.receive_in_thread)
        self.notifier = can.Notifier(bus=bus, listeners=[self.listener])
        self.send_thread = threading.Thread(target=self.loop_in_send_thread)

        return self

    @contextlib.contextmanager
    def linked(self):
        self.connect()

        try:
            yield self
        finally:
            self.loseConnection()

    def connect(self):
        self.notifier.add_listener(self.listener)
        self.send_thread.start()

    def loseConnection(self):
        self.notifier.remove_listener(self.listener)
        self.send_queue.put(None)
        logger.debug('waiting for send thread to join')
        self.send_thread.join()
        logger.debug('send thread joined')

    def receive_in_reactor(self, message):
        logging.debug(
            'receive_in_reactor %s %s',
            threading.get_ident() == threading.main_thread().ident,
            message,
        )
        self.receive_queue.put(message)

    def receive_in_thread(self, message):
        self.reactor.callFromThread(self.receive_in_reactor, message)

    def loop_in_send_thread(self):
        logger.debug('started send thread')
        while True:
            message = self.send_queue.get()

            if message is None:
                logger.debug('send thread received terminate command')
                return
            
            self.bus.send(message)

        logger.debug('ending send thread')
