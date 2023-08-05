import datetime as dt
import json

from src.singleton import Singleton


class DataTypes(metaclass=Singleton):

    def __init__(self):
        self.types = {}
        self.reverse_types = {}
        self.curr_id = 0

    def add_datatype(self, datatype):
        if datatype not in self.reverse_types:
            self.types[self.curr_id] = datatype
            self.reverse_types[datatype] = self.curr_id
            self.curr_id += 1

    def remove_datatype(self, datatype):
        d_id = self.reverse_types[datatype]
        self.reverse_types.pop(datatype)
        self.types.pop(d_id)
        self.curr_id += 1

    def get_value(self, datatype):
        return self.reverse_types[datatype]

    def get_type(self, d_id):
        return self.types[d_id]


class DataContainer:
    """
    A general class to contain the general information of each type of data transferred through the train
    environment network such as the occupancy data extracted from the footage, the footage itself and model updates.
    """

    def __init__(self, carriage_id, timestamp=None):
        self.carriage_id = carriage_id
        self.data_type = DataTypes().get_value(self.__class__)
        self.timestamp = dt.datetime.now().astimezone().isoformat() if timestamp is None else timestamp

    def marshal(self):
        """
        Transform this python object into a JSON string such that it can be sent over the network.
        """

        return json.dumps(self.__dict__, default=self.serialize)

    def serialize(self, field):
        """
        Transform a specific field of this class object to string if json is unable to do it automatically.
        """

        return

    @staticmethod
    def unmarshal(json_data):
        """
        Transform the JSON string to a python object.
        """

        data = json.loads(json_data)
        return DataTypes().get_type(data['data_type']).to_object(data)

    @staticmethod
    def to_object(data):
        """
        Instantiate a new python object containing the given data.
        """

        return

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class OccupancyData(DataContainer):
    """
    Objects of this class represent the occupancy data from a SINGLE train carriage.
    """

    def __init__(self, carriage_id, seat_map, processed_data=None, timestamp=None):
        super().__init__(carriage_id, timestamp)
        self.seat_map = seat_map
        self.processed_data = processed_data if processed_data is not None else {}

    @staticmethod
    def to_object(data):
        return OccupancyData(
            data['carriage_id'],
            data['seat_map'],
            data['processed_data'],
            data['timestamp']
        )

    def to_API_object(self):
        obj = {"carriage": self.carriage_id, "timestamp": self.timestamp, "seatMap": self.seat_map}
        for processed_type, processed_data in self.processed_data.items():
            obj[to_camel_case(processed_type)] = processed_data
        return obj


class ConfigUpdate(DataContainer):
    """
    Objects of this class represent the updates that need to be performed on the model running in each carriage
    of the train unit. The backend emits these model updates.
    """

    def __init__(self, carriage_id, config_type, data, timestamp=None):
        super().__init__(carriage_id, timestamp)
        self.config_type = config_type
        self.data = data

    @staticmethod
    def to_object(data):
        return ConfigUpdate(data['carriage_id'], data['config_type'], data['data'])

    def to_API_object(self):
        obj = {"carriage_id": self.carriage_id, "config_type": self.config_type, "data": self.data}
        return obj


class CarriageData(DataContainer):
    """
    Objects of this class contain the data (size, type, ...) of a carriage of the train unit.
    """

    def __init__(self, carriage_id, carriage_size, carriage_type, timestamp=None):
        super().__init__(carriage_id, timestamp)
        self.size = carriage_size
        self.type = carriage_type

    @staticmethod
    def to_object(data):
        return CarriageData(data['carriage_id'], data['size'], data['type'], data['timestamp'])


def to_camel_case(snake_case):
    """
    Convert the snake_case format to camelCase format.
    """

    first, *rest = snake_case.split('_')
    return first + ''.join(word.capitalize() for word in rest)
