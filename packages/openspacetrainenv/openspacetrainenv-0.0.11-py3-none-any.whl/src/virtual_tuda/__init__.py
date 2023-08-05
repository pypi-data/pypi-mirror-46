"""This module contains the virtual train unit data aggregator which forwards its requests to the real
train unit data aggregator, as well as accepts messages from its leader TUDA.
"""

from src.virtual_tuda.virtual_network_tuda import VirtualNetworkTUDA
from src.virtual_tuda.virtual_tuda import VirtualTUDA

__all__ = ["VirtualTUDA", "VirtualNetworkTUDA"]
