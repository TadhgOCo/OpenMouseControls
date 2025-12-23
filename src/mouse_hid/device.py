import hid

# --- Configuration ---
# Target identifiers from Config/xvi_models.xlsx and decompiled code
# Includes both Factory defaults (0x258A) and Customer models (e.g., R6 0x373E)
TARGET_VENDORS = [0x258A, 0x373E] 
TARGET_INTERFACE_USAGE = 0xFF00 # Vendor Defined Usage Page often used for these
REQUIRED_REPORT_LENGTH = 65     # [cite: 14, 42]

def find_device(output=[None]):
    print("Searching for device...")

    for d in hid.enumerate():
        if d['vendor_id'] not in TARGET_VENDORS:
            continue

        try:
            h = hid.Device(path=d["path"])

            # Try a harmless feature report read
            try:
                h.get_feature_report(0x02, 65)
            except Exception:
                h.close()
                continue

            print(f"Found device: {d.get('product_string')} ({hex(d['vendor_id'])}:{hex(d['product_id'])})")
            output[0] = h
            return h

        except Exception as e:
            print(f"Failed to open candidate: {e}")

    return None

#x = [None]
#find_device(x)
#print(x)

"""
def send(device, type, data):
    \"""Sends the DPI command and handles the protocol timing.\"""
    CreatePacketFunc = protocal.get
    packet = CreatePacketFunc(data)

    print(f"Sending Update ({data})...")
    # Send Feature Report [cite: 16, 139]
    # Note: send_feature_report expects the first byte to be the Report ID
    device.send_feature_report(packet)
    
    # Protocol requires ~30ms delay between Set and Get [cite: 28, 140, 217]
    time.sleep(0.03) 
    
    # Verify Success (Get Feature Report) [cite: 26]
    # We ask for 65 bytes. The Report ID (0x02) is passed to indicate which report we want.
    try:
        response = device.get_feature_report(0x02, 65)
        out1 = response[7]
        out2 = response[8]
        print(out1, out2)
        
        # Check success byte at index 1 (Windows index) -> Index 2 or 1 in Python list depending on backend?
        # Standard HIDAPI returns [ReportID, Data...].
        # The spec says success byte is 0xA1 at Windows byte[1][cite: 73, 121].
        # In Linux HIDAPI buffer: [0]=ReportID, [1]=Status.
        if response and (response[0] == 0xA1 or response[1] == 0xA1):
            print("Success: Device acknowledged command (0xA1).")
        else:
            print(f"Warning: Device did not return success code. Raw: {response[:5]}")
            
    except Exception as e:
        print(f"Read failed (Device might be silent): {e}")"""