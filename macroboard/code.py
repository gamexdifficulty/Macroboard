from neopixel import NeoPixel
from supervisor import runtime
from rainbowio import colorwheel
from digitalio import DigitalInOut
from adafruit_matrixkeypad import Matrix_Keypad
from board import C1,C2,C3,C4,R1,R2,R3,R4,NEOPIXEL

keys = ((1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (4, 8, 12, 16))
cols = [DigitalInOut(x) for x in (C1, C2, C3, C4)]
rows = [DigitalInOut(x) for x in (R1, R2, R3, R4)]
keymap = [[False,False,False,False],
          [False,False,False,False],
          [False,False,False,False],
          [False,False,False,False]]

led_mode = 2
led_speed = 0.1
led_brightness = 1.0
led_breath_state = 0
led_rainbow_index = 0.0

neopixels = NeoPixel(NEOPIXEL, 4, brightness=1.0, auto_write=False)
keypad = Matrix_Keypad(cols, rows, keys)

neopixels.fill([0,0,255])
neopixels.show()

while True:

    # -------------------- Serial Communication --------------------

    if runtime.serial_bytes_available:
        data = input().strip()
        if data.startswith("0"):
            data = data[0:]

            # Change Led

            if data[0] == "0":  
                if data[1] == "0":      # Led mode
                    led_mode = int(data[2])
                elif data[1] == "1":    # Led brightness
                    led_brightness = float(data[2:])
                elif data[1] == "2":    # Led speed
                    led_speed = float(data[2:])
                elif data[1] == "3":    # Led color
                    leds = data[2:]
                    neopixels.fill([int(leds[0:3]),int(leds[3:6]),int(leds[6:])])

    # Keypad event handling

    keys = keypad.pressed_keys
    for y,layer in enumerate(keymap):
        for x,key in enumerate(layer):
            index = y*4+x+1
            if index in keys and keymap[y][x] == False:
                keymap[y][x] = True
                print("press: ",x,y)
            if not index in keys and keymap[y][x] == True:
                keymap[y][x] = False
                print("release: ",x,y)