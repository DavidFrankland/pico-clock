import time
import random

import siliconcraft_display
from siliconcraft_display import Segments, digits

# all the digit segments in a list for shuffling
digit_segments = [Segments.a, Segments.b, Segments.c, Segments.d, Segments.e, Segments.f, Segments.g]


class Style():
    instant = 1
    glitch = 2
    blank = 3
    cycle = 4
    wipe_down = 5
    dissolve = 6
    blink1 = 7
    blink2 = 8


def set_decimal_points(bytes: list[int]):
    clear_decimal_points(bytes)
    bytes[1] |= 0b00001000
    bytes[3] |= 0b00001000


def clear_decimal_points(bytes: list[int]):
    for i in range(0, 6):
        bytes[i] &= 0b11110111


def shuffle_digit_segments():
    n = len(digit_segments)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        digit_segments[i], digit_segments[j] = digit_segments[j], digit_segments[i]


class Display:
    """
    Displays the time on the LED display, with various transition styles.
    """

    def __init__(self, siliconcraft_display: siliconcraft_display.Display, style=Style.instant):
        self.display = siliconcraft_display
        self.prev_display_bytes = [0] * 6
        self.display_bytes = [0] * 6
        self.style = style

    def set_transition_style(self, style: int):
        self.style = style

    def show_time(self, time_string: str):
        for i in range(0, 6):
            self.display_bytes[i] = digits[int(time_string[i])]

        if self.style == Style.instant:
            self._instant_transition()
        elif self.style == Style.glitch:
            self._glitch_transition()
        elif self.style == Style.blank:
            self._blank_transition()
        elif self.style == Style.cycle:
            self._cycle_transition()
        elif self.style == Style.wipe_down:
            self._wipe_down_transition()
        elif self.style == Style.dissolve:
            self._dissolve_transition()
        elif self.style == Style.blink1:
            self._blink1_transition()
        elif self.style == Style.blink2:
            self._blink2_transition()
        else:
            raise ValueError(f'Unknown transition style: {self.style}')

        clear_decimal_points(self.display_bytes)
        self.prev_display_bytes = self.display_bytes.copy()

    def _instant_transition(self):
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)
        time.sleep(0.5)
        clear_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _glitch_transition(self):
        temp_bytes = self.display_bytes.copy()
        animation_duration = 0.4
        steps = 6
        delay = animation_duration / steps
        num_lit_segments = 3
        for step in range(0, steps):
            for digit in range(0, 6):
                if self.display_bytes[digit] != self.prev_display_bytes[digit]:
                    shuffle_digit_segments()
                    b = 0
                    for segment in range(0, num_lit_segments):
                        b |= digit_segments[(segment)]
                    temp_bytes[digit] = b
            clear_decimal_points(temp_bytes)
            self.display.write_bytes(temp_bytes)
            time.sleep(delay)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _blank_transition(self):
        temp_bytes = self.display_bytes.copy()
        for i in range(0, 6):
            if self.display_bytes[i] != self.prev_display_bytes[i]:
                temp_bytes[i] = 0
        clear_decimal_points(temp_bytes)
        self.display.write_bytes(temp_bytes)
        time.sleep(0.25)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _cycle_transition(self):
        patterns = [Segments.b, Segments.c, Segments.d, Segments.e, Segments.f, Segments.a]
        temp_bytes = self.display_bytes.copy()
        animation_duration = 0.4
        steps = len(patterns)
        delay = animation_duration / steps
        for pattern in patterns:
            for i in range(0, 6):
                if self.display_bytes[i] != self.prev_display_bytes[i]:
                    temp_bytes[i] = pattern
            clear_decimal_points(temp_bytes)
            self.display.write_bytes(temp_bytes)
            time.sleep(delay)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _wipe_down_transition(self):
        patterns = [Segments.a, Segments.g, Segments.d]
        temp_bytes = self.display_bytes.copy()
        animation_duration = 0.25
        steps = len(patterns)
        delay = animation_duration / steps
        for pattern in patterns:
            for i in range(0, 6):
                if self.display_bytes[i] != self.prev_display_bytes[i]:
                    temp_bytes[i] = pattern
            clear_decimal_points(temp_bytes)
            self.display.write_bytes(temp_bytes)
            time.sleep(delay)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _dissolve_transition(self):
        shuffle_digit_segments()
        temp_bytes = self.prev_display_bytes.copy()
        animation_duration = 0.3
        steps = len(digit_segments)
        delay = animation_duration / steps
        for segment in digit_segments:
            inv_pattern = segment ^ 0b11111111
            for i in range(0, 6):
                if self.display_bytes[i] != self.prev_display_bytes[i]:
                    temp_bytes[i] = temp_bytes[i] & inv_pattern | (self.display_bytes[i] & segment)
            clear_decimal_points(temp_bytes)
            self.display.write_bytes(temp_bytes)
            time.sleep(delay)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)

    def _blink1_transition(self):
        self._blink_transition(display_segment_g=False)

    def _blink2_transition(self):
        self._blink_transition(display_segment_g=True)

    def _blink_transition(self, display_segment_g: bool):
        temp_bytes = self.display_bytes.copy()
        old_segment_masks = [Segments.b | Segments.c | Segments.e | Segments.f | Segments.g, Segments.g, 0, 0]
        new_segment_masks = [0, 0, Segments.g, Segments.b | Segments.c | Segments.e | Segments.f | Segments.g]
        animation_duration = 0.3
        delay = animation_duration / len(old_segment_masks)
        for i in range(0, len(old_segment_masks)):
            for digit in range(0, 6):
                if self.display_bytes[digit] != self.prev_display_bytes[digit]:
                    d = self.prev_display_bytes[digit] & old_segment_masks[i]
                    d |= self.display_bytes[digit] & new_segment_masks[i]
                    if display_segment_g:
                        d |= Segments.g
                    temp_bytes[digit] = d
            clear_decimal_points(temp_bytes)
            self.display.write_bytes(temp_bytes)
            time.sleep(delay)
        set_decimal_points(self.display_bytes)
        self.display.write_bytes(self.display_bytes)
