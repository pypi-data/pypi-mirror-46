from src.train_unit_data_aggregator import TrainUnitDataAggregator


class VirtualTUDA(TrainUnitDataAggregator):

    def __init__(self, leader: TrainUnitDataAggregator):
        super().__init__()
        self.leader = leader

    def forward_occupancy_data(self, occupancy_data):
        """Override this to use different forwarding techniques"""
        self.leader.receive_occupancy_data(occupancy_data)

    def receive_occupancy_data(self, occupancy_data):
        self.forward_occupancy_data(occupancy_data)

    def receive_config_update(self, model_update):
        self._local_config_update(model_update)
