def get_angle_snap(profile_id):
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x01
    buf[5] = 0x01
    buf[6] = 0x84

    if not profile_id == -1:
        buf[7] = profile_id
        buf[4] = 0x02
    
    return bytes(buf)  

def set_angle_snap(enable, profile_id):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x01
    buf[5] = 0x01
    buf[6] = 0x04
    buf[7] = enable

    if not profile_id == -1:
        buf[4] = 0x02
        buf[7] = profile_id
        buf[8] = enable

    return bytes(buf)