from collections import defaultdict
from enum import Enum

from src.logger import Logger


class STATES(Enum):
    """An enum of the different states an election component can be in."""

    IDLE = 0  # The component is idle and can accept messages (default state)
    SENT_ELECTION = 1  # The component sent an election message
    CLOSED = 2  # The component is closed and will not reply to messages
    LEADER = 3  # The component is the leader


class ElectionComponent:
    """A component that handles the election procedure on the train."""

    def __init__(self, id, ip=None):
        self._id = id
        self._others = set()
        self._state = STATES.IDLE
        self._answers = defaultdict(list)
        self._leader = None
        self._time_out = 2  # TODO: make this part of the configuration
        self.round = 0
        self.election_rounds_participated = set()
        self.ip = ip

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return hash(self.get_id())

    def candidate_discovery(self):
        """Discover other candidates for the election"""
        Logger().debug('Starting candidate discovery', location=self.__class__.__name__)
        candidates = [i for i in self._others if i.get_state() != STATES.CLOSED]
        Logger().debug('Finished candidate discovery', location=self.__class__.__name__)
        return candidates

    def receive_message(self, message, round_nr):
        self._on_receive_message(message, round_nr)

    def _on_receive_message(self, message, round_nr):
        """Do something when a message is received.
        When the update_leader message has been received and the component has not yet participated in the
        current round, it discovers the candidates in the network and restarts the election without broadcasting."""
        if message == 'update_leader' and round_nr not in self.election_rounds_participated and self.get_state() != STATES.CLOSED:
            self.election_rounds_participated.add(round_nr)
            self.round = round_nr
            self._start_election(True)

    def send_message(self, source, message):
        """Send a message to a given source"""
        source.receive_message(message, self.round)

    def broadcast_message(self, message):
        """Broadcast a message to all other candidates"""
        for candidate in self._others:
            self.send_message(candidate, message)

    def _start_election(self, candidate_discovery):
        self._leader = max(
            self.candidate_discovery() + [self] if candidate_discovery else self._others.union(set(self)),
            key=lambda x: x.get_id()
        )
        is_leader = self._leader.get_id() == self.get_id()
        self.election_rounds_participated.add(self.round)
        self._on_elected(is_leader)
        self.broadcast_message('update_leader')

    def start_election(self, candidate_discovery=True):
        """Start the election procedure by sending an election message to all higher ID'ed candidates"""
        self.round += 1
        self._start_election(candidate_discovery=candidate_discovery)

    def _on_elected(self, is_leader):
        """Logic to be ran when a leader has been elected"""
        if is_leader:
            self._state = STATES.LEADER
        self.on_elected(is_leader)

    def on_elected(self, is_leader):
        """Callback that will be called when a leader has been elected"""
        raise NotImplementedError

    def get_leader(self):
        return self._leader

    def is_leader(self):
        return self.get_state() == STATES.LEADER

    def get_state(self):
        return self._state

    def get_id(self):
        return self._id

    def destroy(self):
        """Destroy this election component. This will set its state to closed."""
        self._state = STATES.CLOSED
