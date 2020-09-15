import application_params as ap

"""
Message Structure:

    2 bytes of message length + the word '~Available' + 2 byte of Available cpus
    = 0x000A+b'~Handshake'
"""


class Available:
    id = b'~Available'
    id_len = len(id)
    msg_len = ap.INT_LEN + id_len + ap.INT_LEN

    def __init__(self, available):
        self.available = available

    def to_sendable(self):
        return int.to_bytes(self.id_len, ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED) \
               + self.id \
               + int.to_bytes(self.available, ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)

    @staticmethod
    def is_this(data: bytes):

        # Check if the bytes are the right length
        if len(data) < Available.msg_len:
            return False

        # Decode bytes
        msz = int.from_bytes(data[:ap.INT_LEN], byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
        msg = data[ap.INT_LEN:msz + ap.INT_LEN]

        # Check if decoded length is correct
        if msz != Available.id_len:
            return False

        # Check if decoded message is correct
        if msg != Available.id:
            return False

        # All Checks Passed
        return True

    @staticmethod
    def from_sendable(data: bytes):
        if Available.is_this(data):
            avail = int.from_bytes(data[ap.INT_LEN + Available.id_len:ap.INT_LEN + Available.id_len+ap.INT_LEN],
                                   byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
            return Available(avail), True
        return None, False
