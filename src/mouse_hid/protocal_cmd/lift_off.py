def get_lift_off(ProfileID):
    buf = bytearray(65)

    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x88

    if ProfileID == -1:
        buf[4] = 0x01

    else:
        buf[7] = ProfileID
        buf[4] = 0x02
    
    return bytes(buf)

def set_lift_off(ProfileID, dist):
    buf = bytearray(65)

    buf[3] = 0x02

    buf[5] = 0x01
    buf[6] = 0x08

    if ProfileID == -1:
        buf[4] = 0x01
        buf[7] = dist

    else:
        buf[4] = 0x02
        buf[7] = ProfileID
        buf[8] = dist

    return bytes(buf)
    #return True # NOTE: Look at the scource code (why?)