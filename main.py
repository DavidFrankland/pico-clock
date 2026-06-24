import time
import machine

import clock
import siliconcraft_display
from siliconcraft_display import Segments, digits, Letters
import network_utils
import time_utils
import settings

uart = machine.UART(0, baudrate=38400, tx=machine.Pin(16))
display = siliconcraft_display.Display(uart, 255)

if settings.display_startup_animation:
    print('startup banner')
    startup_message_bytes = [Letters.p, Letters.i, Letters.c, Letters.o, 0,
                             Letters.c, Letters.l, Letters.o, Letters.c, Letters.k]
    display.scroll_bytes(startup_message_bytes)
    time.sleep(1)

network_helper = network_utils.NetworkHelper(display)
network_helper.connect()
if settings.display_ip_address:
    ip_address = network_helper.ip_address
    ip_address_bytes = []
    for char in ip_address:
        if char == '.':
            ip_address_bytes.append(Segments.p)
        else:
            ip_address_bytes.append(digits[int(char)])
    display.scroll_bytes(ip_address_bytes)
network_helper.sync_time()

my_clock = clock.Display(display)
old_time = 0
current_time = old_time
my_clock.transition_style = settings.transition_style
num_transitions = 8

try:
    while True:
        while current_time == old_time:
            machine.idle()
            current_time = time.time()
        old_time = current_time
        year, month, day, hour, minute, second, weekday, yearday = time_utils.localtime()
        time_string = f'{hour:02}{minute:02}{second:02}'
        my_clock.show_time(time_string)
        if hour == 4 and minute == 0 and second == 0:
            network_helper.sync_time()
        if settings.cycle_transitions:
            if second % 10 == 0:
                my_clock.transition_style = (my_clock.transition_style + 1) % num_transitions
                print(f'switching to effect style {my_clock.transition_style}')
except KeyboardInterrupt:
    display.clear()
    print('program stopped by user')
