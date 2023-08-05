from src import Broker


class InternalAPI:
    """
    This component handles all network requests made by clients (staff, travellers, ...) aboard the train.
    This component receives the most recent seat occupancy data from the train unit data aggregator and stores this
    data such that incoming received network requests can be fulfilled using only this locally stored data.
    """

    def __init__(self):
        self.occupancy_data_map = {}

    def receive_occupancy_data(self, occupancy_data):
        """
        Receive and store the updated seat occupancy data from the train unit data aggregator.
        """

        id = occupancy_data.carriage_id
        self.occupancy_data_map[id] = occupancy_data.to_API_object()

    def destroy(self):
        """Handles all destroy logic which should for example close reactor listeners."""
        Broker().unsubscribe(self)
