import time
import digitalio
import board
import adafruit_matrixkeypad
from gpiozero import LED


def blink_led(time_in_seconds, led):
    """
    Blink the led for an amount of time
    """
    led.on()
    time.sleep(time_in_seconds)
    led.off()
    time.sleep(time_in_seconds)


def get_pressed_key(keys, led):
    """
    If there are more than 1 keys pressed, then return nothing... and blink the led 3 times
    else return the key and blink 1 time
    """
    if keys is None or len(keys) > 1:
        blink_led(0.1, led)
        blink_led(0.1, led)
        blink_led(0.1, led)
        return None

    result = None
    if keys:
        result = str(keys[0])
        blink_led(0.1, led)
        print(result)

    return result


def check_code(code, door, led):
    """
    Checks if the current code is equal to the predefined code
    """
    if len(code) > 4:
        door.off()
        print("To many numbers entered, reset code")
        blink_led(0.1, led)
        blink_led(0.1, led)
        blink_led(0.1, led)
    elif code == "3266":
        print("The right code was entered")
        print("The door is unlocking")
        door.on()
        led.on()
        return True

    return False


def main():
    """
    Main starting application
    """
    # Membrane 3x4 matrix keypad on Raspberry Pi -
    # https://www.adafruit.com/product/419
    cols = [digitalio.DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
    rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]

    # 3x4 matrix keypad on Raspberry Pi -
    # rows and columns are mixed up for https://www.adafruit.com/product/3845
    # cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
    # rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]

    keys = (("#", 0, "*"), (9, 8, 7), (6, 5, 4), (3, 2, 1))

    keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
    led = LED(17)
    door = LED(4)

    code = ""

    while True:
        keys = keypad.pressed_keys
        key_pressed = get_pressed_key(keys, led)

        if key_pressed is None:
            continue

        if key_pressed == "*":
            code = ""
            door.off()
            led.off()
        else:
            code = code + key_pressed

        if check_code(code, door, led):
            time.sleep(10)
            door.off()
            led.off()

        print("code: {}".format(code))

        time.sleep(0.1)


main()

