"""
Tests for the .comm.labjack_ljm subpackage.
"""

import logging

import pytest

from hvl_ccb.comm import (
    LJMCommunication,
    LJMCommunicationConfig,
    LJMCommunicationError,
)

logging.disable(logging.ERROR)


@pytest.fixture(scope='module')
def testconfig():
    return {
        'identifier': '-2'
    }


@pytest.fixture
def com(testconfig):
    with LJMCommunication(testconfig) as com:
        yield com


def test_labjack_config_cleaning():
    with pytest.raises(ValueError):
        LJMCommunicationConfig(device_type='T5')

    with pytest.raises(ValueError):
        LJMCommunicationConfig(connection_type='Gardena')


def test_labjack_config_enums():
    config = LJMCommunicationConfig(device_type=LJMCommunicationConfig.DeviceType.T4)
    assert str(config.device_type) == "T4"

    config = LJMCommunicationConfig(
        connection_type=LJMCommunicationConfig.ConnectionType.TCP)
    assert str(config.connection_type) == "TCP"


def test_open(testconfig):
    com = LJMCommunication(testconfig)
    com.open()
    com.open()

    failing_config = dict(testconfig)
    failing_config['identifier'] = 'this_is_an_invalid_identifier'
    com = LJMCommunication(failing_config)
    with pytest.raises(LJMCommunicationError):
        com.open()


def test_read_name(com):
    with pytest.raises(LJMCommunicationError):
        com.read_name("SERIAL_NUMBER")

    with pytest.raises(LJMCommunicationError):
        com.read_name("SERIAL_NUMBER", "SERIAL_NUMBER")

    with pytest.raises(TypeError):
        com.read_name(123)


def test_write_name(com):
    with pytest.raises(LJMCommunicationError):
        com.write_name("test", 0)

    with pytest.raises(LJMCommunicationError):
        com.write_names(["test1", "test2"], [1, 2])

    with pytest.raises(TypeError):
        com.write_name(123, 456)


def test_write_address(com):
    with pytest.raises(NotImplementedError):
        com.write_address(1234, 5678)
