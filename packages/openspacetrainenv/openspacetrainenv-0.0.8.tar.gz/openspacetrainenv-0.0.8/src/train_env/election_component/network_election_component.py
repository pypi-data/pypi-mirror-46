import json
import uuid

from twisted.internet import reactor, defer

from src.election_component.election_component import ElectionComponent, STATES
from src.logger import Logger
from src.network_daemon import MulticastNetworkServer, MulticastNetworkClient


class NetworkElectionComponent(ElectionComponent):
    """Election component that uses multicast messages to discover other election components"""

    class MulticastElectionServer(MulticastNetworkServer, MulticastNetworkClient):
        """Multicast election server which takes care of sending messages as well as
        retrieving multicast messages.
        """

        message_type_callbacks = {
            "candidates": "_received_candidate_message",
            'election': '_retrieve_election_message'
        }

        def __init__(self, group, port, election_component):
            super().__init__(group, port)
            self.election_component = election_component
            self.replied_messages = set()

        def _received_candidate_message(self, message, address):
            """Receive and process a candidate message"""
            self.election_component._add_candidate(message["id"], address)

            if message["message_id"] not in self.replied_messages \
                    and self.election_component.get_state() != STATES.CLOSED:
                self.replied_messages.add(message["message_id"])
                response = {
                    "id": self.election_component.get_id(),
                    "message_id": message["message_id"],
                    "message_type": message["message_type"]
                }
                self.send_message(json.dumps(response))

        def _retrieve_election_message(self, message, _):
            """Receive and process an election message"""
            self.election_component.receive_message(message['message'], message['round'])

        def datagramReceived(self, datagram, address):
            """Overriden method from twisted. Reroutes the information to the correct method"""
            message = json.loads(datagram)
            getattr(self, self.message_type_callbacks[message["message_type"]])(message, address)

    def __init__(self, group, port, election_id=None, **kwargs):
        super().__init__(election_id if election_id is not None else str(uuid.uuid4()), **kwargs)
        self.group = group
        self.port = port
        self._server = self.MulticastElectionServer(self.group, self.port, self)
        reactor.listenMulticast(self.port, self._server, listenMultiple=True)
        self._discovery_time = 1

    def _discover(self):
        """Send a multicast message across the network (to the same multicast group)
        Do note that this method takes some time (one to multiple seconds) to come to
        a stable situation.
        """

        message = {"id": self.get_id(), "message_id": str(uuid.uuid4()), "message_type": "candidates"}
        self._server.replied_messages.add(message["message_id"])
        self._server.send_message(json.dumps(message))

    def _add_candidate(self, candidate, ip):
        """Add an election candidate"""
        self._others.add(ElectionComponent(candidate, ip=ip))

    def candidate_discovery(self):
        """Returns the list of retrieved candidates, using a set discovery time."""
        Logger().debug('Starting candidate discovery', location=self.__class__.__name__)
        deferred = defer.Deferred()
        self._discover()
        reactor.callLater(self._discovery_time, deferred.callback, None)
        return deferred

    def broadcast_message(self, message):
        self.send_message(None, message)

    def _start_election(self, _):
        """Do the local election. Check all others and pick the highest.
        Also broadcast this message so the others do the same.
        """
        self._leader = max(
            self._others,
            key=lambda x: x.get_id()
        )
        is_leader = self._leader.get_id() == self.get_id()
        self.election_rounds_participated.add(self.round)
        self._on_elected(is_leader)
        self.broadcast_message('update_leader')

    def start_election(self, candidate_discovery=True):
        """Handle callbacks for election. No real election logic is done here."""
        deferred = defer.Deferred()
        self.round += 1
        if candidate_discovery:
            candidate_defer = self.candidate_discovery()
            candidate_defer.addCallback(self._start_election)
            candidate_defer.addCallback(
                lambda x: Logger().debug('Finished candidate discovery', location=self.__class__.__name__))
        else:
            self._start_election(None)

        reactor.callLater(
            self._time_out + (0 if not candidate_discovery else self._discovery_time),
            deferred.callback,
            None
        )
        return deferred

    def receive_message(self, message, round_nr):
        """Receive a message from the network."""
        self._on_receive_message(message, round_nr)

    def send_message(self, other, message):
        """Send a message over the network to the given candidate"""
        message = {
            'message': message,
            'source': self.get_id(),
            'message_type': 'election',
            'round': self.round
        }
        self._server.send_message(json.dumps(message))
