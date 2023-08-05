# OpenSpace
## Train Environment

This is the repository of the train environment of the OpenSpace project. This project is written in Python 3.6 and will be running on the computers present on the train.

The project follows the [PEP008 style guide](https://www.python.org/dev/peps/pep-0008/), every collaborator should make sure his code is according to the standards.

Tests are very important in this project and should be written for each functional unit. The project uses the [unittest](https://docs.python.org/3.6/library/unittest.html#test-discovery) library for unit tests and [nose](https://nose.readthedocs.io/) for test discovery. 

Documentation is key to working in team, so make sure your code is well documented, also following the PEP008 style rules.

![alt text](https://i.imgur.com/opw2vug.png "Logo Title Text 2")

### Camera Handler

The camera handler uses a pubsub pattern to let subscribers know when frames are published. These frames will be transformed in the requested codec for each subscriber. These frames are sent to the broker to be redistributed amongst the components.

### Vision Container

The vision container will wrap the CV-ML service in the train environment. This will be done by importing their python script into our service and expose our broker as a singleton. This way, the vision container can publish messages and subscribe to messages through the broker. The init script should contain the setup logic for their container, as our service will not call any methods from within their service (except the registered callbacks).

### Broker

The broker (previously carriage communicator) is responsible for the internal routing of messages using a broker pattern.
Exposed methods:
* Broker.get_instance()
* self.subscribe('message', callback)
* self.publish('message', \*args, \*\*kwargs)

### Election Component
The election component is responsible for the election procedure amongst the different carriages as well as initiating the (physical) TUDA at an election win.

### Virtualized TUDA Module

Virtualized TUDA present on every carriage. This component has to transfer the connections to the TUDA by a HTTP connection.

### Train Unit Data Aggregator

The train unit data aggregator is the central point within the current sequence of carriages. This component has to buffer the received information and needs to communicate with the internal API and the transfer module.

#### Main TUDA Module

This module has to make sure the data is timestamped and routed to the other transfer modules (internal API & transfer module).

#### Internal API Module

This module has to buffer/store the data and respond to API calls that originate from the internal network on the train.

#### Transfer Module

This module is responsible for the connection to the wayside (backend). This module has to transfer the data to the AMQP module already present on the train (not part of our service).

### Test Simulations

To simulate the AMQP communication and the internal API, we need to create simple simulations of these components.
