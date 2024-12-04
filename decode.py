import argparse
import csv
import json
import struct
from datetime import datetime

from dateutil.relativedelta import relativedelta


wind_lookup = {
    0: 'N',
    1: 'NNE',
    2: 'NE',
    3: 'ENE',
    4: 'E',
    5: 'ESE',
    6: 'SE',
    7: 'SSE',
    8: 'S',
    9: 'SSW',
    10: 'SW',
    11: 'WSW',
    12: 'W',
    13: 'WNW',
    14: 'NW',
    15: 'NNW',
}

ordered_fields = {
90: [
        {
            'name': 'firmware_revision',
            'slice': (0, 2),
        },
        {
            'name': 'battery_level',
            'slice': (2, 4),
        },
        {
            'name': 'percent_iss_packets_received_per_period',
            'slice': (4, 6),
        },
        {
            'name': 'percent_soil_moisture_packets_received_per_period',
            'slice': (6, 8),
        },
        {
            'name': 'sd_card_available_size_100s_mb',
            'slice': (8, 10),
        },
        {
            'name': 'avg_rx_rssi',
            'slice': (10, 12),
        },
        {
            'name': 'avg_rx_snr',
            'slice': (12, 14),
        },
        {
            'name': 'rx_crc_error_counter',
            'slice': (14, 16),
        },
        {
            'name': 'ack_tries',
            'slice': (16, 18),
        },
        {
            'name': 'davis_rssi_threshold',
            'slice': (18, 20),
        },
    ],
    110: [
        {
            'name': 'sequence_number',
            'slice': (0, 4)
        },
{
            'name': 'avg_temperature',
            'slice': (4, 8)
        },
        {
            'name': 'high_temp',
            'slice': (8, 10),
        },
        {
            'name': 'low_temp',
            'slice': (10, 12),
        },
        {
            'name': 'rainfall',
            'slice': (12, 16),
        },
        {
            'name': 'rain_rate',
            'slice': (16, 20),
        },
        {
            'name': 'humidity',
            'slice': (20, 22)
        },
    ],
    111: [
        {
            'name': 'sequence_number',
            'slice': (0, 4)
        },
        {
            'name': 'barometer',
            'slice': (4, 8),
        },
        {
            'name': 'solar_radiation',
            'slice': (8, 12),
        },
        {
            'name': 'solar_radiation_high',
            'slice': (12, 16),
        },
        {
            'name': 'avg_wind_speed',
            'slice': (16, 18),
        },
        {
            'name': 'high_wind_speed',
            'slice': (18, 20),
        },
        {
            'name': 'wind_dir',
            'slice': (20, 22),
        },
    ],
    112: [
        {
            'name': 'sequence_number',
            'slice': (0, 4)
        },
        {
            'name': 'soil_temp_1',
            'slice': (4, 6),
        },
        {
            'name': 'soil_temp_2',
            'slice': (6, 8),
        },
        {
            'name': 'soil_temp_3',
            'slice': (8, 10),
        },
        {
            'name': 'soil_temp_4',
            'slice': (10, 12),
        },
        {
            'name': 'soil_moist_1',
            'slice': (12, 14),
        },
        {
            'name': 'soil_moist_2',
            'slice': (14, 16),
        },
        {
            'name': 'soil_moist_3',
            'slice': (16, 18),
        },
        {
            'name': 'soil_moist_4',
            'slice': (18, 20),
        },
        {
            'name': 'leaf_wetness_1',
            'slice': (20, 22),
        },
    ],
    100: [
        {
            'name': 'sequence_number',
            'slice': (0, 4)
        },
        {
            'name': 'avg_temperature',
            'slice': (4, 8)
        },
        {
            'name': 'high_temp',
            'slice': (8, 10),
        },
        {
            'name': 'low_temp',
            'slice': (10, 12),
        },
        {
            'name': 'rainfall',
            'slice': (12, 16),
        },
        {
            'name': 'rain_rate',
            'slice': (16, 20),
        },
        {
            'name': 'humidity',
            'slice': (20, 22)
        },
        {
            'name': 'barometer',
            'slice': (22, 26),
        },
        {
            'name': 'solar_radiation',
            'slice': (26, 30),
        },
        {
            'name': 'solar_radiation_high',
            'slice': (30, 34),
        },
        {
            'name': 'avg_wind_speed',
            'slice': (34, 36),
        },
        {
            'name': 'high_wind_speed',
            'slice': (36, 38),
        },
        {
            'name': 'wind_dir',
            'slice': (38, 40),
        },
        {
            'name': 'soil_temp_1',
            'slice': (40, 42),
        },
        {
            'name': 'soil_temp_2',
            'slice': (42, 44),
        },
        {
            'name': 'soil_temp_3',
            'slice': (44, 46),
        },
        {
            'name': 'soil_temp_4',
            'slice': (46, 48),
        },
        {
            'name': 'soil_moist_1',
            'slice': (48, 50),
        },
        {
            'name': 'soil_moist_2',
            'slice': (50, 52),
        },
        {
            'name': 'soil_moist_3',
            'slice': (52, 54),
        },
        {
            'name': 'soil_moist_4',
            'slice': (54, 56),
        },
        {
            'name': 'leaf_wetness_1',
            'slice': (56, 58),
        },

    ],
# Moteino board packet
    113: [
        {
            'name': 'sequence_number',
            'slice': (0, 4)
        },
        {
            'name': 'moteino_data',
            'slice': (4, 22),
        },
    ],
    # The next four are the same, but without the sequence number at the start.
170: [
        {
            'name': 'avg_temperature',
            'slice': (0, 4)
        },
        {
            'name': 'high_temp',
            'slice': (4, 6),
        },
        {
            'name': 'low_temp',
            'slice': (6, 8),
        },
        {
            'name': 'rainfall',
            'slice': (8, 12),
        },
        {
            'name': 'rain_rate',
            'slice': (12, 16),
        },
        {
            'name': 'humidity',
            'slice': (16, 18)
        },
        {
            'name': 'barometer',
            'slice': (18, 22),
        },
        {
            'name': 'solar_radiation',
            'slice': (22, 26),
        },
        {
            'name': 'solar_radiation_high',
            'slice': (26, 30),
        },
        {
            'name': 'avg_wind_speed',
            'slice': (30, 32),
        },
        {
            'name': 'high_wind_speed',
            'slice': (32, 34),
        },
        {
            'name': 'wind_dir',
            'slice': (34, 36),
        },
        {
            'name': 'soil_temp_1',
            'slice': (36, 38),
        },
        {
            'name': 'soil_temp_2',
            'slice': (38, 40),
        },
        {
            'name': 'soil_temp_3',
            'slice': (40, 42),
        },
        {
            'name': 'soil_temp_4',
            'slice': (42, 44),
        },
        {
            'name': 'soil_moist_1',
            'slice': (44, 46),
        },
        {
            'name': 'soil_moist_2',
            'slice': (46, 48),
        },
        {
            'name': 'soil_moist_3',
            'slice': (48, 50),
        },
        {
            'name': 'soil_moist_4',
            'slice': (50, 52),
        },
        {
            'name': 'leaf_wetness_1',
            'slice': (52, 54),
        },
    ],
180: [
        {
            'name': 'avg_temperature',
            'slice': (0, 4)
        },
        {
            'name': 'high_temp',
            'slice': (4, 6),
        },
        {
            'name': 'low_temp',
            'slice': (6, 8),
        },
        {
            'name': 'rainfall',
            'slice': (8, 12),
        },
        {
            'name': 'rain_rate',
            'slice': (12, 16),
        },
        {
            'name': 'humidity',
            'slice': (16, 18)
        },
    ],
    181: [
        {
            'name': 'barometer',
            'slice': (0, 4),
        },
        {
            'name': 'solar_radiation',
            'slice': (4, 8),
        },
        {
            'name': 'solar_radiation_high',
            'slice': (8, 12),
        },
        {
            'name': 'avg_wind_speed',
            'slice': (12, 14),
        },
        {
            'name': 'high_wind_speed',
            'slice': (14, 16),
        },
        {
            'name': 'wind_dir',
            'slice': (16, 18),
        },
    ],
    182: [
        {
            'name': 'soil_temp_1',
            'slice': (0, 2),
        },
        {
            'name': 'soil_temp_2',
            'slice': (2, 4),
        },
        {
            'name': 'soil_temp_3',
            'slice': (4, 6),
        },
        {
            'name': 'soil_temp_4',
            'slice': (6, 8),
        },
        {
            'name': 'soil_moist_1',
            'slice': (8, 10),
        },
        {
            'name': 'soil_moist_2',
            'slice': (10, 12),
        },
        {
            'name': 'soil_moist_3',
            'slice': (12, 14),
        },
        {
            'name': 'soil_moist_4',
            'slice': (14, 16),
        },
        {
            'name': 'leaf_wetness_1',
            'slice': (16, 18),
        },
    ],
}


moteino_sensors = {
    1: {
        'name': 'RG-15 Rain Gauge',
        'data_size_bytes': 2,
        'struct_format': '!H'
    },
    2: {
        'name': 'Dual PMS5003 / Humidity',
        'data_size_bytes': 4,
        'struct_format': '!H'
    },
}



def decode_whinwan_bytes(port_num: int, data_bytes: str, time_interval=15, transmit_time=None):

    out = {}

    formats = {
        90: '!BBBBBBBBBb',
        100: '!HhBBHHBHHHBBBBBBBBBBBB',
        110: '!HhBBHHB',
        111: '!HHHHBBB',
        112: '!HBBBBBBBBB',
        113: '!HHBBBBBBB',

        170: '!hBBHHBHHHBBBBBBBBBBBB',
        180: '!hBBHHB',
        181: '!HHHBBB',
        182: '!BBBBBBBBB',
    }

    record = struct.unpack(formats[port_num], bytes.fromhex(data_bytes))

    moteino_config = None

    for i, field in enumerate(ordered_fields[port_num]):
        data = {
            'hex': data_bytes[field['slice'][0]:field['slice'][1]],
            'raw_value': record[i],
            'interpreted': None,
        }
        field_name = field['name']

        raw_val = record[i]
        interp = raw_val
        interp_val = raw_val

        if field_name == 'avg_temperature':
            if raw_val == -129:
                interp_val = None
                interp = '--'
            else:
                interp_val = f'{raw_val / 10.0:.1f}'
                interp = f'{interp_val} deg F'
        elif field_name == 'high_temp':
            if raw_val == 255:
                interp_val = None
                interp = '--'
            else:
                delta = raw_val / 10.0
                interp_val = f'{(record[i-1] / 10.0 + delta):.1f}'
                interp = f"+{delta} deg F => {interp_val} deg F"
        elif field_name == 'low_temp':
            if raw_val == 255:
                interp_val = None
                interp = '--'
            else:
                delta = raw_val / 10.0
                interp_val = f'{record[i-2] / 10.0 - delta:.1f}'
                interp = f"-{delta} deg F => {interp_val} deg F"
        elif field_name == 'sequence_number':
            # use the timestamp the gateway received the packet to determine the interval.
            if transmit_time:
                # Just find the most recent interval
                aligned_minute = transmit_time.minute - (transmit_time.minute % time_interval)
                val = datetime(year=transmit_time.year, month=transmit_time.month, day=transmit_time.day,
                               hour=transmit_time.hour, minute=aligned_minute, second=0)
            else:
                now = datetime.utcnow()
                current_month_start = datetime(year=now.year, month=now.month, day=1, hour=0, minute=0, second=0)
                delta = relativedelta(minutes=time_interval * raw_val)
                val = (current_month_start + delta)

            interp_val = interp = val.strftime('%Y-%m-%dT%H:%M:00Z')

        elif field_name == 'rainfall':
            if raw_val == 2**16-1:
                interp_val = None
                interp = '--'
            else:
                interp_val = raw_val
                interp = f'{raw_val / 100.0:.2f}" Rain'

        elif field_name == 'humidity':
            if raw_val == 255:
                interp_val = None
                interp = '--'
            else:
                interp_val = raw_val
                interp = f"{interp_val}%"

        elif field_name == 'rain_rate':
            if raw_val == 2**16-1:
                interp_val = None
                interp = '--'
            else:
                interp_val = raw_val
                interp = f"{raw_val / 100.0:.2f} inches/hr"

        elif field_name == 'barometer':
            interp_val = f"{raw_val / 1000.0:.3f}"
            interp = f"{interp_val} in. hg"
        elif field_name == 'wind_dir':
            prevailing_mask = 240 # 0xF0
            gust_mask = 15 # 0x0F
            gust_val = raw_val & gust_mask
            prevailing_val = (raw_val & prevailing_mask) >> 4
            gust = wind_lookup[gust_val]
            prevailing = wind_lookup[prevailing_val]
            interp = f"prevailing dir: {prevailing}; gust_dir: {gust}"
            out['prevailing_wind_dir'] = {'interp_val': prevailing}
            out['gust_wind_dir'] = {'interp_val': gust}

        elif field_name in ['avg_wind_speed', 'high_wind_speed']:
            interp = f"{raw_val} MPH"
        elif field_name in ['soil_temp_1', 'soil_temp_2', 'soil_temp_3', 'soil_temp_4']:
            if raw_val == 255:
                interp_val = None
                interp = '--'
            else:
                interp_val = raw_val - 90
                interp = f'{interp_val} deg F'
        elif field_name in ['soil_moist_1', 'soil_moist_2', 'soil_moist_3', 'soil_moist_4']:
            if raw_val == 255:
                interp_val = None
                interp = '--'
            else:
                interp = f'{raw_val}cb'

        elif field_name in ['solar_radiation', 'solar_radiation_high']:
            if raw_val == (2**16)-1:
                interp = '--'
                interp_val = None
            else:
                interp = f'{raw_val} W/m^2'

        # Moteino board
        elif field_name == 'moteino_data':
            # moteino_config = raw_val
            moteino_bytes = bytes.fromhex(data['hex'])

            # For now, should be 0 always. Future devices might be multi-packet.
            moteino_packet_type = (moteino_bytes[0] & 0xf0) >> 4
            davis_id = ((moteino_bytes[0] & 0x07))
            error_bit = ((moteino_bytes[1] & 0x80) >> 7)
            moteino_sensor_number = ((moteino_bytes[1] & 0x7c) >> 2)

            sensor = moteino_sensors.get(moteino_sensor_number)

            interp_val = {'davis_id': davis_id,
                          'error_bit': error_bit,
                          'moteino_sensor_number': moteino_sensor_number,
                          'sensor': sensor.get('name') if sensor else 'Unknown',
                          'sensor_data': decode_moteino_sensor(moteino_sensor_number, sensor, moteino_bytes)
                          }
            moteino_config = interp_val
            interp = json.dumps(interp_val)
        #elif field_name == 'moteino_data_bytes' and moteino_config is not None:
            sensor = moteino_config['sensor']
            if sensor:
                #data_part_hex = data_bytes[8:]
                #sensor_data_hex = data_part_hex[:(2 * sensor['data_size_bytes'])]
                #raw_val = struct.unpack(sensor['struct_format'], bytes.fromhex(sensor_data_hex))

                #interp_val = interp
                interp = raw_val

        elif field_name == "firmware_revision":
            major_rev = raw_val >> 6
            minor_rev = raw_val & int("3F", 16)
            interp_val = {'major': major_rev, 'minor': minor_rev}
            interp = f"{major_rev}.{minor_rev}"
        elif field_name == "battery_level":
            val = raw_val / 10.0
            interp_val = val
            interp = f"{interp_val} V"

        data['interpreted'] = interp
        data['interp_val'] = interp_val
        out[field['name']] = data

    return out


def print_decoded_whinwhan_bytes(writer, bytes: str, port_number: int, time_interval: int):

    writer.writerow([
        'Field',
        'Hex',
        'Value',
        'Interpreted',
    ])

    out_data = decode_whinwan_bytes(port_number, bytes, time_interval)

    out_table = []
    for field in ordered_fields[port_number]:
        field_output = out_data.get(field['name'])
        if field_output:
            field_hex = field_output['hex']
            field_val = field_output['raw_value']
            interp = field_output['interpreted']
        else:
            field_hex = ''
            field_val = ''
            interp = ''

        out_table.append([field['name'], field_hex, field_val, interp])

    writer.writerows(out_table)


def decode_moteino_sensor(moteino_sensor_number, sensor, moteino_bytes):
    if moteino_sensor_number == 1:
        # Rain sensor - discontinued ...
        return {}
    elif moteino_sensor_number == 2:
        # 0-100%
        humidity = ((moteino_bytes[2] & 0xf8) >> 3) + ((moteino_bytes[1] & 0x03) << 5)
        # PM1.0: %d ug/m3
        pm1p0 = ((moteino_bytes[3] & 0xfc) >> 2) + ((moteino_bytes[2] & 0x07) << 6)
        # PM2.5: %d ug/m3
        pm2p5 = ((moteino_bytes[4] & 0xfe) >> 1) + ((moteino_bytes[3] & 0x03) << 7)
        # PM10.0: %d ug/m3
        pm10p0 = ((moteino_bytes[5] & 0xff)) + ((moteino_bytes[4] & 0x01) << 8)
        return {
            'humidity': humidity,
            'pm1p0': pm1p0,
            'pm2p5': pm2p5,
            'pm10p0': pm10p0,
        }
    else:
        return {}



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Decodes WHINWAN data and writes CSV to file.")
    parser.add_argument("--out", help="output file path")
    parser.add_argument("--input_bytes", help="Input string")
    parser.add_argument("--time_interval", help="Recording interval in minutes, default 15", default=15)

    parser.add_argument("--port_number", type=int,
                        help="LORA port number: 100 (combined), 110 (Temp/Hum/Rain), 111 (Pressure/Wind/Solar), 112 (SM/ST/LW)", default=100)

    args = parser.parse_args()
    with open(args.out, 'w+') as f:
        w = csv.writer(f)

        print_decoded_whinwhan_bytes(w, args.input_bytes, port_number=int(args.port_number), time_interval=int(args.time_interval))
