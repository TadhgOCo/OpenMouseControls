def get_device_pid():
    buf = bytearray(65)

    buf[3] = 0x01
    buf[4] = 0x06

    buf[6] = 0x8B
    buf[7] = 0x02

    return bytes(buf)