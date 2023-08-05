import sys


rules = [
    ('luftdaten_testdrive', 'ldi_v2'),
    ('earth_43_sensors', 'ldi_readings'),
    ('location_name', 'station_id'),
    ('$Location$', '$ldi_station_id'),
    ('$Location', '$ldi_station_name'),
]

def replace(payload):
    for rule in rules:
        payload = payload.replace(rule[0], rule[1])
    return payload


def run():
    payload = sys.stdin.read()
    payload = replace(payload)
    print(payload)


if __name__ == '__main__':
    run()
