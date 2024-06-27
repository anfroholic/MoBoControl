from machine import Pin, SoftI2C
import utime
import mcp23017

i2c = SoftI2C(scl=Pin(27), sda=Pin(26), freq=100000)
print(i2c.scan()) # scan for devices
led = Pin(2, Pin.OUT)

mcp = mcp23017.MCP23017(i2c)
time_between_frames = 5

# hardware pins
reset_pin = 7
pwr_pin = 6
jumper_pins = {
    "JPG1": (8, 9),
    "JBR1": (10, 11),
    "JPB1": (12, 13),
    "JPME1": (15, 14),
    "JPME2": (5, 4),
    "JI2C1": (3, 2),
    "JI2C2": (1, 0),
}

def pulse_reset():
    print('pulsing reset')
    mcp[reset_pin].value(1)
    utime.sleep(5)
    mcp[reset_pin].value(0)
    print('reset pulsed')

def pulse_power():
    print('pulsing power')  
    mcp[pwr_pin].value(1)
    utime.sleep(1)
    mcp[pwr_pin].value(0)
    print('power pulsed')  

class Jumper:
    def __init__(self, mcp, pin_0, pin_1):
        self.mcp = mcp
        self.pin_0 = pin_0  # 1 -> 2
        self.pin_1 = pin_1  # 2 -> 3
        self.value = None
        self.setup()
        
    def setup(self):
        """init the device pins"""
        self.mcp.pin(self.pin_0, mode=0, value=0)
        utime.sleep_ms(time_between_frames)
        self.mcp.pin(self.pin_1, mode=0, value=0)
        utime.sleep_ms(time_between_frames)
        
    def on(self):
        """jumps jumper 2->3 """
        self.mcp[self.pin_0].value(0)
        utime.sleep_ms(time_between_frames)
        self.mcp[self.pin_1].value(1)
        self.value = 1
        utime.sleep_ms(time_between_frames)
        
    def off(self):
        """jumps jumper 1->2 """
        self.mcp[self.pin_1].value(0)
        utime.sleep_ms(time_between_frames)
        self.mcp[self.pin_0].value(1)
        self.value = 0
        utime.sleep_ms(time_between_frames)
        
    def none(self):
        """desconnects all jumpers """
        self.mcp[self.pin_1].value(0)
        utime.sleep_ms(time_between_frames)
        self.mcp[self.pin_0].value(0)
        self.value = None
        utime.sleep_ms(time_between_frames)

print('mcp23017 device')
# init the power and reset pins
mcp.pin(pwr_pin, mode=0, value=0)
utime.sleep_ms(time_between_frames)
mcp.pin(reset_pin, mode=0, value=0)
utime.sleep_ms(time_between_frames)

jumpers = {name: Jumper(mcp, pin[0], pin[1]) for name, pin in jumper_pins.items()}
print('mcp23017 initted')

def list_jumper_values():
    for k, v in jumpers.items():
        print(f"{k}: {v.value}")


def beep():
    print('posted')
    
# spkr = Pin(34, Pin.IN)
# spkr.irq(trigger=Pin.IRQ_RISING, handler=beep)

# from machine import ADC
# spkr = ADC(Pin(34))
# spkr.atten(ADC.ATTN_11DB)
# threshold = 5000

# from machine import UART
# uart = UART(1, baudrate=9600, tx=13, rx=35)
# print(f'message: {uart.read()}' if uart.any() else '0')


# while True:
#     if spkr.read_u16() > threshold:
#         print('posted')
#         utime.sleep(1)
    
#     utime.sleep(.001)


