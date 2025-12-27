dicPollingRate = {}

dicPollingRate[8] = 125
dicPollingRate[4] = 250
dicPollingRate[2] = 500
dicPollingRate[1] = 1000
dicPollingRate[32] = 2000
dicPollingRate[64] = 4000
dicPollingRate[128] = 8000

def set_polling_rate(PollingRate, profile_id):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x01
    buf[5] = 0x01
    
    if profile_id != -1:
        buf[4] = 0x01
        buf[7] = PollingRate
    else:
        buf[4] = 0x02
        buf[7] = profile_id
        buf[8] = PollingRate

    return bytes(buf)

def get_polling_rate(profile_id):
    buf = bytearray(65)

    buf[3] = 0x02
    buf[4] = 0x01
    buf[5] = 0x01
    buf[6] = 0x80
    if profile_id != -1:
        buf[4] = 0x01
    else:
        buf[4] = 0x02
        buf[7] = profile_id
        

    return bytes(buf)