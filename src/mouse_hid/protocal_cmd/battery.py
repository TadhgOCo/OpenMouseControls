def get_battery():
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x02
    buf[5] = 0x00
    buf[6] = 0x83
    
    return bytes(buf)   