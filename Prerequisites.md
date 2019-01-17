Home Automation Workshop Prerequisites
======================================

Most of the work you will be doing will be on the home automation server,
which is an Orange Pi running Home Assistant's HassOS distribution. However,
you will need to be able to build firmware for your remote 1-Wire device
if you wish to make changes to that device (such as supporting new device
types).

These instructions assume an x86-64 based Linux machine.

stlink
------

We need to install an open source version of the STMicroelectronics Stlink
Tools. stlink is the name of the hardware programmer we are going to use to
flash new firmware onto our 1-Wire boards.

On Fedora do this:

```sudo dnf install stlink```

For Ubuntu users, you need to be running at least Ubuntu Cosmic (18.10) for
the stlink tools to be packaged.

```sudo apt-get install stlink-tools```

For other distributions you're a little more on your own. Build the STlink
utilites from here: https://github.com/texane/stlink

MBED CLI
--------

Arm Mbed CLI is the name of the Arm Mbed command-line tool. Mbed CLI enables
Git- and Mercurial-based version control, dependencies management,
code publishing, support for remotely hosted repositories (GitHub, GitLab and
mbed.org), use of the Arm Mbed OS build system and export functions and other
operations.

We will install mbed with pip, but first we should ensure that we have a
recent version of pip. Examples here are for Ubuntu:

```
sudo apt-get install python       # We need python! Every computer does!
sudo apt-get install python-pip   # Install a basic pip
sudo pip install -U pip           # Upgrade it to the lastest version
sudo apt-get remove python-pip    # Remove the outdated system pip
sudo pip install mbed-cli         # Install the mbed-cli
```

If you get an error from that final pip command line like this:

```
sudo pip install mbed-cli
bash: /usr/bin/pip: No such file or directory
```

I had this issue because /usr/local/bin isn't in the default path for new
Ubuntu installs. You can fix this by doing this thing:

```
echo "export PATH=\$PATH:/usr/local/bin" >> ~/.bashrc
bash # i.e. start a new shell
```

And now re-run the failed pip command.

Fetch git module and submodules
-------------------------------

Fetch this git module onto your dev machine if you haven't already:

```
sudo apt-get install git
git clone https://github.com/InfernoEmbedded/HomeAutomationWorkshop
```

This git repo has submodules. You need to fetch those as well:

```
cd HomeAutomationWorkshop
git submodule update --init --recursive
```

Fetch ARM GCC Toolchain
-----------------------

Now let's setup the GCC toolchain for the ARM chips.

```
cd onewire-softdevice/toolchain
./build-arm.sh
```

Tell MBed where to find the source
----------------------------------

```
mkdir -p ~/.mbed
echo "MBED_OS_DIR=$(pwd)/../mbed-os" > ~/.mbed/.mbed
```

Install mbed python requirements
--------------------------------

mbed wont use a virtualenv (it's horrible, I know), so we have to pip install
into the system python a bunch of dependancies:

```
cd ../mbed-os
sudo pip install -r requirements.txt
```

Confirm you can build the firmware
----------------------------------

Now it's time to try a compile.

```
cd ../devices/16_Channel_SSR_Driver/src/
./build.sh
```

If you see errors about missing python dependancies or something like this:

```
[mbed] Working path "/home/mikal/HomeAutomationWorkshop/onewire-softdevice/devices/16_Channel_SSR_Driver/src" (library)
[mbed] Program path "/home/mikal/HomeAutomationWorkshop/onewire-softdevice/devices/16_Channel_SSR_Driver/src"
[mbed] Auto-installing missing Python modules (colorama, pyserial, prettytable, jinja2, intelhex, junit_xml, pyyaml, urllib3, requests, mbed_ls, mbed_host_tests, mbed_greentea, beautifulsoup4, fuzzywuzzy, pyelftools, jsonschema, future, manifest_tool, mbed_cloud_sdk, icetea)...
[mbed] WARNING: Unable to auto-install required Python modules.
       The mbed OS tools in this program require the following Python modules: colorama, pyserial, prettytable, jinja2, intelhex, junit_xml, pyyaml, urllib3, requests, mbed_ls, mbed_host_tests, mbed_greentea, beautifulsoup4, fuzzywuzzy, pyelftools, jsonschema, future, manifest_tool, mbed_cloud_sdk, icetea
       You can install all missing modules by running "pip install -r requirements.txt" in "/home/mikal/HomeAutomationWorkshop/onewire-softdevice/mbed-os"
       On Posix systems (Linux, etc) you might have to switch to superuser account or use "sudo"
---
Traceback (most recent call last):
  File "/home/mikal/HomeAutomationWorkshop/onewire-softdevice/mbed-os/tools/make.py", line 22, in <module>
    from builtins import str
ImportError: No module named builtins
[mbed] ERROR: "/usr/bin/python" returned error.
       Code: 1
       Path: "/home/mikal/HomeAutomationWorkshop/onewire-softdevice/devices/16_Channel_SSR_Driver/src"
       Command: "/usr/bin/python -u /home/mikal/HomeAutomationWorkshop/onewire-softdevice/mbed-os/tools/make.py -t GCC_ARM -m INFERNOEMBEDDED_SOFTDEVICE --profile ./release.json --source . --source ../../../mbed-os --source ../../../libs/OneWireSlave --build ./BUILD/INFERNOEMBEDDED_SOFTDEVICE/GCC_ARM-RELEASE --artifact-name 16ChannelSSR --color"
       Tip: You could retry the last command with "-v" flag for verbose output
---
```

Then you probably failed to install the python dependancies into the system
python. Try that bit again. A successful build will end with soemthing like:

```
Link: 16ChannelSSR
Elf2Bin: 16ChannelSSR
| Module                           |         .text |     .data |        .bss |
|----------------------------------|---------------|-----------|-------------|
| ../..                            | 15952(+15952) | 420(+420) | 2930(+2930) |
| BUILD/INFERNOEMBEDDED_SOFTDEVICE |     478(+478) |     0(+0) |       0(+0) |
| [fill]                           |       45(+45) |     0(+0) |     21(+21) |
| [lib]/c_nano.a                   |   6798(+6798) | 100(+100) |     21(+21) |
| [lib]/gcc.a                      |   3048(+3048) |     0(+0) |       0(+0) |
| [lib]/misc                       |     220(+220) |     8(+8) |     28(+28) |
| Subtotals                        | 26541(+26541) | 528(+528) | 3000(+3000) |
Total Static RAM memory (data + bss): 3528(+3528) bytes
Total Flash memory (text + data): 27069(+27069) bytes

Image: ./BUILD/INFERNOEMBEDDED_SOFTDEVICE/GCC_ARM-RELEASE/16ChannelSSR.bin
```
