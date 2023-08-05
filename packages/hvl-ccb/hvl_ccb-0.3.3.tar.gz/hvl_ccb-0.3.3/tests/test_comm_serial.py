"""
Tests for .comm sub-package
"""
import dataclasses
import time

import pytest

from hvl_ccb.comm import SerialCommunication, SerialCommunicationConfig


@pytest.fixture(scope="module")
def testconfig():
    return SerialCommunicationConfig(
        port="loop://?logging=debug",
        baudrate=115200,
        parity=SerialCommunicationConfig.Parity.NONE,
        stopbits=SerialCommunicationConfig.Stopbits.ONE,
        bytesize=SerialCommunicationConfig.Bytesize.EIGHTBITS,
        terminator=b'\r\n',
        timeout=0.2
    )


def test_serial_config(testconfig):
    with pytest.raises(ValueError):
        dataclasses.replace(testconfig, parity='B')

    with pytest.raises(ValueError):
        dataclasses.replace(testconfig, stopbits=2.5)

    with pytest.raises(ValueError):
        dataclasses.replace(testconfig, bytesize=9)


def _decode_terminator(testconfig):
    return testconfig.terminator.decode(SerialCommunication.ENCODING)


def test_timeout(testconfig):
    with SerialCommunication(testconfig) as sc:
        started_at = time.time()
        assert sc.read_text() == ''
        elapsed = time.time() - started_at
        timeout = testconfig.timeout
        assert elapsed >= timeout
        assert elapsed < 1.25 * timeout


def _test_serial_communication(testconfig, sc):
    # send something
    test_strings = ["Test message 1",
                    "testmessage2",
                    "190testmessage: 3",
                    ]

    for t in test_strings:
        # send line
        sc.write_text(t)

        # read back line
        answer = sc.read_text()

        assert answer == t + _decode_terminator(testconfig)


def test_serial_communication(testconfig):
    """
    Tests SerialCommunication
    """

    # manually open/close port
    sc = SerialCommunication(testconfig)
    assert sc is not None
    sc.open()
    _test_serial_communication(testconfig, sc)
    sc.close()

    # or use with statement
    with SerialCommunication(testconfig) as sc:
        assert sc is not None
        _test_serial_communication(testconfig, sc)
