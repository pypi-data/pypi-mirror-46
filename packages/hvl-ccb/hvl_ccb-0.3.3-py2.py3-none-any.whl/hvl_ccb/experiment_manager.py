# -*- coding: utf-8 -*-

"""
Main module containing the top level ExperimentManager class.
Inherit from this class to implement your own experiment functionality in another
project and it will help you start, stop and manage your devices.
"""

import logging
from typing import Dict
from enum import Enum

from .dev import Device, DeviceSequenceMixin


class ExperimentStatus(Enum):
    """
    Enumeration for the experiment status
    """
    INITIALIZED = 0
    STARTING = 1
    RUNNING = 2
    FINISHING = 3
    FINISHED = 4
    ERROR = 5


class ExperimentError(Exception):
    """
    Exception to indicate that the current status of the experiment manager is on
    ERROR and thus no operations can be made until reset.
    """

    pass


class ExperimentManager(DeviceSequenceMixin):
    """
    Experiment Manager can start and stop communication protocols and devices.
    It provides methods to queue commands to
    devices and collect results.
    """

    def __init__(self, devices: Dict[str, Device]) -> None:
        """
        Constructor for ExperimentManager. Takes a dictionary of instantiated devices
        and initializes the experiment status to STOPPED.
        """

        super().__init__(devices)

        # experiment manager status
        self._status = ExperimentStatus.INITIALIZED

    def _change_status(self, new_status: ExperimentStatus) -> None:
        """
        Change the status of this experiment manager to a new value. Includes logging.

        :param new_status: is the Enum of the new experiment status.
        """

        if new_status is not self._status:
            # new status is different, log
            if new_status is ExperimentStatus.ERROR:
                logging.error('Experiment Status: {0} {1}'.format(new_status,
                                                                  new_status.name))
            else:
                logging.info('Experiment Status: {0} {1}'.format(new_status,
                                                                 new_status.name))
            self._status = new_status

    def run(self) -> None:
        """
        Start experimental setup, start all devices.
        """

        self._change_status(ExperimentStatus.STARTING)

        try:
            super().start()
        except Exception as e:
            logging.error(e)
            self._change_status(ExperimentStatus.ERROR)
            raise ExperimentError from e
        else:
            self._change_status(ExperimentStatus.RUNNING)

    def finish(self) -> None:
        """
        Stop experimental setup, stop all devices.
        """

        self._change_status(ExperimentStatus.FINISHING)

        try:
            super().stop()
        except Exception as e:
            logging.error(e)
            self._change_status(ExperimentStatus.ERROR)
            raise ExperimentError from e
        else:
            self._change_status(ExperimentStatus.FINISHED)

    def start(self) -> None:
        """
        Alias for ExperimentManager.run()
        """
        self.run()

    def stop(self) -> None:
        """
        Alias for ExperimentManager.finish()
        """
        self.finish()

    @property
    def status(self) -> ExperimentStatus:
        """
        Get experiment status.

        :return: experiment status enum code.
        """

        return self._status

    def is_finished(self) -> bool:
        """
        Returns true, if the status of the experiment manager is `finished`.

        :return: True if finished, false otherwise
        """
        return self.status == ExperimentStatus.FINISHED

    def is_running(self) -> bool:
        """
        Returns true, if the status of the experiment manager is `running`.

        :return: True if running, false otherwise
        """
        return self.status == ExperimentStatus.RUNNING

    def is_error(self) -> bool:
        """
        Returns true, if the status of the experiment manager is `error`.

        :return: True if on error, false otherwise
        """
        return self.status == ExperimentStatus.ERROR

    def add_device(self, name: str, device: Device) -> None:
        """
        Add a new device to the manager. If the experiment is running, automatically
        start the device. If a device with this name already exists, raise an exception.

        :param name: is the name of the device.
        :param device: is the instantiated Device object.
        :raise DeviceExistingException:
        """

        if self.status == ExperimentStatus.ERROR:
            logging.error('Experiment is on ERROR, cannot add device')
            raise ExperimentError

        super().add_device(name, device)

        # check experiment status and start device if started
        if self.status == ExperimentStatus.RUNNING:
            logging.info(
                'Experiment is already RUNNING, start Device {}'.format(Device)
            )
            try:
                device.start()
            except Exception as e:
                logging.error(e)
                self._change_status(ExperimentStatus.ERROR)
                raise ExperimentError from e
