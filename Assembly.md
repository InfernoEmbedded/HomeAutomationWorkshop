# Assembly instructions for 1Wire Control Board (Hat)

## Tools
- Reflow Oven or Hot Air Rework station
- Fine tip soldering iron
- Fine tip tweezers
- Fresh solder paste
- Solder squeegee
- Solder mask stencil
- Multimeter

## Instructions
- Bring up the DC/DC power supply with a 24V input and confirm the output is 5V. If you are using an adjustable supply, fix the trimmer with threadlock after setting.
- Align the stencil with your board, it will help if you fabricate alignment holes.
- Squeegee the solder paste across your stencil.
- Place the surface mount components onto the board. The direction of the text on the board should match the direction of the text on the components.
- Reflow the board using the oven or reflow station.
- Inspect the the joints and rework if necessary. Pay careful attention to the RJ45 pins, looking for shorts.
- Solder the DC jack and DS18B20.
- Using a pair of female pin headers to stabilise the pins, insert the 1x10 & 2x10 male pin headers in the GPIO holes to form a 3x10 header, and solder them.
- Insert the 2x20 female pin headers onto the underside of the board and solder them.
- (optional) insert the 2x3 I2C pin headers for expansion boards and solder them.

## Testing
- With the hat disconnected from the Orange Pi, connected 24V to the DC jack and confirm the output is 5V
- Connect the hat to an Orange Pi Prime and confirm the board boots when powered through the hat
- Ensure i2c-0 is enabled in devicetree/bootloader `ls /dev/i2c-0`, if not, configure i2c-0 and reboot. For Armbian, add `overlays=i2c0` to  `/boot/armbianEnv.txt` and reboot.
- Confirm the DS2482-100 is detected `i2cdetect -y 0` should show a device at address 0x18.
- In a new terminal, run `owserver --debug --i2c=/dev/i2c-0:18`
- In a new terminal, run `owdir /uncached`. This should list the DS18B20 temperature sensor. If not, check the owserver output for hints as to what the problem is.
Some fake DS18B20 devices give checksum errors (don't ask how I found this out).
- Connect a known good external 1Wire device, `owdir /uncached` should list both the temperature sensor and external device. If not, confirm the external device is receiving
signal and power.
- ```
echo 6 >/sys/class/gpio/export
echo in > /sys/class/gpio6/direction
cat /sys/class/gpio6/value # should read 1 by default, 0 when button is pressed
```
