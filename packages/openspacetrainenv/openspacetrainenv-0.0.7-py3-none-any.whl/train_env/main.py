from twisted.internet import reactor

from src.election_component.tuda_election_component import TudaElectionComponent
from src.logger import Logger


def setup_election_component():
    election_component = TudaElectionComponent()
    election_component.start_election()


def start_network_listeners(environment_function=None):
    """Start the reactor and let the remaining functions run on another thread"""

    Logger().info('Setup done, starting network listeners', location='SETUP')
    if environment_function is not None:
        reactor.callFromThread(environment_function)
    reactor.run()


def main():
    Logger().info('Setting up train environment', location='SETUP')

    start_network_listeners(setup_election_component())


if __name__ == '__main__':
    main()
