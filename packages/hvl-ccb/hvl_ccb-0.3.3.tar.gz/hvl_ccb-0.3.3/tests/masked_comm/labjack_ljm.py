"""
Masked version of LJM Communication for testing purposes.
"""

from collections import defaultdict
from queue import Queue
from typing import Union, Sequence

from hvl_ccb import comm


class MaskedLJMCommunication(comm.LJMCommunication):
    """
    Masks the LJMCommunication protocol disabling read and write to be able to test
    the functionality of devices without
    """

    def __init__(self, configuration):
        super().__init__(configuration)

        self._read_buffer = defaultdict(Queue)
        self._write_buffer = Queue()

    def read_name(self,  *names: str):

        out = [
            self._read_buffer[name].get() if not self._read_buffer[name].empty() else 0
            for name in names
        ]

        return out[0] if len(out) == 1 else out

    def write_name(self,
                   name: Union[Sequence[str], str],
                   value: Union[Sequence[object], object]):

        if isinstance(name, str):
            name = [name]
            value = [value]

        for pair in zip(name, value):
            self._write_buffer.put(pair)

    def write_address(self,
                      address: Union[Sequence[int], int],
                      value: Union[Sequence[object], object]):
        pass

    def put_name(self, name: str, value: object):
        self._read_buffer[name].put(value)

    def get_written(self):
        return self._write_buffer.get() if not self._write_buffer.empty() else None
