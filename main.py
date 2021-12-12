#!/usr/bin/python3
from bme280 import bme280


def main():
    bme = bme280.BME280(i2c_address=0x77, i2c_port=1)
    print(f'Chip id: {hex(bme.chip_id())}')


if __name__ == '__main__':
    main()
