def get_dev_firmware_ver():
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x10
    buf[6] = 0x81
    
    return bytes(buf)

def get_dongle_firmware_ver():
    buf = bytearray(65)
    
    buf[3] = 0x00
    buf[4] = 0x10
    buf[6] = 0x81
    
    return bytes(buf)