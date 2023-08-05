"""This module exposes the different implementations of the election component which orchestrates
the election on the train to select a leader."""

from src.election_component.election_component import ElectionComponent
from src.election_component.network_election_component import NetworkElectionComponent

__all__ = ['ElectionComponent', 'NetworkElectionComponent']
