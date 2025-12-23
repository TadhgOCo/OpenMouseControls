def get_button(profileID, ButtonID, functionID, data, byte_0): # NOTE: need to oberseve source code
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x05 + byte_0
    buf[5] = 0x03
    buf[6] = 0x80
    buf[7] = profileID
    buf[8] = ButtonID
    buf[9] = 0x00
    buf[10] = functionID
    buf[11] = byte_0 # ?

    for i in range(byte_0):
        buf[12 + i] = data[i]

    return bytes(buf)

def set_button(profileID, ButtonID, functionID, data, byte_0): # NOTE: need to oberseve source code
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x05 + byte_0
    buf[5] = 0x03
    buf[6] = 0x00
    buf[7] = profileID
    buf[8] = ButtonID
    buf[9] = 0x00
    buf[10] = functionID
    buf[11] = byte_0 # ?

    for i in range(byte_0):
        buf[12 + i] = data[i]

    return bytes(buf)