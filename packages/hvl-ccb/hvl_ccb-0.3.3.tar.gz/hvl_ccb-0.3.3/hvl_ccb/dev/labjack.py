"""
Labjack Device for hvl_ccb.
Originally developed and tested for LabJack T7-PRO.

Makes use of the LabJack LJM Library Python wrapper.
This wrapper needs an installation of the LJM Library for Windows, Mac OS X or Linux.
Go to:
https://labjack.com/support/software/installers/ljm
and
https://labjack.com/support/software/examples/ljm/python
"""

import logging
from typing import Union

from .base import SingleCommDevice
from ..comm import LJMCommunication
from ..utils.enum import NameEnum


class LabJackError(Exception):
    """
    Errors of the LabJack device.
    """
    pass


class LabJack(SingleCommDevice):
    """
    LabJack Device.
    This class is tested with a LabJack T7-Pro and should work with T4, T7 and DIGIT
    communicating through the LJM Library. Other or older hardware versions and
    variants of LabJack devices are not supported.
    """

    def __init__(self, com, dev_config=None) -> None:
        """
        Constructor for a LabJack Device.

        :param com: Communication protocol object of type
            LJMCommunication. If a configuration (dict or configdataclass) is given,
            a new communication protocol object will be instantiated.
        :param dev_config: There is no device configuration for LabJack yet.
        """
        super().__init__(com, dev_config)

    @staticmethod
    def default_com_cls():
        return LJMCommunication

    def start(self) -> None:
        """
        Start the Device.
        """

        logging.info('Starting Device')

        self.com.open()

    def stop(self) -> None:
        """
        Stop the Device.
        """

        logging.info('Stopping Device')

        self.com.close()

    def get_serial_number(self) -> int:
        """
        Returns the serial number of the connected LabJack.

        :return: Serial number.
        """

        return int(self.com.read_name("SERIAL_NUMBER"))

    def get_sbus_temp(self, number: int) -> float:
        """
        Read the temperature value from a serial SBUS sensor.

        :param number: port number (0..22)
        :return: temperature in Kelvin
        """

        return float(
            self.com.read_name("SBUS{}_TEMP".format(number))
        )

    def get_sbus_rh(self, number: int) -> float:
        """
        Read the relative humidity value from a serial SBUS sensor.

        :param number: port number (0..22)
        :return: relative humidity in %RH
        """

        return float(self.com.read_name("SBUS{}_RH".format(number)))

    def get_ain(self, channel: int) -> float:
        """
        Read the voltage of an analog input.

        :param channel: is the AIN number (0..254)
        :return: the read voltage
        """

        return float(self.com.read_name("AIN{}".format(channel)))

    def set_ain_range(self, channel: int, ain_range: float) -> None:
        r"""
        Set the range of an analog input port.

        Possible values for ``ain_range`` are:

        *  10   => +- 10   V
        *  1    => +- 1    V
        *  0.1  => +- 0.1  V
        *  0.01 => +- 0.01 V

        :param channel: is the AIN number (0..254)
        :param ain_range: is the range specifier
        """

        if ain_range not in (10, 1, 0.1, 0.01):
            raise LabJackError('Not supported range: {}'.format(ain_range))

        self.com.write_name(
            "AIN{}_RANGE".format(channel), ain_range
        )

    def set_ain_resolution(self, channel: int, resolution: int) -> None:
        """
        Set the resolution index of an analog input port.

        For a T7 Pro values between 0-12 are allowed.
        0 will set the resolution index to default value.

        :param channel: is the AIN number (0..254)
        :param resolution: is the resolution index
        """

        if resolution not in range(13):
            raise LabJackError('Not supported resolution index: {}'.format(resolution))

        self.com.write_name(
            'AIN{}_RESOLUTION_INDEX'.format(channel), resolution
        )

    def set_ain_differential(self, pos_channel: int, differential: bool) -> None:
        """
        Sets an analog input to differential mode or not.
        T7-specific: For base differential channels, positive must be even channel
        from 0-12 and negative must be positive+1. For extended channels 16-127,
        see Mux80 datasheet.

        :param pos_channel: is the AIN number (0..12)
        :param differential: True or False
        :raises LabJackError: if parameters are unsupported
        """

        if pos_channel not in range(13):
            raise LabJackError('Not supported pos_channel: {}'.format(pos_channel))

        if pos_channel % 2 != 0:
            raise LabJackError('AIN pos_channel for positive part of differential pair '
                               'must be even: {}'.format(pos_channel))

        neg_channel = pos_channel + 1

        self.com.write_name(
            "AIN{}_NEGATIVE_CH".format(pos_channel),
            neg_channel if differential else 199
        )

    class ThermocoupleType(NameEnum):
        """
        Thermocouple type; NONE means disable thermocouple mode.
        """
        _init_ = 'ef_index'
        NONE = 0
        E = 20
        J = 21
        K = 22
        R = 23
        T = 24
        S = 25
        C = 30
        PT100 = 40
        PT500 = 41
        PT1000 = 42

    class CjcType(NameEnum):
        """
        CJC slope and offset
        """
        _init_ = 'slope offset'
        internal = 1, 0
        lm34 = 55.56, 255.37

    class TemperatureUnit(NameEnum):
        """
        Temperature unit (to be returned)
        """
        _init_ = 'ef_config_a'
        K = 0
        C = 1
        F = 2

    def set_ain_thermocouple(
            self,
            pos_channel: int,
            thermocouple: Union[None, str, ThermocoupleType],
            cjc_address: int = 60050,
            cjc_type: Union[str, CjcType] = CjcType.internal,
            vrange: float = 0.01,
            resolution: int = 10,
            unit: Union[str, TemperatureUnit] = TemperatureUnit.K) -> None:
        """
        Set the analog input channel to thermocouple mode.

        :param pos_channel: is the analog input channel of the positive part of the
            differential pair
        :param thermocouple: None to disable thermocouple mode, or string specifying
            the thermocouple type
        :param cjc_address: modbus register address to read the CJC temperature
        :param cjc_type: determines cjc slope and offset, 'internal' or 'lm34'
        :param vrange: measurement voltage range (10, 1, 0.1, 0.01)
        :param resolution: resolution index (T7 Pro: 0-12)
        :param unit: is the temperature unit to be returned ('K', 'C' or 'F')
        :raises LabJackError: if parameters are unsupported
        """

        if thermocouple is None:
            thermocouple = self.ThermocoupleType.NONE
        else:
            thermocouple = self.ThermocoupleType(thermocouple)

        unit = self.TemperatureUnit(unit)

        cjc_type = self.CjcType(cjc_type)

        self.set_ain_differential(pos_channel=pos_channel, differential=True)
        self.set_ain_range(pos_channel, vrange)
        self.set_ain_resolution(pos_channel, resolution)
        self.set_ain_range(pos_channel + 1, vrange)
        self.set_ain_resolution(pos_channel+1, resolution)

        # specify thermocouple mode
        self.com.write_name(
            "AIN{}_EF_INDEX".format(pos_channel), thermocouple.ef_index
        )

        # specify the units for AIN#_EF_READ_A and AIN#_EF_READ_C (0 = K, 1 = C, 2 = F)
        self.com.write_name(
            "AIN{}_EF_CONFIG_A".format(pos_channel), unit.ef_config_a
        )

        # specify modbus address for cold junction reading CJC
        self.com.write_name(
            "AIN{}_EF_CONFIG_B".format(pos_channel), cjc_address
        )

        # set slope for the CJC reading, typically 1
        self.com.write_name(
            f'AIN{pos_channel}_EF_CONFIG_D', cjc_type.slope
        )

        # set the offset for the CJC reading, typically 0
        self.com.write_name(
            f'AIN{pos_channel}_EF_CONFIG_E', cjc_type.offset
        )

    def read_thermocouple(self, pos_channel: int) -> float:
        """
        Read the temperature of a connected thermocouple.

        :param pos_channel: is the AIN number of the positive pin
        :return: temperature in specified unit
        """

        return round(
                self.com.read_name(
                    "AIN{}_EF_READ_A".format(pos_channel)
                ), 2)
