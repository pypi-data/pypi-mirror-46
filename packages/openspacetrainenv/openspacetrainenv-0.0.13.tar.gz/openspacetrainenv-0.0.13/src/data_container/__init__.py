"""
This module exposes the different data containers that are used across the application and their (de)serialization logic
"""

from src.data_container.data_container import DataTypes, DataContainer, OccupancyData, ConfigUpdate, DataTypes, \
    CarriageData

__all__ = ['DataTypes', 'DataContainer', 'OccupancyData', 'ConfigUpdate', 'CarriageData']

DataTypes().add_datatype(ConfigUpdate)
DataTypes().add_datatype(OccupancyData)
DataTypes().add_datatype(CarriageData)
