# pico-clock

A Raspberry Pi Pico clock which displays the time on a a [Silicon Craft](https://www.siliconcraft.net/) SC6Dlite LED display.

Various transitions are available which make the display more interesting.

The choice of components was based more on what was at hand, rather than personal choice. The LED display was found in our local Maker Space - [Otley MAKER SPACE](https://otleymakerspace.co.uk/) - and nobody seemed to want it, so it was put to use.

## Requirements

### Hardware

- Raspberry Pi Pico (1 or 2), with wifi or without<br>
- Silicon Craft SC6Dlite LED display
- breadboard, wires

### Software

- Visual Studio Code with MicroPico extension installed
- MicroPython installed on the Pi Pico

I followed this guide to get started: [Programming Raspberry Pi Pico with VS Code and MicroPython](https://randomnerdtutorials.com/raspberry-pi-pico-vs-code-micropython/)

## Connection

The LED display is capable of receiving serial data over a standard 5V TTL interface. This makes interfacing with the Pi Pico very easy, just 3 wires are needed:

| Pi Pico  | LED display |
| -------- | ----------- |
| GND      | GND         |
| VBUS     | 5VDC        |
| UART0 TX | TTL receive |

The Pi Pico has 2 UARTs available. I used UART0 on pin 21, as it is located on the corner of the PCB and was most convenient.

If you use a different UART or pin, you'll need to modify the line of code in [main.py](main.py) that initialises the UART. Here we specify 0 for the UART ID, and GPIO pin 16 (which is actually pin 21 on the PCB). Consult the [Raspberry Pi Pico Pinout](https://pico.pinout.xyz/) for details.

```Python
uart = machine.UART(0, baudrate=38400, tx=machine.Pin(16))
```

## How to

- Wire it up
- Upload [clock.py](clock.py) and [siliconcraft_display.py](siliconcraft_display.py) to the Pi Pico
- Sync RTC
- run [main.py](main.py)

## To do

- improve "How to" instructions
- add FreeCAD 3D file for breadboard stand
- wifi version (NTP, web interface)
- add photos and videos
