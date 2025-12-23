def pair_to_device(isPaired):
    buf = bytearray(65)

    buf[3] = 0x1
    buf[4] = 0x1
    buf[6] = 0x0C
    buf[7] = isPaired # () NOTE: check source to see possible values

    return bytes(buf)

def get_paired():
    buf = bytearray(65)

    buf[3] = 0x01
    buf[6] = 0x8C

    return bytes(buf)