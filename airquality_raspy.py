# Monitoring AIR Quality with Raspberry, Adafruit and SDS sensor https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/
import serial, time
import aqi
from Adafruit_IO import Client
aio = Client(ADAFRUIT_USER, ADAFRUIT_PW)

ser = serial.Serial('/dev/ttyUSB0')

while True:
        data = []
        for index in range(0,10):
                datum = ser.read()
                data.append(datum)

        pmtofive = int.from_bytes(b''.join(data[2:4]), byteorder='little')/10
        pmtofive_aqi = str(aqi.to_iaqi(aqi.POLLUTANT_PM25, pmtofive, algo=aqi.ALGO_EPA))
        #print('PM 2.5: ', pmtofive)
        #print('PM 2.5 AQI', pmtofive_aqi)
        aio.send('air25', pmtofive)
        aio.send('air25-aqi',pmtofive_aqi)
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little')/10
        pmten_aqi = str(aqi.to_iaqi(aqi.POLLUTANT_PM10, pmten, algo=aqi.ALGO_EPA))
        #print('PM 10 AQI: ', pmten_aqi)
        aio.send('air10', pmten)
        aio.send('air10-aqi',pmten_aqi)
        #print('PM 10: ', pmten)
