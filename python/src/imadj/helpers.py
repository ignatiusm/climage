# Helper functions


def le(byte_str):
    """
    Converts a LITTLE ENDIAN bytestring into an integer
    """
    n = 0
    for index, byte in enumerate(byte_str):
        n += byte << (index * 8)
    return n
