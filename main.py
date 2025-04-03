from machine import Pin, I2C, PWM
from time import sleep

# --- LCD Setup (I2C) ---
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

def lcd_init():
    lcd_write(0x03)
    lcd_write(0x03)
    lcd_write(0x03)
    lcd_write(0x02)
    lcd_write(0x28)
    lcd_write(0x0C)
    lcd_write(0x06)
    lcd_write(0x01)

def lcd_write(cmd, mode=0):
    buf = bytearray(2)
    buf[0] = (cmd & 0xF0) | 0x04 | mode
    buf[1] = (cmd & 0xF0) | mode
    i2c.writeto(0x27, buf)
    buf[0] = ((cmd << 4) & 0xF0) | 0x04 | mode
    buf[1] = ((cmd << 4) & 0xF0) | mode
    i2c.writeto(0x27, buf)

def lcd_string(message, line):
    lcd_write(line)
    for char in message:
        lcd_write(ord(char), 1)

# --- RGB LED Setup (PWM) ---
# Define RGB LED pins (adjust if needed)
RED_PIN = 15   # GP15 (Pin 20)
GREEN_PIN = 14  # GP14 (Pin 19)
BLUE_PIN = 13   # GP13 (Pin 17)

# Initialize PWM for each color channel
red = PWM(Pin(RED_PIN))
green = PWM(Pin(GREEN_PIN))
blue = PWM(Pin(BLUE_PIN))

# Set PWM frequency (1000Hz is a good default)
red.freq(1000)
green.freq(1000)
blue.freq(1000)

def set_rgb(r, g, b):
    # Scale 0-255 to 0-65535 (Pico PWM range)
    red.duty_u16(r * 257)    # 257 ≈ 65535/255
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)

def blink_rgb(color, delay=0.5):
    set_rgb(*color)  # Turn ON with given color
    sleep(delay)
    set_rgb(0, 0, 0)  # Turn OFF (all channels 0)
    sleep(delay)

# Predefined colors (R, G, B)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# --- Initialize LCD ---
lcd_init()
lcd_string("Stop Sleeping!", 0x80)  # Line 1
lcd_string("Wake Up Now!", 0xC0)   # Line 2

# --- Main Loop (RGB Blinking) ---
while True:
    blink_rgb(RED)
    blink_rgb(GREEN)
    blink_rgb(BLUE)
    blink_rgb(PURPLE)
    blink_rgb(YELLOW)
