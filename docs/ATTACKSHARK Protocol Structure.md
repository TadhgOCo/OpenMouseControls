# ATTACKSHARK Protocol Documentation

> [!IMPORTANT]
> **Core Protocol Concept**
> **Command IDs are NOT unique.**
> The firmware identifies a command using these three bytes:
> 1. **Category** (Byte 4)
> 2. **Compatibility** (Byte 5)
> 3. **Command ID** (Byte 6)
> 
> 
> For example, **Angle Snap** and **Dongle LED** both use Command ID `0x04` (SET) / `0x84` (GET), but they have different Categories (`0x01` vs `0x02`).

## 1. Protocol Packet Structure

**Packet Length:** 65 Bytes

**Old Protocol:**
| Byte Index | Field | Description |
| --- | --- | --- |
| **[0]** | Report ID | Usually `0x00` (Handled Automatically). |
| **[3]** | Target Device | `0x00` = Dongle, `0x01` = Keyboard, `0x02` = Mouse. |
| **[4]** | Category | Feature namespace (eg., Performance, Lighting). |
| **[5]** | Compatibility | Feature type (eg., Value, Toggle, Data). |
| **[6]** | Command ID | Action to preform |
| **[7+]** | Payload | Data payload (Little Endian or Big Endian varies by feature). |

**New Protocol:**
| Byte Index | Field | Description |
| --- | --- | --- |
| **[0]** | Report ID | Usually `0x00` (Handled Automatically). |
| **[3]** | Target Device | `0x00` = Dongle, `0x01` = Keyboard, `0x02` = Mouse. |
| **[4]** | Category | The feature namespace (e.g., Performance, Lighting). |
| **[5]** | Compatibility | The feature type (e.g., Value, Toggle, Data). |
| **[6]** | Command ID | Action to preform |
| **[7]** | Parameter 1 | Profile ID (1-6), Sub-ID, or MSB of a value. |
| **[8+]** | Payload | Data payload (Little Endian or Big Endian varies by feature). |

## 2. Protocol Value

### Target Device  (Byte 3)

| Value | Device |
| --- | --- |
| `0x00` | Dongle / Receiver |
| `0x01` | Keyboard |
| `0x02` | Mouse |

### Feature Categories (Byte 4)

| Value | Category Name |
| --- | --- |
| `0x00` | Buttons, macros, pairing, general config |
| `0x01` | Performance (polling, motion sync, angle snap, sensor) |
| `0x02` | Power, system, reset, debounce, lighting toggle |
| `0x03` | Lighting (global brightness) |
| `0x04` | RF / Address |
| `0x06` | Identity / Metadata |
| `0x0A` | DPI Stage Data |
| `0x10` | Firmware Version |
| `0x13` | DPI Colors |

### Feature Compatibility (Byte 5)

| Value | Meaning |
| --- | --- |
| `0x00` | General / default feature |
| `0x01` | Performance-related (DPI, polling, motion sync, angle snap, LOD) |
| `0x02` | Lighting / power / RF |
| `0x03` | Button Mapping |
| `0x04` | Macros / button bindings |

---

## 3. Command Tables  (Byte 6)

> [!NOTE]
> * **SET ID:** Used to write configuration.
> * **GET ID:** Used to read configuration.
> * **Payload:** Check the "Decoding Values" section for details on Polling Rate and specific bitmasks.
> 128 is taken from all GET Command ids to get the SET request for that feature.
> 
> 

### Performance & Sensor (Category `0x01`)

| Feature Name | Category | Comp | Set ID | Get ID | Payload Notes |
| --- | --- | --- | --- | --- | --- |
| **Polling Rate** | `0x01` | `0x01` | `0x00` | `0x80` | See Below. |
| **Angle Snap** | `0x01` | `0x01` | `0x04` | `0x84` | `1` = On, `0` = Off |
| **Motion Sync** | `0x01` | `0x01` | `0x09` | `0x89` | `1` = On, `0` = Off |
| **Ripple Control** | `0x01` | `0x01` | `0x0A` | `0x8A` | `1` = On, `0` = Off |
| **LOD (Lift Off)** | `0x01` | `0x01` | `0x08` | `0x88` | `1` = 1mm, `2` = 2mm | # NOTE: Not Correct
| **Sensor Wake** | `0x01` | `0x01` | `0x11` | `0x91` | Wake sensor on move (`1`/`0`) |

### Power & System (Category `0x02`)

| Feature Name | Category | Comp | Set ID | Get ID | Payload Notes |
| --- | --- | --- | --- | --- | --- |
| **Sleep Time** | `0x02` | `0x00` | `0x07` | `0x87` | Bytes [7-8] (Big Endian) |
| **Debounce** | `0x02` | `0x00` | `0x08` | `0x88` | Byte [8] = ms (e.g., 4ms) |
| **Dongle LED** | `0x02` | `0x02` | `0x04` | `0x84` | `1` = On, `0` = Off |
| **Active DPI** | `0x02` | `0x01` | `0x02` | `0x82` | Byte [8] = Active Stage Index (1-6) |
| **Battery Level** | `0x02` | `0x00` | - | `0x83` | Byte [7] = Status, [8] = Percent |
| **Reset Profile** | `0x02` | `0x00` | `0xC0` | - | **Destructive Reset** |

### Configuration (Category `0x00` / `0x0A` / `0x13`)

| Feature Name | Category | Comp | Set ID | Get ID | Payload Notes |
| --- | --- | --- | --- | --- | --- |
| **DPI Stages** | `0x0A` | `0x01` | `0x01` | `0x81` | See Below |
| **DPI Colors** | `0x13` | `0x02` | `0x01` | `0x81` | RGB Arrays |
| **Button Map** | `0x00` | `0x03` | `0x00` | `0x80` | Map clicks to keys |
| **Macros** | `0x00` | `0x04` | `0x03` | - | Set Macro Data Block |
| **Firmware Ver** | `0x02` | `0x10` | - | `0x81` | Read Firmware Version |

#### Profile ID (Byte 7):
The Profile ID is a value that ranges from 1-6 but it is possible access numbers up to 64 and still get a success code. This may cause errors with data storage space and is unsupported by the manufacturer.

---

## 4. Decoding Values

### A. Polling Rate Map

The polling rate is encoded as a specific byte value, not the direct Hz number.

| Protocol Value | Polling Rate (Hz) |
| --- | --- |
| `1 / 16` | 1000 Hz |
| `2` | 500 Hz |
| `4` | 250 Hz |
| `8` | 125 Hz |
| `32` | 2000 Hz |
| `64` | 4000 Hz |
| `128` | 8000 Hz |

### B. DPI Stages & Colors

DPI is managed in two parts: The DPI Value and the DPI Color. Minimum value of 50, Maximum value varies by model, Step value is 50.

**1. DPI Stage Info (Category `0x0A`)**

* **Set Packet:** `[4]=0x10`, `[5]=0x01`, `[6]=0x01`
* **Get Packet:** `[4]=0x10`, `[5]=0x01`, `[6]=0x81`
* **Payload Structure:**
* `Byte [7]`: Total stages (eg., 6)
* `Byte [8]`: Current Stage Index being edited
* `Byte [9+]`: DPI Values (2 bytes per stage, Big Endian).



**2. DPI Colors (Category `0x13`)**

_(No idea why this exists)_
* **Set Packet:** `[4]=0x13`, `[5]=0x02`, `[6]=0x01`
* **Payload:** An array of RGB bytes corresponding to the DPI stages.

### C. Macro Management

Macros use Big Endian for IDs and Sizes.

**1. Check Existing Macros (`GetExistMacroInfo`)**

* **Packet:** `[4]=0x06`, `[5]=0x04`, `[6]=0x81`
* **Loop:** Send this packet for IDs 1 through 30.
* **Payload Sent:** `[7]=ID_High`, `[8]=ID_Low`
* **Response:** If Byte [1] == `0xA1`, the macro exists. Size is in Bytes [9-12].

**2. Delete Macro**

* **Packet:** `[4]=0x02`, `[5]=0x04`, `[6]=0x02`
* **Payload:** `[7]=ID_High`, `[8]=ID_Low`

---

## 5. Return Codes & Retry Logic

The device status is returned in **Byte [1]** of the response packet (assuming Byte [0] is Report ID).

| Value | Meaning | Action Required |
| --- | --- | --- |
| **161** (`0xA1`) | **Success** | Command Successful. |
| **> 161** | **Busy** | Device is busy. Wait 30ms and retry the command. |
| **< 161** | **Corrupt** | Buffer error. Send 3 blank **GET** requests to clear buffer, then retry command. |
| **0 / 255** | **Timeout** | Device disconnected or hardware timeout. |

---

## 6. Python Implementation Example

This script implements the corrected "Busy" vs "Corrupt" retry logic.

```python
import hid
import time

def send_command(device: hid.device, packet: bytes, target=0x02) -> tuple[bool, bytes]:
    # 1. Send the Feature Report
    # Ensure packet is 65 bytes padded
    padded_packet = packet + bytes(65 - len(packet))
    device.send_feature_report(padded_packet)
    
    # 2. Wait 30ms (Critical)
    time.sleep(0.03)
    
    # 3. Read Response
    # Request 65 bytes from the Target Device ID
    response = device.get_feature_report(target, 65)
    
    # HIDAPI includes Report ID at index 0, so real data starts at 1
    # We check byte [1] for the status code 0xA1 (161)
    status_code = response[1]
    
    if status_code == 0xA1:
        return True, response

    # --- RETRY LOGIC ---
    
    # Case A: Device is Busy (> 0xA1)
    # Keep trying to SEND the command again
    if status_code > 0xA1:
        print("Device Busy, retrying...")
        for _ in range(5):
            device.send_feature_report(padded_packet)
            time.sleep(0.03)
            response = device.get_feature_report(target, 65)
            if response[1] == 0xA1:
                return True, response

    # Case B: Transmission Corrupt (< 0xA1)
    # Clear buffer with GET requests, then SEND again
    if status_code < 0xA1:
        print("Packet Corrupt, clearing buffer...")
        # Clear buffer loop
        for _ in range(3):
            time.sleep(0.03)
            # Just read, don't write
            device.get_feature_report(target, 65) 
            
        # Retry the Write
        device.send_feature_report(padded_packet)
        time.sleep(0.03)
        response = device.get_feature_report(target, 65)
        
        if response[1] == 0xA1:
            return True, response

    return False, response

# --- USAGE EXAMPLES ---

def set_polling_rate(device: hid.device, hz: int) -> bool:
    # Map Hz to Protocol Value
    hz_map = {
        1000: 1, 500: 2, 250: 4, 125: 8, 1000: 16,
        2000: 32, 4000: 64, 8000: 128
    }
    
    # Structure: [3]=Target, [4]=Cat, [5]=Comp, [6]=Cmd, [7]=Val
    packet = bytearray(65)
    packet[3] = 0x02 # Mouse
    packet[4] = 0x01 # Perf Cat
    packet[5] = 0x01 # Perf Comp
    packet[6] = 0x00 # Set Polling
    packet[7] = hz_map[hz] # Byte Map
    
    success, resp = send_command(device, packet)
    print(f"Set Polling Rate {hz}Hz: {success}")

    return success


def set_angle_snap(device: hid.device, enable: bool) -> bool:
    packet = bytearray(65)
    packet[3] = 0x02
    packet[4] = 0x01 # Perf Cat
    packet[5] = 0x01 # Perf Comp
    packet[6] = 0x04 # Set Angle Snap (Note: 0x04 is reused in other Cats)
    packet[7] = enable
    
    success, resp = send_command(device, packet)
    print(f"Set Angle Snap {enable}: {success}")

    return success

```