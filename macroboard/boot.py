from storage import disable_usb_drive
from digitalio import DigitalInOut
from adafruit_matrixkeypad import Matrix_Keypad
from board import C1,C2,C3,C4,R1,R2,R3,R4

keys = ((1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (4, 8, 12, 16))
cols = [DigitalInOut(x) for x in (C1, C2, C3, C4)]
rows = [DigitalInOut(x) for x in (R1, R2, R3, R4)]

keypad = Matrix_Keypad(cols, rows, keys)
keys = keypad.pressed_keys

if not keys:
    disable_usb_drive()