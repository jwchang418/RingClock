import network
import ntptime
import time
import neopixel
from machine import Pin

ssid = 'ssid'
password = 'password'

ws_pin = 0
led_nums = 12
brightness = [0,1,3,5,10,20]

np = neopixel.NeoPixel(Pin(ws_pin), led_nums)


def show_clock(hour, minute, second):
    # Display red
    # calculate the ratio of the second hand
    sec_ratio = int(second % 5 )
    # calculate the ratio of the long hand
    min_ratio = int( minute % 5 )
    # calculate the ratio of the short hand
    hour_ratio = int( minute / 60 * 5)
    
    second_hand = int( second / 5 )
    long_hand = int( minute / 5 )
    short_hand = hour%12
    
    # clear the led status
    np.fill(( 0, 0, 0 ))
    
    # set the second hand status
    np[second_hand] = ( brightness[5 - sec_ratio], 0, 0 )
    if( second_hand + 1 == 12 ):
        np[0] = ( brightness[sec_ratio], 0, 0 )
    else:
        np[second_hand+1] = ( brightness[sec_ratio], 0, 0 )
    
    # set the long hand status
    np[long_hand] = ( np[long_hand][0], brightness[5 - min_ratio], 0 )
    if( long_hand + 1 == 12 ):
        np[0] = ( np[0][0], brightness[min_ratio], 0 )
    else:
        np[long_hand+1] = ( np[long_hand+1][0], brightness[min_ratio], 0 )
    
    # set the short hand status
    np[short_hand] = ( np[short_hand][0], np[short_hand][1], brightness[5 - hour_ratio] )
    if( short_hand + 1 == 12 ):
        np[0] = ( np[0][0], np[short_hand][1], brightness[hour_ratio] )
    else:
        np[short_hand+1] = ( np[short_hand+1][0], np[short_hand+1][1], brightness[hour_ratio] )
    np.write()


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# wait for wifi connection
while not wlan.isconnected():
    time.sleep(1)

# get the NTP time
try:
    ntptime.settime()
except Exception as e:
    print("Failed to synchronize time:", e)
    
# disconnect the WiFi
wlan.disconnect()

# refresh the led status for every 1 second
while True:
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(time.mktime(time.localtime())+28800)
    show_clock(hour,minute,second)
    time.sleep(1)
