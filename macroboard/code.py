from neopixel import NeoPixel
from supervisor import runtime
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

neopixels = NeoPixel(NEOPIXEL, 4, brightness=1.0, auto_write=False)
keypad = Matrix_Keypad(cols, rows, keys)

neopixels.fill([0,0,255])
neopixels.show()

while True:

    # Serial Communication

    if runtime.serial_bytes_available:
        data = input().strip()
        if data.startswith("0"):
            print(data)

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