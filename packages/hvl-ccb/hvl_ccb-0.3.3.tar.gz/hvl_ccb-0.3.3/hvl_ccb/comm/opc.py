"""
Communication protocol implementing an OPC UA connection.
This protocol is used to interface with the "Supercube" PLC from Siemens.
"""

import logging
from typing import Iterable, Union

from opcua import Client, Node, Subscription
from opcua.ua import NodeId, DataValue

from .base import CommunicationProtocol
from ..configuration import configdataclass


class OpcUaSubHandler:
    """
    Base class for subscription handling of OPC events and data change events.
    Override methods from this class to add own handling capabilities.

    To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing.
    """

    def datachange_notification(self, node, val, data):
        logging.getLogger(__name__).debug(
            'OPCUA Datachange event: {} to value {}'.format(node, val)
        )

    def event_notification(self, event):
        logging.getLogger(__name__).debug('OPCUA Event: {}'.format(event))


@configdataclass
class OpcUaCommunicationConfig:
    """
    Configuration dataclass for OPC UA Communciation.
    """

    #: Hostname or IP-Address of the OPC UA server.
    host: str

    #: Endpoint of the OPC server, this is a path like 'OPCUA/SimulationServer'
    endpoint_name: str

    #: Port of the OPC UA server to connect to.
    port: int = 4840

    #: object to use for handling subscriptions.
    sub_handler: OpcUaSubHandler = OpcUaSubHandler()

    #: Update period for generating datachange events in OPC UA [milli seconds]
    update_period: int = 500


class OpcUaCommunication(CommunicationProtocol):
    """
    Communication protocol implementing an OPC UA connection.
    Makes use of the package python-opcua.
    """

    def __init__(self, config) -> None:
        """
        Constructor for OpcUaCommunication.

        :param config: is the configuration dictionary.
        """

        super().__init__(config)

        self.logger = logging.getLogger(__name__)

        url = (
            'opc.tcp://{host}:{port}/{endpoint}'.format(
                host=self.config.host,
                port=self.config.port,
                endpoint=self.config.endpoint_name,
            )
        )

        self.logger.info('Create OPC UA client to URL: {}'.format(url))

        self._client = Client(url)

        # the objects node exists on evere OPC UA server and is the root for all
        # objects.
        self._objects_node = None  # type: Node

        # subscription handler
        self._sub_handler = self.config.sub_handler

        # subscription object
        self._subscription = None  # type: Subscription

    @staticmethod
    def config_cls():
        return OpcUaCommunicationConfig

    def open(self) -> None:
        """
        Open the communication to the OPC UA server.
        """

        self.logger.info('Open connection to OPC server.')
        with self.access_lock:
            self._client.connect()
            # in example from opcua, load_type_definitions() is called after connect(
            # ). However, this raises ValueError when connecting to Siemens S7,
            # and no problems are detected omitting this call.
            # self._client.load_type_definitions()
            self._objects_node = self._client.get_objects_node()
            self._subscription = self._client.create_subscription(
                self.config.update_period, self._sub_handler)

    def close(self) -> None:
        """
        Close the connection to the OPC UA server.
        """

        self.logger.info('Close connection to OPC server.')
        with self.access_lock:
            self._subscription.delete()
            self._client.disconnect()

    def read(self, node_id, ns_index):
        """
        Read a value from a node with id and namespace index.

        :param node_id: the ID of the node to read the value from
        :param ns_index: the namespace index of the node
        :return: the value of the node object.
        """

        with self.access_lock:
            return self._client.get_node(
                NodeId(identifier=node_id, namespaceidx=ns_index)).get_value()

    def write(self, node_id, ns_index, value) -> None:
        """
        Write a value to a node with name ``name``.

        :param node_id: the id of the node to write the value to.
        :param ns_index: the namespace index of the node.
        :param value: the value to write.
        """

        with self.access_lock:
            self._client.get_node(
                NodeId(identifier=node_id, namespaceidx=ns_index)
            ).set_value(DataValue(value))

    def init_monitored_nodes(self, node_id: Union[str, Iterable[str]],
                             ns_index: int) -> None:
        """
        Initialize monitored nodes.

        :param node_id: one or more strings of node IDs.
        :param ns_index: the namespace index the nodes belong to.
        """

        if isinstance(node_id, str):
            ids = [node_id]
        else:
            ids = node_id

        nodes = []
        for id_ in ids:
            nodes.append(self._client.get_node(
                NodeId(identifier=id_, namespaceidx=ns_index)
            ))

        with self.access_lock:
            self._subscription.subscribe_data_change(nodes)
