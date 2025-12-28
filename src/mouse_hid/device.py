import hid

# --- Configuration ---
TARGET_VENDORS = [0x258A, 0x373E] 
TARGET_INTERFACE_USAGE = 0xFF00
REQUIRED_REPORT_LENGTH = 65

def find_device(output=[None]):
    print("Searching for device...")

    for d in hid.enumerate():
        if d['vendor_id'] not in TARGET_VENDORS:
            continue

        try:
            h = hid.Device(path=d["path"])
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