def set_dongle_LED(enable, profile_id):
    buf = bytearray(65)

    buf[4] = 0x02
    buf[5] = 0x02
    buf[6] = 0x04
    buf[7] = profile_id
    buf[8] = enable
    
    return bytes(buf)

def get_dongle_LED(profile_id):
    buf = bytearray(65)

    buf[4] = 0x02
    buf[5] = 0x02
    buf[6] = 0x84
    buf[7] = profile_id

    return bytes(buf)