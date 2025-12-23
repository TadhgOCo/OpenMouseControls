def set_dpi_stage_info(stage_count, dpi_value, profileID):
    """
    Constructs the SetDPIStageInfo packet[cite: 96, 228].
    
    Structure based on trace[cite: 263]:
    [0] Report ID (0x02)
    [1] Length (StageCount * 4 + 2)
    [2] SubCommand (0x01)
    [3] Code (0x01)
    [4] ProfileID (0x01)
    [5] StageCount (0x01)
    [6-9] DPI Data (X High, X Low, Y High, Y Low) - Big Endian [cite: 240]
    """
    
    idx_1 = 256%dpi_value
    dpi_bytes = [int( (dpi_value-idx_1)/256 ), idx_1]

    buf = bytearray(65)
    
    buf[3] = 0x02  # Report ID [cite: 52]
    
    # Windows Index [4] corresponds to Linux Index [1] [cite: 66]
    buf[4] = (stage_count * 4) + 2 
    
    buf[5] = 0x01  # Fixed [cite: 103]
    buf[6] = 0x01  # Fixed [cite: 104]
    buf[7] = profileID
    buf[8] = stage_count
    
    # Copy DPI X and Y
    buf[9] = dpi_bytes[0]
    buf[10] = dpi_bytes[1]
    buf[11] = dpi_bytes[0]
    buf[12] = dpi_bytes[1]
    
    return bytes(buf)

def get_dpi_stage(profileID): # GetActiveDPI
  
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x02
    buf[5] = 0x01
    buf[6] = 0x82
    buf[7] = profileID
    
    return bytes(buf)

def set_dpi_stage(profileID, stage):
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x02
    buf[5] = 0x01
    buf[6] = 0x02
    buf[7] = profileID
    buf[8] = stage
    
    return bytes(buf)

def get_dpi_stage_info(profileID, stage): # GetDPIStageInfo
    buf = bytearray(65)
    
    buf[3] = 0x02
    buf[4] = 0x0A
    buf[5] = 0x01
    buf[6] = 0x81
    buf[7] = profileID
    buf[8] = stage
    
    return bytes(buf)