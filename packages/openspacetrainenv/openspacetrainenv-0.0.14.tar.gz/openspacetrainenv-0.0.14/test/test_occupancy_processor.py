import random
import unittest

from plugin.occupancy_processor import FreeSeatsProcessor, FillRateProcessor
from plugin.occupancy_processor.occupancy_processor import OccupancyProcessor
from src import EventListener, Broker, Event


class OccupancyProcessorTestListener(EventListener):
    def __init__(self):
        super().__init__()
        self.received = []
        self.set_message_type_callback('processed_occupancy', lambda x: self.received.append(x))


class OccupancyProcessorTests(unittest.TestCase):
    def test_occupancy_processor(self):
        test_occupancy_1 = {
            '1': True,
            '2': False,
            '3': True,
            '4': False,
            '5': True,
            '6': False,
            'input_id': 1
        }

        # Create and subscribe listeners
        broker = Broker()
        broker.clear_listeners()
        occupancy_processor = OccupancyProcessor('processed_occupancy', FreeSeatsProcessor())
        occupancy_processor.add_sub_processor(FillRateProcessor())
        test_listener = OccupancyProcessorTestListener()
        broker.subscribe(test_listener, 'processed_occupancy')

        # Publish occupancy
        broker.publish(Event('occupancy', test_occupancy_1))

        # Check result
        self.assertEqual(test_listener.received[0].processed_data['fill_rate'], 0.5)
        self.assertEqual(test_listener.received[0].processed_data['free_seats'], 3)
        self.assertEqual(test_listener.received[0].seat_map, test_occupancy_1)

    def test_occupancy_processor_multiple(self):
        test_occupancy_1 = {str(i): 0 for i in range(1, 7)}
        test_occupancy_2 = {str(i): 1 for i in range(1, 7)}
        test_occupancy_1["input_id"] = 1
        test_occupancy_2["input_id"] = 1

        broker = Broker()
        broker.clear_listeners()

        # create random seat occupancy
        random.seed(64)
        nr_of_seats = random.randint(5, 100)
        nr_occupied = random.randint(0, nr_of_seats)
        occupancy_list = [1 for _ in range(nr_occupied)]
        occupancy_list.extend([0 for _ in range(nr_of_seats - nr_occupied)])
        random.shuffle(occupancy_list)
        test_occupancy_3 = {str(i + 1): occupancy_list[i] for i in range(nr_of_seats)}
        test_occupancy_3["input_id"] = 1

        # Create listener and subscribe
        # occupancy_processor already created in previous tests
        occupancy_processor = OccupancyProcessor('processed_occupancy', FreeSeatsProcessor())
        occupancy_processor.add_sub_processor(FillRateProcessor())
        test_listener = OccupancyProcessorTestListener()
        broker.subscribe(test_listener, 'processed_occupancy')

        # Publish occupancies
        broker.publish(Event('occupancy', test_occupancy_1))
        broker.publish(Event('occupancy', test_occupancy_2))
        broker.publish(Event('occupancy', test_occupancy_3))

        # Check if each processed instance is correct
        for i, fill_rate, free_seats, test_occupancy in [(0, 0, 6, test_occupancy_1), (1, 1, 0, test_occupancy_2), (
                2, nr_occupied / nr_of_seats, nr_of_seats - nr_occupied, test_occupancy_3)]:
            self.assertEqual(test_listener.received[i].processed_data['fill_rate'], fill_rate)
            self.assertEqual(test_listener.received[i].processed_data['free_seats'], free_seats)
            self.assertEqual(test_listener.received[i].seat_map, test_occupancy)
