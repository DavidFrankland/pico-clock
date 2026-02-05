import network
import time
import ntptime

import siliconcraft_display
import wifi_credentials


class NetworkHelper:

    def __init__(self, display: siliconcraft_display.Display):
        network.hostname('pico-clock')
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.display = display

    def connect(self):
        wlan = self.wlan
        print('scanning for networks: ', end='')
        s = 0b11100011
        c = 0b00100110
        a = 0b01110111
        n = 0b01100100
        self.display.write_bytes([s, c, a, n, 0, 0])
        time.sleep(0.1)
        networks = wlan.scan()
        print(f'found {len(networks)} networks')
        for network in networks:
            found_ssid = network[0].decode()
            print(f'{found_ssid}: ', end='')
            have_credential = False
            for credential in wifi_credentials.credentials:
                known_ssid, known_password = credential
                if found_ssid == known_ssid:
                    have_credential = True
                    break
            if not have_credential:
                print('not known')
                continue
            print('trying to connect', end='')
            wlan.connect(known_ssid, known_password)
            timeout = 10
            start_time = time.time()
            spinner_segments = [0b00100000, 0b01000000, 0b00000010, 0b00000100]
            spinner_index = 0
            while not wlan.isconnected():
                if time.time() - start_time > timeout:
                    print()
                    print(f'connection to {found_ssid} timed out')
                    break
                print(end='.')
                n = 0b01100100
                e = 0b10110111
                t = 0b10100110
                self.display.write_bytes([n, e, t, 0, 0, spinner_segments[spinner_index]])
                spinner_index = (spinner_index + 1) % len(spinner_segments)
                time.sleep(0.1)
            print()
            self.display.clear()
            time.sleep(0.1)
            if wlan.isconnected():
                break
        if wlan.isconnected():
            print(f'connected to {found_ssid}')
        else:
            print('could not connect to any known network')
            segment_g = 0b00100000
            self.display.write_bytes([segment_g, segment_g, segment_g, segment_g, segment_g, segment_g])
            time.sleep(0.1)

    @property
    def connected(self):
        return self.wlan.isconnected()

    def sync_time(self):
        if not self.connected:
            self.connect()
        print('syncing time')
        n = 0b01100100
        t = 0b10100110
        p = 0b10110101
        self.display.write_bytes([n, t, p, 0, 0, 0])
        time.sleep(0.1)
        ok = False
        while not ok:
            try:
                ntptime.settime()
                print('time synchronized with NTP server')
                ok = True
            except Exception as e:
                print(f'failed to synchronize time: {e}')
        self.display.clear()
        time.sleep(0.1)
