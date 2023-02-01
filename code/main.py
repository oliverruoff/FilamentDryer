import time
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from DHT22 import DHT22

# Configure manually how much degree should be targeted in degree celcius
TARGET_TEMP = 45
# Configure manually how long a filament should be dried
HEAT_TIMER_MINUTES = 360

# LCD configs
I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Temp. sensor configs
dht22=DHT22(Pin(15,Pin.IN,Pin.PULL_UP))#sensor connected GPIO 15 pin

# Relay to control the heat
RELAY = Pin(13, Pin.OUT)

# Helper used for adding spaces in front of a str
def rjust(context, length):
    return ' ' * max(0, length - len(context)) + context 
    

def update_display(target_temp, current_temp, current_humid, start_humid, minutes_passed):
    #lcd.clear()
    # If you want that time sticks to 0 once time is up:
    #if minutes_passed > HEAT_TIMER_MINUTES:
    #    minutes_passed = HEAT_TIMER_MINUTES
    lcd.move_to(0,0)
    lcd.putstr("T:" + str(int(current_temp)) + "/" + str(target_temp) + "C")
    lcd.move_to(10,0)
    lcd.putstr(" M:" + rjust(str(HEAT_TIMER_MINUTES - int(minutes_passed)), 3))
    lcd.move_to(0,1)
    lcd.putstr("H:" + rjust(str(int(current_humid)),2) + "%")
    lcd.move_to(11,1)
    lcd.putstr("P:" + rjust(str(int(start_humid-current_humid)),2) + "%")
    
def activate_relay(relay):
    relay.value(1)

def deactivate_relay(relay):
    relay.value(0)

T, start_humid = dht22.read()
start_time = time.time()
while True:
    time.sleep(0.5)
    T, H = dht22.read()
    minutes_passed = (time.time() - start_time) / 60
    update_display(target_temp=TARGET_TEMP, current_temp=T, current_humid=H, start_humid=start_humid, minutes_passed=minutes_passed)
    # Check if relay and therefore heating needs to be activated
    if T < TARGET_TEMP and minutes_passed < HEAT_TIMER_MINUTES:
        activate_relay(RELAY)
    else:
        deactivate_relay(RELAY)
        


