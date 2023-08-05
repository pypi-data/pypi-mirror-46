import unittest
import uuid

from twisted.internet import reactor

from src.election_component import ElectionComponent, NetworkElectionComponent
from src.election_component.election_component import STATES
from src.election_component.tuda_election_component import TudaElectionComponent
from src.network_daemon import MockingNetworkServer, MockingNetworkClient
from src.train_unit_data_aggregator.network_train_unit_data_aggregator import NetworkTrainUnitDataAggregator
from src.virtual_tuda import VirtualNetworkTUDA


class _TestElectionComponent(ElectionComponent):
    def __init__(self, id):
        super().__init__(id)

    def on_elected(self, is_leader):
        pass

    def __str__(self):
        return '{} - [{}]'.format(self._id, self._others)


class TestElectionComponent(unittest.TestCase):
    def _update_others(self, election_components):
        for i, election_component in enumerate(election_components):
            election_component._others = election_components[:i] + election_components[i + 1:]

    def test_election(self):
        # Create election components
        election_components = [_TestElectionComponent(i) for i in range(5)]

        # Fill in the other election components as others (instead of candidate discovery)
        self._update_others(election_components)

        # Let the third note start the election
        election_components[2].start_election()

        # The election component with the highest id should win (== 5)
        self.assertTrue(election_components[4].is_leader())

        # Close the highest election component
        election_components[4].destroy()

        # Start the election from the second highest component
        election_components[3].start_election()

        # Check if this component won
        self.assertTrue(election_components[3].is_leader())

        # Add a new highest component
        election_components.append(_TestElectionComponent(1000))
        self._update_others(election_components)

        # Let a random component start the election
        election_components[3].start_election()

        # The newly created component should win the election
        self.assertTrue(election_components[5].is_leader())


class _TestNetworkElectionComponent(NetworkElectionComponent):
    def on_elected(self, is_leader):
        pass

    def __str__(self):
        return '{} - [{}]'.format(self._id, self._others)


class TestNetworkElectionComponent(unittest.TestCase):

    def _discover(self, searching_election_component, election_components):
        """Candidate discover function"""
        self.component_list = [searching_election_component] + election_components

        # Discover the other components using the multicast request
        deferred = searching_election_component.candidate_discovery()

        # When candidates have been found, test the election procedure
        deferred.addCallback(self._test_election)

    def _stop_reactor(self, _):
        """Stop reactor callback"""
        reactor.stop()

    def _election(self, largest_id_component: ElectionComponent, other_components):
        """Do the election test"""

        # Close the normal leader
        largest_id_component.destroy()

        # Do the election
        defer = other_components[-1].start_election(candidate_discovery=False)

        # Stop the reactor after the election
        defer.addCallback(self._stop_reactor)

    def _test_election(self, _):
        # Sort the components and pass the component to the election
        sorted_components = list(
            sorted(self.component_list, key=lambda x: x.get_id()))[::-1]

        # Do the election
        self._election(sorted_components[0], sorted_components[1:])

    def test_candidate_discovery(self, amount_of_components=10):
        self.skipTest('This is not a unittest and should not be run in the unittest configuration. '
                      'As this tests requires access to the local network, this test does not work on Jenkins'
                      ' and can be seen as an \'integration\' test.')

        # Create other election components
        election_components = [_TestNetworkElectionComponent("224.0.0.1", 8005) for _ in range(amount_of_components)]

        # Create the component that starts the discovery
        searching_election_component = _TestNetworkElectionComponent("224.0.0.1", 8005)

        # Let the test run for a second
        reactor.callFromThread(self._discover, searching_election_component, election_components)

        # Let the Twisted reactor run
        reactor.run()

        # Assert if all the ids have been received
        self.assertSetEqual({i.get_id() for i in election_components + [searching_election_component]},
                            {i.get_id() for i in searching_election_component._others})

        # Sort the components
        sorted_components = list(
            sorted([searching_election_component] + election_components, key=lambda x: x.get_id()))[::-1]

        # Check if the second best one is the leader
        self.assertTrue(sorted_components[0].is_leader())


class _MockedNetworkElectionComponent(NetworkElectionComponent):
    """Mocking class for the network election component. All the transportation methods have been mocked."""

    class MockedElectionServer(MockingNetworkServer, MockingNetworkClient,
                               NetworkElectionComponent.MulticastElectionServer):
        message_type_callbacks = {
            "candidates": "_received_candidate_message",
            'election': '_retrieve_election_message'
        }

        def __init__(self, election_component):
            super(MockingNetworkServer, self).__init__()
            self.election_component = election_component
            self.replied_messages = set()

        def send_message(self, message):
            super().send_message(message)
            for other in self.election_component._others:
                other._server.datagramReceived(self.transport.value().decode('utf-8'), None)
            self.transport.clear()

    def __init__(self, x=None):
        if x is None:
            self.uuid = str(uuid.uuid4())
        else:
            self.uuid = x
        ElectionComponent.__init__(self, self.uuid)
        self._server = self.MockedElectionServer(self)
        self._discovery_time = 1
        self.i = 0

    def on_elected(self, is_leader):
        pass

    def start_election(self, candidate_discovery=False):
        self.round += 1
        _MockedNetworkElectionComponent._start_election(self, None)

    def _start_election(self, _):
        self.i += 1
        super(_MockedNetworkElectionComponent, self)._start_election(_)


class TestMockedNetworkElectionComponent(unittest.TestCase):

    def _update_others(self, election_components):
        for i, election_component in enumerate(election_components):
            election_component._others = set(election_components)

    def test_election(self):
        """Test the mocked network election component"""

        # Create election components
        election_components = list(
            reversed(
                sorted(
                    [
                        _MockedNetworkElectionComponent() for _ in range(10)
                    ], key=lambda x: x.get_id()
                )
            )
        )

        # Fill in the other election components as others (instead of candidate discovery)
        self._update_others(election_components)

        # Let the third note start the election
        election_components[2].start_election()

        # The election component with the highest id should win (== 5)
        self.assertTrue(election_components[0].is_leader())

        # Check if it really only took one round
        for election_component in election_components:
            self.assertEqual(election_component.i, 1)

        # Close the highest election component
        election_components[0].destroy()

        # Do manual candidate discovery
        self._update_others([election_component for election_component in election_components if
                             election_component.get_state() != STATES.CLOSED])

        # Start the election from the second highest component
        election_components[3].start_election()

        # Check if this component won
        self.assertTrue(election_components[1].is_leader())

        # Check if it really only took two rounds (including the previous)
        for election_component in election_components[1:]:
            self.assertEqual(election_component.i, 2)

        # Add a new highest component
        new_leader = _MockedNetworkElectionComponent('ffffffff-62cc-4738-8227-d6f87b4be188')
        election_components.append(new_leader)

        election_components = list(
            reversed(
                sorted(
                    election_components, key=lambda x: x.get_id()
                )
            )
        )

        self._update_others(election_components)

        # Let a random component start the election
        election_components[3].start_election()

        # The newly created component should win the election
        self.assertTrue(election_components[0].is_leader())

        for election_component in election_components:
            election_component._server.transport.loseConnection()


class TestTUDAElectionComponent(unittest.TestCase):
    def test_on_elected(self):
        from src import ConfigurationStore

        cstore = ConfigurationStore()
        cstore.set_value("tuda_port", 9090)
        cstore.set_value("tuda_mport", 9091)

        leader_tuda_el_comp = TudaElectionComponent(with_timer=False)
        leader_tuda_el_comp.on_elected(True)
        self.assertTrue(isinstance(leader_tuda_el_comp.get_tuda_object(), NetworkTrainUnitDataAggregator))
        leader_tuda_el_comp.get_tuda_object().destroy()

        cstore.set_value("tuda_port", 9092)
        cstore.set_value("tuda_mport", 9093)

        non_leader_tuda_el_comp = TudaElectionComponent(with_timer=False)
        non_leader_tuda_el_comp._leader = leader_tuda_el_comp
        non_leader_tuda_el_comp.on_elected(False)
        self.assertTrue(isinstance(non_leader_tuda_el_comp.get_tuda_object(), VirtualNetworkTUDA))
        non_leader_tuda_el_comp.get_tuda_object().destroy()
