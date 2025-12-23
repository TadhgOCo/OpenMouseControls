def set_motion_sync(enable, profile_id):
    buf = bytearray(65)

    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x09
    if profile_id == -1:
        buf[4] = 0x01
        buf[7] = enable

    else:
        buf[7] = profile_id
        buf[8] = enable
        buf[4] = 0x02

    return bytes(buf)

def get_motion_sync(profile_id):
    buf = bytearray(65)

    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x89
    if profile_id == -1:
        buf[4] = 0x01

    else:
        buf[7] = profile_id
        buf[4] = 0x02

    return bytes(buf)