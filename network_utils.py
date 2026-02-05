import machine
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
            self.display.clear()
            spinner_segments = [0b00100000, 0b01000000, 0b00000010, 0b00000100]
            spinner_index = 0
            while not wlan.isconnected():
                if time.time() - start_time > timeout:
                    print()
                    print(f'connection to {found_ssid} timed out')
                    break
                print(end='.')
                self.display.write_bytes([0, 0, 0, 0, 0, spinner_segments[spinner_index]])
                spinner_index = (spinner_index + 1) % len(spinner_segments)
                machine.idle()
                time.sleep(0.1)
            print()
            self.display.clear()
            if wlan.isconnected():
                break
        if wlan.isconnected():
            print(f'connected to {found_ssid}')
        else:
            print('could not connect to any known network')

    @property
    def connected(self):
        return self.wlan.isconnected()

    def sync_time(self):
        if not self.connected:
            self.connect()
        try:
            ntptime.settime()
            print('time synchronized with NTP server')
        except Exception as e:
            print(f'failed to synchronize time: {e}')
