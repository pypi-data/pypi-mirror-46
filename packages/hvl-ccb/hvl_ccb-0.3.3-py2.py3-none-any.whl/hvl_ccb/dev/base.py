"""
Module with base classes for devices.
"""

from abc import ABC, abstractmethod
from typing import Dict, Callable, Type

from ..comm import CommunicationProtocol
from ..configuration import ConfigurationMixin, configdataclass


class DeviceExistingException(Exception):
    """
    Exception to indicate that a device with that name already exists.
    """

    pass


@configdataclass
class EmptyConfig:
    """
    Empty configuration dataclass that is the default configuration for a Device.
    """
    pass


class Device(ConfigurationMixin, ABC):
    """
    Base class for devices. Implement this class for a concrete device,
    such as measurement equipment or voltage sources.

    Specifies the methods to implement for a device.
    """

    def __init__(self, dev_config=None):
        """
        Constructor for Device.
        """

        super().__init__(dev_config)

    @abstractmethod
    def start(self) -> None:
        """
        Start or restart this Device. To be implemented in the subclass.
        """

        pass  # pragma: no cover

    @abstractmethod
    def stop(self) -> None:
        """
        Stop this Device. To be implemented in the subclass.
        """

        pass  # pragma: no cover

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @staticmethod
    def config_cls():
        return EmptyConfig


class DeviceSequenceMixin(ABC):
    """
    Mixin that can be used on a device or other classes to provide facilities for
    handling multiple devices in a sequence.
    """

    def __init__(self, devices: Dict[str, Device]):
        """
        Constructor for the DeviceSequenceMixin.

        :param devices: is a dictionary of devices to be added to this sequence.
        """

        self._devices = devices  # type: Dict[str, Device]

    def apply_to_devices(self, func: Callable[[Device], object]) -> \
            Dict[str, object]:
        """
        Apply a function to all devices in this sequence.

        :param func: is a function that takes a device as an argument.
        :return: a sequence of objects returned by the called function.
        """

        returned_objects = {}

        for name in self._devices.keys():
            returned_objects[name] = func(self.get_device(name))

        return returned_objects

    def get_device(self, name: str) -> Device:
        """
        Get a device by name.

        :param name: is the name of the device.
        :return: the device object from this sequence.
        """

        return self._devices.get(name)

    def add_device(self, name: str, device: Device) -> None:
        """
        Add a new device to the device sequence.

        :param name: is the name of the device.
        :param device: is the instantiated Device object.
        :raise DeviceExistingException:
        """

        if name in self._devices.keys():
            raise DeviceExistingException

        self._devices[name] = device

    def remove_device(self, name: str) -> Device:
        """
        Remove a device from this sequence and return the object.

        :param name: is the name of the device.
        :return: device object.
        """

        return self._devices.pop(name, None)

    def start(self) -> None:
        """
        Start all devices in this sequence in their added order.
        """

        for name in self._devices.keys():
            self.get_device(name).start()

    def stop(self) -> None:
        """
        Stop all devices in this sequence in their reverse order.
        """

        for name in reversed(list(self._devices.keys())):
            self.get_device(name).stop()


class SingleCommDevice(Device, ABC):
    """
    Base class for devices with a single communication protocol.
    """

    # Omitting typing hint `com: CommunicationProtocol` on purpose
    # to enable PyCharm autocompletion for subtypes.
    def __init__(self, com, dev_config=None) -> None:
        """
        Constructor for Device. Links the communication protocol and provides a
        configuration for the device.

        :param com: Communication protocol to be used with
            this device. Can be of type: - CommunicationProtocol instance, - dictionary
            with keys and values to be used as configuration together with the
            default communication protocol, or - @configdataclass to be used together
            with the default communication protocol.

        :param dev_config: configuration of the device. Can be:
            - None: empty configuration is used, or the specified config_cls()
            - @configdataclass decorated class
            - Dictionary, which is then used to instantiate the specified config_cls()
        """

        super().__init__(dev_config)

        if isinstance(com, CommunicationProtocol):
            self._com = com
        else:
            self._com = self.default_com_cls()(com)

    @staticmethod
    @abstractmethod
    def default_com_cls() -> Type[CommunicationProtocol]:
        """
        Get the class for the default communication protocol used with this device.

        :return: the type of the standard communication protocol for this device
        """
        pass  # pragma: no cover

    @property
    def com(self):
        """
        Get the communication protocol of this device.

        :return: an instance of CommunicationProtocol subtype
        """
        return self._com

    def start(self) -> None:
        """
        Open the associated communication protocol.
        """

        self.com.open()

    def stop(self) -> None:
        """
        Close the associated communication protocol.
        """

        self.com.close()
