from machine import UART

#  ───a───
# │       │
# f       b
# │       │
#  ───g───
# │       │
# e       c
# │       │
#  ───d───  p


class Segments:
    """
    Single segment bitmaps.
    """
    #     fcgb.eda
    a = 0b00000001
    b = 0b00010000
    c = 0b01000000
    d = 0b00000010
    e = 0b00000100
    f = 0b10000000
    g = 0b00100000
    p = 0b00001000


class Letters:
    """
    Bitmaps for some letters that can be reasonably represented on a 7 segment display.
    """
    #     fcgb.eda
    a = 0b01110111
    c = 0b00100110
    e = 0b10110111
    i = 0b00000100
    l = 0b10000100
    k = 0b11100101
    n = 0b01100100
    o = 0b01100110
    p = 0b10110101
    s = 0b11100011
    t = 0b10100110
    P = 0b10110101
    I = 0b10000100
    C = 0b10000111
    O = 0b11010111
    L = 0b10000110
    K = 0b11100101

# segment bitmaps for the 0-9 digits
digits = [
    # fcgb.eda
    0b11010111,  # 0
    0b01010000,  # 1
    0b00110111,  # 2
    0b01110011,  # 3
    0b11110000,  # 4
    0b11100011,  # 5
    0b11100111,  # 6
    0b01010001,  # 7
    0b11110111,  # 8
    0b11110011,  # 9
]


class Display:
    """
    Represents a Silicon Craft SC6Dlite LED display.
    """

    def __init__(self, uart: UART,  id: int):
        self.uart = uart
        self.id = id

    def write_bytes(self, display_bytes: list[int]):
        """
        Send the individual digit segment data to the display.
        """
        self.uart.write(bytes([self.id]))
        self.uart.write(bytes('a', 'utf-8'))
        self.uart.write(bytes(display_bytes))

    def clear(self):
        """
        Blank the display.
        """
        self.write_bytes([0, 0, 0, 0, 0, 0])

    def toggle_brightness(self):
        """
        Switch between low/high brightness.
        The display powers on at full brightness.
        """
        self.uart.write(bytes([self.id]))
        self.uart.write(bytes('n', 'utf-8'))

    def set_protocol(self, new_baud_rate: int, new_id: int):
        """
        Set the display baud rate and ID.
        Settings are stored in the non volatile memory and remain unchanged until next setting.
        Display shows “ SEt” when programming is done.
        You need to reset the display by turning off then on for the changes to take effect.
        """
        b = 0
        if new_baud_rate == 9600:
            b = 36
        if new_baud_rate == 19200:
            b = 18
        if new_baud_rate == 38400:
            b = 9
        if b != 0:
            raw_bytes = [0x1e, 0x1e, b, new_id]
            self.uart.write(bytes(raw_bytes))
            exit()
