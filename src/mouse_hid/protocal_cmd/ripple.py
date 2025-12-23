def get_ripple_contol(profile_id):
    buf = bytearray(65)
    
    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x8A

    if profile_id == -1: 
        buf[4] = 0x01

    else:
        buf[7] = profile_id
        buf[4] = 0x02
    
    return bytes(buf)  

def set_ripple_contol(enable, profile_id):
    buf = bytearray(65)

    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x0A

    if profile_id == -1:
        buf[4] = 0x01
        buf[7] = enable

    else:
        buf[4] = 0x02
        buf[7] = profile_id
        buf[8] = enable

    return bytes(buf)