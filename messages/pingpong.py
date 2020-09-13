import application_params as ap

"""
Message Structure:

    2 bytes of message length + the word '~Ping'
    = 0x000A+b'~Handshake'
"""


class Ping:
    id = b'~Ping'
    id_len = len(id)

    def to_sendable(self):
        return int.to_bytes(self.id_len, ap.INT_LEN, byteorder=ap.BYTE_ORDER, signed=ap.SIGNED) + self.id

    @staticmethod
    def is_this(data: bytes):

        # Check if the bytes are the right length
        if len(data) < ap.INT_LEN + Ping.id_len:
            return False

        # Decode bytes
        msz = int.from_bytes(data[:ap.INT_LEN], byteorder=ap.BYTE_ORDER, signed=ap.SIGNED)
        msg = data[ap.INT_LEN:msz + ap.INT_LEN]

        # Check if decoded length is correct
        if msz != Ping.id_len:
            return False

        # Check if decoded message is correct
        if msg != Ping.id:
            return False

        # All Checks Passed
        return True

    @staticmethod
    def from_sendable(data: bytes):
        if Ping.is_this(data):
            return Ping(), True
        return None, False
