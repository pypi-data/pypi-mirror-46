"""
Tests for the dev.labjack module.
"""

import pytest

from hvl_ccb.dev import LabJack, LabJackError
from tests.masked_comm import MaskedLJMCommunication


@pytest.fixture(scope="module")
def com_config():
    return {
        'device_type': 'ANY',
        'connection_type': 'ANY',
        'identifier': '-2'  # identifier = -2 specifies LJM DEMO mode, see
        # https://labjack.com/support/software/api/ljm/demo-mode
    }


@pytest.fixture
def started_dev_comm(com_config):
    com = MaskedLJMCommunication(com_config)
    with LabJack(com) as lj:
        yield lj, com


def test_instantiation(com_config):
    lj = LabJack(com_config)
    assert lj is not None


def test_get_serial_number(started_dev_comm):
    lj, com = started_dev_comm
    com.put_name("SERIAL_NUMBER", 1234)
    assert lj.get_serial_number() == 1234


def test_get_sbus_temp(started_dev_comm):
    lj, com = started_dev_comm
    com.put_name("SBUS0_TEMP", 298.15)
    assert lj.get_sbus_temp(0) == 298.15


def test_get_sbus_rh(started_dev_comm):
    lj, com = started_dev_comm
    com.put_name("SBUS0_RH", 40.5)
    assert lj.get_sbus_rh(0) == 40.5


def test_get_ain(started_dev_comm):
    lj, com = started_dev_comm
    com.put_name("AIN0", 1.23)
    assert lj.get_ain(0) == 1.23


def test_set_ain_range(started_dev_comm):
    lj, com = started_dev_comm

    lj.set_ain_range(0, 10)
    assert com.get_written() == ('AIN0_RANGE', 10)

    lj.set_ain_range(0, 0.1)
    assert com.get_written() == ('AIN0_RANGE', 0.1)

    with pytest.raises(LabJackError):
        lj.set_ain_range(0, 0.2)
    assert com.get_written() is None


def test_set_ain_resolution(started_dev_comm):
    lj, com = started_dev_comm

    lj.set_ain_resolution(0, 10)
    assert com.get_written() == ('AIN0_RESOLUTION_INDEX', 10)
    lj.set_ain_resolution(0, 0)
    assert com.get_written() == ('AIN0_RESOLUTION_INDEX', 0)

    with pytest.raises(LabJackError):
        lj.set_ain_resolution(0, -14)
    assert com.get_written() is None

    with pytest.raises(LabJackError):
        lj.set_ain_resolution(0, 13)
    assert com.get_written() is None


def test_set_ain_differential(started_dev_comm):
    lj, com = started_dev_comm

    lj.set_ain_differential(4, True)
    assert com.get_written() == ('AIN4_NEGATIVE_CH', 5)

    lj.set_ain_differential(4, False)
    assert com.get_written() == ('AIN4_NEGATIVE_CH', 199)

    with pytest.raises(LabJackError):
        lj.set_ain_differential(5, True)
    assert com.get_written() is None

    with pytest.raises(LabJackError):
        lj.set_ain_differential(14, True)
    assert com.get_written() is None


def test_set_ain_thermocouple(started_dev_comm):
    lj, com = started_dev_comm

    lj.set_ain_thermocouple(0, None)
    lj.set_ain_thermocouple(0, LabJack.ThermocoupleType.NONE)
    lj.set_ain_thermocouple(0, 'K')
    lj.set_ain_thermocouple(0, LabJack.ThermocoupleType.K)
    with pytest.raises(ValueError):
        lj.set_ain_thermocouple(0, 'B')

    lj.set_ain_thermocouple(0, thermocouple='T', unit='F')
    lj.set_ain_thermocouple(0, thermocouple='T', unit=LabJack.TemperatureUnit.F)
    with pytest.raises(ValueError):
        lj.set_ain_thermocouple(0, 'K', unit='B')

    lj.set_ain_thermocouple(0, thermocouple='T', cjc_type='lm34')
    lj.set_ain_thermocouple(0, thermocouple='T', cjc_type=LabJack.CjcType.lm34)
    with pytest.raises(ValueError):
        lj.set_ain_thermocouple(0, 'K', cjc_type='LM35')


def test_read_thermocouple(started_dev_comm):
    lj, com = started_dev_comm
    com.put_name('AIN0_EF_READ_A', 244.3)
    assert lj.read_thermocouple(0) == 244.30
