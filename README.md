# OpenMouseControls

OpenMouseControls is project aimed at allowing users to use Attackshark extra mouse features on all operating systems instead of windows only.
This project involves reverse-engineered protocols. Use at your own risk. I am not responsible for any damage caused to your hardware.

---

![Alt UIScreenshot](https://raw.githubusercontent.com/TadhgOCo/OpenMouseControls/refs/heads/main/assets/UIScreenshot.jpg)

> [!CAUTION]
> | Model(s)           | Support Level | Notes                                  |
> |--------------------|---------------|----------------------------------------|
> | R6 / R11 Ultra     | 🟢 Supported  | Tested on R6 (Dongle Mode)             |
> | X6 / X8 / X11      | 🟢 Supported  | Should work out of the box             |
> | R1 / R5 Ultra      | 🟡 Limited    | GUI may not display correctly          |
> | X6 / G / A         | 🟡 Limited    | GUI may not display correctly          |
> | V3 / V6            | 🟡 Limited    | CLI workaround required (Profile -1)   |

**Check CLI Usage below for more details**
---
### Core Functionality:
- Read Battery levels & Charging Status
- Read Dongle + Mouse Firmware Version & Check for compatibility
- Modification of the following features:
    - DPI
    - Motion Sync
    - Ripple Control
    - Angle Snap
    - Dongle LED
    - Polling Rate
    - Lift-Off Distance
    - Debounce Time
    - Sleep Timer

---
### Known Issues & Limitations:
We are tracking a few bugs as we head toward a stable v1.0.0.

- **Sync Latency:** When clicking the Sync button, the application may appear to "freeze" for a few seconds (1-2 on Windows, 3-5 on Linux) before the syncing process begins. The app remains functional and will resume normally once the sync ends. A fix for this UI thread blocking is planned for the next update.

- **No Profile Switching:** This feature is planned for the next update.
- **No Button Reassignment:** This feature is also planned although it is secondary.
- **No Macro Creation:** This Feature is not currently planned.
- **No Bluetooth Connectivity:** This Feature is not currently planned.
---


## Getting Started:


### Prerequisites
* Python 3.x _(If building from source)_
* Windows: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (May be required for hidapi)

### Installation & Run:

### 1. Installation via git (Build From Source)
1. Clone the repo:
    * Clone the repo with git: `sh git clone https://github.com/TadhgOCo/OpenMouseControls`
    * Run : `cd OpenMouseControls`

2. Install packages:
    * pip : `pip install -r requirements.txt`
    * pip : `pip install pyinstaller`
    * Bash - Linux ONLY : `bash script.sh "$(pwd)"`

>[!Tip]
> You may start the app here to ensure no errors: `python app.py`

3. Build the Project:
    * Run: `pyinstaller app.spec`
    * Run: `cd dist`

**Windows: All in one Place**
```
git clone https://github.com/TadhgOCo/OpenMouseControls
cd OpenMouseControls

pip install -r requirements.txt
pip install pyinstaller

pyinstaller app.spec

cd dist
OpenMouseControl-Windows
```

**Linux : All in one Place**
```
git clone https://github.com/TadhgOCo/OpenMouseControls
cd OpenMouseControls

pip install -r requirements.txt
pip install pyinstaller

bash script.sh "$(pwd)"
pyinstaller app.spec

cd dist
./OpenMouseControl-Linux
```
Finally to start the app once installed:
* **Windows** : `OpenMouseControl`
* **Linux** : `./OpenMouseControl`

### 2. Installation via Releases Tab
> [!NOTE]
> **Windows Users:**
> - You may need [Microsoft C++ build tools 2015 or higher](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed
>
> **Linux Users:**
> - You may need to run `install.sh` with super user privileges (`sudo`) to allow the mouse and program to communicate properly.
> - Also ensure you run `chmod +x OpenMouseControl-Linux` before running the app **OR** set as excutable in the files app UI.

1. Download the latest version for you Operating System from the [Releases tab](https://github.com/TadhgOCo/OpenMouseControls)
2. Extract the archive

To start the app from the command line once installed:
* **Windows** : `OpenMouseControl`
* **Linux** : `./OpenMouseControl`

### 3. Installation of the Command-line Tool
```
git clone https://github.com/TadhgOCo/OpenMouseControls

cd OpenMouseControls
cd cli
```
#### Usage:
`python cli.py [Command] --value [Value] --profile [ID]`

* `Command` The command you want set _(Do -h for the list)_
* `--Value`, `-V` The value you want to change _(If assigning)_
* `--profile`, `-p` The ProfileID you want to change _(1 by default)_. Set to -1 if your mouse is not on the supported list and doesn't work with the UI
* `-h` Help options, provides a list of the commands you can use above
* `-v` Print the version number and exit

### Tech Stack:
* Language: Python
* Hardware Interface: Cython-hidapi
* GUI Framework: CustomTkinter

### License
* Distributed under the MIT License. See LICENSE for more information.
