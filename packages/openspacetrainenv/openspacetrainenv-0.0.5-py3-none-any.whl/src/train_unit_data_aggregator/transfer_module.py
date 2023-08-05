import json

import pika
import requests

from src.data_container import ConfigUpdate


class TransferModule:
    """This component handles the data flow from the train unit to the remote backend and vice versa."""

    def __init__(self, amqp_host="localhost", username="", password=""):
        self.tuda = None
        self.host = amqp_host
        self.parameters = pika.ConnectionParameters(amqp_host, 5672, "/", pika.PlainCredentials(username, password))
        self.data = None
        self.queue = None

    def attach_tuda(self, tuda):
        """
        Attach the train unit data aggregator to the transfer module so that the transfer module
        can interact with it.
        """

        self.tuda = tuda

    def transfer_to_train(self, data):
        """Transfer the model update to the train unit data aggregator"""
        if self.tuda:
            self.tuda.receive_config_update(ConfigUpdate(data['carriage_id'], data['config_type'], data['data']))
        else:
            raise ValueError("Train unit data aggregator is unknown!")

    def transfer_to_backend(self, data, queue):
        """
        Transfer the given data (seat occupancy data, ...) to the backend.
        First a connection to the AMQP server is setup, next the necessary queue is declared to the channel and
        the data is published.
        """
        # TODO: remove this dirty hack
        pass

    def receive_config_link(self, body):
        r = requests.get(body['download_link'])
        body.pop('download_link')
        body['data'] = json.loads(r.text)
        self.transfer_to_train(body)
