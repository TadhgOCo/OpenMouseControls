def get_sleep(Profile_ID):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x02
    buf[6] = 0x87

    if not Profile_ID == -1:
        buf[4] = 0x03
        buf[7] = Profile_ID

    return bytes(buf)

def set_sleep(SleepTime, Profile_ID):
    buf = bytearray(65)

    idx_1 = 256%SleepTime
    SleepTimeBytes = [idx_1, (SleepTime-idx_1)/256]

    buf[3] = 0x02
    buf[4] = 0x02
    buf[6] = 0x07

    if Profile_ID == -1:
        buf[4] = 0x03
        buf[7] = Profile_ID
        buf[8] = SleepTimeBytes[0]
        buf[9] = SleepTimeBytes[1]
    else:
        buf[7] = SleepTimeBytes[0]
        buf[8] = SleepTimeBytes[1]

    return bytes(buf)