import machine

import clock
import siliconcraft_display

uart = machine.UART(0, baudrate=38400, tx=machine.Pin(16))
display = siliconcraft_display.Display(uart, 255)
rtc = machine.RTC()

my_clock = clock.Display(display)
old_time = (0, 0, 0, 0, 0, 0, 0, 0)
current_time = old_time

style: int = clock.Style.blink1
my_clock.set_transition_style(style)
num_effects = 8
cycle_effects = True

try:
    while True:
        while current_time == old_time:
            machine.idle()
            current_time = rtc.datetime()
        old_time = current_time
        (year, month, day, weekday, hour, minute, second, subsecond) = current_time
        time_string = f'{hour:02}{minute:02}{second:02}'
        my_clock.show_time(time_string)
        if cycle_effects:
            if second % 10 == 0:
                style = (style % num_effects) + 1
                print(f'Switching to effect style {style}')
                my_clock.set_transition_style(style)
except KeyboardInterrupt:
    display.clear()
    print('Program stopped by user')
