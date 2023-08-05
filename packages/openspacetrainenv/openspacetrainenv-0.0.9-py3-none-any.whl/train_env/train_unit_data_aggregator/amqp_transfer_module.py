import json
import requests

from pika.adapters import twisted_connection
from twisted.internet import defer, protocol, reactor, task

from src.logger import Logger
from src.train_unit_data_aggregator.transfer_module import TransferModule

class AMQPTransferModule(TransferModule):
    """Transfer module which uses the AMQP transfer protocol."""

    def __init__(self, amqp_port=5672, **kwargs):
        super().__init__(**kwargs)
        self.port = amqp_port

    def attach_tuda(self, tuda):
        super().attach_tuda(tuda)
        self._listen_updates()

    def transfer_to_backend(self, data, queue):
        """Overridden method which transfers the data to the AMQP server."""
        print(data)
        cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, self.parameters)
        d = cc.connectTCP(self.host, self.port)
        d.addCallback(lambda p: p.ready)
        d.addCallback(self._publish, data, queue)
        d.addErrback(self._on_connection_error)
        Logger().debug("AMQP connection was set-up", location=self.__class__.__name__)

    def _on_connection_error(self, error):
        """Error callback which logs all twisted errors."""
        Logger().error(f'An error occurred setting up the AMQP connection: "{repr(error)}"',
                       location=self.__class__.__name__)

    @defer.inlineCallbacks
    def _publish(self, connection, data, queue):
        """Callback when AMQP connection is fully set-up."""
        channel = yield connection.channel()
        yield channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(data))
        Logger().debug("Sent AMQP message to queue", location=self.__class__.__name__)
        self._reset_module(channel, connection)

    def _reset_module(self, channel, connection):
        """Resets the queue & the data."""
        channel.close()
        connection.close()
        Logger().debug("AMQP connection closed and module reset", location=self.__class__.__name__)

    @defer.inlineCallbacks
    def _run(self, connection):
        channel = yield connection.channel()
        #exchange = yield channel.exchange_declare(exchange='updates')
        for carriage_id in self.tuda.get_carriages():
            queue_name = 'updates_' + str(carriage_id)
            yield channel.queue_declare(queue=queue_name, auto_delete=False, exclusive=False)
            queue_object, consumer_tag = yield channel.basic_consume(queue=queue_name)
            l = task.LoopingCall(self._read, queue_object)
            Logger().info("Start consuming " + queue_name, location=self.__class__.__name__)
            l.start(0.01)

    @defer.inlineCallbacks
    def _read(self, queue_object):
        ch, method, properties, body = yield queue_object.get()
        if body:

            Logger().info("received update", location=self.__class__.__name__)
            self.receive_config_link(json.loads(body))
        yield ch.basic_ack(delivery_tag=method.delivery_tag)

    def _listen_updates(self):
        cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, self.parameters)
        d = cc.connectTCP(self.host, self.port)
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self._run)
