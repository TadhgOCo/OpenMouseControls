def get_debounce(profileID):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x02
    buf[6] = 0x88
    buf[7] = profileID

    return bytes(buf)

def set_debounce(DebounceTime, profileID):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x02
    buf[6] = 0x08
    buf[7] = profileID
    buf[8] = DebounceTime

    return bytes(buf)