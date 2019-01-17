# Home Automation Workshop Prerequisites
Most of the work you will be doing will be on the home automation server, but you will need to be able to build firmware
for your remote 1Wire devices if you wish to make changes.

These instructions assume an x86-64 based Linux machine.

## 1Wire Firmware
- Install stlink
Fedora
```dnf install stlink```
Ubuntu Cosmic
```apt install stlink-tools```

Others:
Build the STlink utilites from here:
https://github.com/texane/stlink

- Install MBED CLI
Follow the instructions here to install MBED CLI:
https://github.com/ARMmbed/mbed-cli

- Fetch git submodules
This git repo has submodules. If you haven't fetched them already, do so now:
```
 git submodule update --init --recursive
```

- Fetch ARM GCC Toolchain
```
cd onewire-softdevice/toolchain
./build-arm.sh
```

- Tell MBed where to find the source
```
mkdir -p ~/.mbed
echo "MBED_OS_DIR=/path/to/onewire-softdevice/mbed-os" > ~/.mbed/.mbed
```

- Confirm you can build the firmware
```
cd onewire-softdevice/devices/16_Channel_SSR_Driver/src/
./build.sh
```

