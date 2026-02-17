import hid

# --- Configuration ---
TARGET_VENDORS = [0x258A, 0x373E]

TARGET_NAMES = [
    'X3',
    'X3 PRO',
    'X3 MAX',
    'X8 SE',
    'X8 PLUS',
    'X8 PRO',
    'X8 ULTRA',
    'X8 ULTIMATE',
    'X11',
    'X11 SE',
    'R11 ULTRA',
    'R5 ULTRA',
    'G3',
    'G3 PRO',
    'X6',
    'R1',
    'R3',
    'X1',
    'R2',
    'X5',
    'X2',
    'V6',
    'V3',
    'V5',
    'R6'
]

SUFFIX_LIST = [
    "PRO",
    "MAX",
    "SE",
    "PLUS",
    "ULTRA",
    "ULTIMATE"
]

def find_device(output=[None]):
    print("Searching for device...")

    for d in hid.enumerate():
        product_str = d.get('product_string')
        
        product_str = product_str.split(" ")
        if product_str[1] in SUFFIX_LIST:
            device_name = product_str[0] + product_str[1]
        else:
            device_name = product_str[0]

        if d['vendor_id'] not in TARGET_VENDORS or device_name not in TARGET_NAMES:
            continue

        try:
            h = hid.Device(path=d["path"])
            try:
                h.get_feature_report(0x02, 65)
            except Exception:
                h.close()
                continue

            
            print(f"Found device: {product_str} ({hex(d['vendor_id'])}:{hex(d['product_id'])})")
            output[0] = (h, product_str)
            return (h, product_str)

        except Exception as e:
            print(f"Failed to open candidate: {e}")

    return None