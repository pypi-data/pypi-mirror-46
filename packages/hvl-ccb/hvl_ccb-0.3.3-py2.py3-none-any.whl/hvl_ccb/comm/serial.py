"""
Communication protocol for serial ports. Makes use of the `pySerial
<https://pythonhosted.org/pyserial/index.html>`_ library.
"""

# Note: PyCharm does not recognize the dependency correctly, it is added as pyserial.
import serial

from .base import CommunicationProtocol
from ..configuration import configdataclass
from ..utils.enum import ValueEnum, unique


@configdataclass
class SerialCommunicationConfig:
    """
    Configuration dataclass for :class:`SerialCommunication`.
    """

    @unique
    class Parity(ValueEnum):
        """
        Serial communication parity.
        """
        EVEN = serial.PARITY_EVEN
        MARK = serial.PARITY_MARK
        NAMES = serial.PARITY_NAMES
        NONE = serial.PARITY_NONE
        ODD = serial.PARITY_ODD
        SPACE = serial.PARITY_SPACE

    @unique
    class Stopbits(ValueEnum):
        """
        Serial communication stopbits.
        """
        ONE = serial.STOPBITS_ONE
        ONE_POINT_FIVE = serial.STOPBITS_ONE_POINT_FIVE
        TWO = serial.STOPBITS_TWO

    @unique
    class Bytesize(ValueEnum):
        """
        Serial communication bytesize.
        """
        FIVEBITS = serial.FIVEBITS
        SIXBITS = serial.SIXBITS
        SEVENBITS = serial.SEVENBITS
        EIGHTBITS = serial.EIGHTBITS

    #: Port is a string referring to a COM-port (e.g. ``'COM3'``) or a URL.
    #: The full list of capabilities is found `on the pyserial documentation
    #: <https://pythonhosted.org/pyserial/url_handlers.html>`_.
    port: str

    #: Baudrate of the serial port
    baudrate: int

    #: Parity to be used for the connection.
    parity: (str, Parity)

    #: Stopbits setting, can be 1, 1.5 or 2.
    stopbits: (int, float, Stopbits)

    #: Size of a byte, 5 to 8
    bytesize: (int, Bytesize)

    #: The terminator character. Typically this is ``b'\r\n'`` or ``b'\n'``, but can
    #: also be ``b'\r'`` or other combinations.
    terminator: bytes = b'\r\n'

    #: Timeout in seconds for the serial port
    timeout: (int, float) = 2

    def clean_values(self):
        if not isinstance(self.parity, self.Parity):
            self.force_value('parity', self.Parity(self.parity))

        if not isinstance(self.stopbits, self.Stopbits):
            self.force_value('stopbits', self.Stopbits(self.stopbits))

        if not isinstance(self.bytesize, self.Bytesize):
            self.force_value('bytesize', self.Bytesize(self.bytesize))


class SerialCommunication(CommunicationProtocol):
    """
    Implements the Communication Protocol for serial ports.
    """

    ENCODING = 'utf-8'
    UNICODE_HANDLING = 'replace'

    def __init__(self, configuration):
        """
        Constructor for SerialCommunication.
        """

        super().__init__(configuration)

        # create the serial port specified in the configuration
        with serial.serial_for_url(self.config.port, do_not_open=True) as self.ser:
            self.ser.baudrate = self.config.baudrate
            self.ser.parity = self.config.parity.value
            self.ser.stopbits = self.config.stopbits.value
            self.ser.bytesize = self.config.bytesize.value
            self.ser.timeout = self.config.timeout

    @staticmethod
    def config_cls():
        return SerialCommunicationConfig

    def open(self):
        """
        Open the serial connection.
        """

        # open the port
        with self.access_lock:
            self.ser.open()

    def close(self):
        """
        Close the serial connection.
        """

        # close the port
        with self.access_lock:
            self.ser.close()

    def write_text(self, text: str):
        """
        Write text to the serial port. The text is encoded and terminated by
        the configured terminator.

        :param text: Text to send to the port.
        """

        with self.access_lock:
            self.ser.write(text.encode(self.ENCODING, self.UNICODE_HANDLING)
                           + self.config.terminator)

    def read_text(self) -> str:
        """
        Read one line of text from the serial port. The input buffer may
        hold additional data afterwards, since only one line is read.

        :return: String read from the serial port.
        """

        with self.access_lock:
            decoded = self.ser.readline().decode(self.ENCODING)

        return decoded
