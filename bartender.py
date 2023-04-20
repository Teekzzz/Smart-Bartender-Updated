#Originally created and heavily influenced from HackerShackOfficial

#Created by TWrex

# Major improvements made to the original code:
# - Updated the codebase from Python 2 to Python 3 to ensure compatibility with the latest Python features and libraries
# - Improved various aspects of the code:
#   - Replaced all print statements with print functions for Python 3 compatibility
#   - Enhanced exception handling by utilizing a 'finally' block to ensure proper GPIO cleanup
#   - Replaced 'iteritems()' with 'items()' to maintain compatibility with Python 3
#   - Addressed indentation inconsistencies to improve code readability
#   - Now returns an empty dictionary to avoid issues with missing pump configurations
#   - Added an editable OLED Title

# This code provides a full solution for a RaspberryPI-controlled bartending system.
# It sets up an OLED screen and buttons to navigate through a menu of drinks.
# Once a drink is selected, the corresponding pumps will be activated for a specific amount of time
# to create the chosen drink. The NeoPixel strip is also configured and used for lighting.
# The pump configuration is read from a JSON file and is used to control the GPIO pins of the pump.

# Made for Mitch with Love xo



# Import required libraries and modules
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys
import RPi.GPIO as GPIO
import json
import threading
import traceback

from dotstar import Adafruit_DotStar
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options

# Set up the GPIO mode for the Raspberry Pi
GPIO.setmode(GPIO.BCM)

# Define the screen dimensions for the OLED display
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Configure the left button settings
LEFT_BTN_PIN = 13
LEFT_PIN_BOUNCE = 1000

# Configure the right button settings
RIGHT_BTN_PIN = 5
RIGHT_BTN_BOUNCE = 2000

# Define OLED pin and general settings
OLED_RESET_PIN = 15
OLED_DC_PIN = 16

# Configure the NeoPixel strip settings
NUMBER_NEOPIXELS = 45
NEOPIXEL_DATA_PIN = 26
NEOPIXEL_CLOCK_PIN = 6
NEOPIXEL_BRIGHTNESS = 64

# Configure the flow rate settings for the pumps
setflow = 60.0 / 100.0
FLOW_RATE = setflow

# Bartender Class: Main class responsible for managing the drink-making process
class Bartender(MenuDelegate):
    def __init__(self):
        self.running = False

        # Set the OLED screen dimensions
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.btn1Pin = LEFT_BTN_PIN
        self.btn2pin = RIGHT_BTN_PIN

        # Configure the GPIO interrupts for the left and right buttons
        GPIO.setup(self.btn1Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn2Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initialize the OLED display with the required settings
        spi_bus = 0
        spi_device = 0
        gpio = gaugette.gpio.GPIO()
        spi = gaugette.spi.SPI(spi_bus, spi_device)

        # Configure the OLED display with the required pins for proper communication
        self.led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=OLED_RESET_PIN, dc_pin=OLED_DC_PIN, rows=self.screen_height, cols=self.screen_width)
        self.led.begin()
        self.led.clear_display()
        self.led.display()
        self.led.invert_display()
        time.sleep(0.5)
        self.led.normal_display()
        time.sleep(0.5)

        # Load the pump configuration from the provided JSON file
        self.pump_configuration = Bartender.readPumpConfiguration()
        for pump in self.pump_configuration.keys():
            GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)

        # Display the title on the OLED screen
        self.display_title("BAR BITCH")

        # Set up the NeoPixel strip with the specified configuratiself.pumpon
        self.numpixels = NUMBER_NEOPIXELS
        datapin = NEOPIXEL_DATA_PIN
    clockpin = NEOPIXEL_CLOCK_PIN
    self.strip = Adafruit_DotStar(self.numpixels, datapin, clockpin)
    self.strip.begin()
    self.strip.setBrightness(NEOPIXEL_BRIGHTNESS)

    # Turn off all pixels on the NeoPixel strip
    for i in range(0, self.numpixels):
        self.strip.setPixelColor(i, 0)
    self.strip.show()

    print("Initialization Complete! :)")

# Method to read the pump configuration from the JSON file
@staticmethod
def readPumpConfiguration():
    try:
        with open("pump_config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: No Pump Configuration File Found!")
        return {}  # Return an empty dictionary to avoid issues with missing pump configuration


# Method to handle menu item selection
def menu_item_selected(self, menu_item):
    if isinstance(menu_item, Back):
        return
    if menu_item.is_drink():
        self.make_drink(menu_item, drink_options[menu_item.name])

# Method to execute the drink-making process
def make_drink(self, drink, recipe):
    for ingredient, amount in recipe.items():
        pump = self.pump_for_ingredient(ingredient)
        if pump:
            self.start_pump(pump, amount)
        else:
            print(f"No pump available for ingredient: {ingredient}")

# Method to activate the pump for a specified duration
def start_pump(self, pump, amount):
    pump_time = amount / FLOW_RATE
    pump_pin = self.pump_configuration[pump]["pin"]
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(pump_time)
    GPIO.output(pump_pin, GPIO.HIGH)

# Method to find the appropriate pump for each ingredient
def pump_for_ingredient(self, ingredient):
    for pump, details in self.pump_configuration.items():
        if details["value"].lower() == ingredient.lower():
            return pump
    return None

#OLED Display Title
def display_title(self, title):
        self.led.clear_display()
        self.led.select_font(1)  # Select a larger font size
        x = (self.screen_width - self.led.text_width(title)) // 2  # Calculate the horizontal center of the text
        y = (self.screen_height - self.led.font_height()) // 2  # Calculate the vertical center of the text
        self.led.draw_text(x, y, title)
        self.led.display()

# Main method to run the Bartender application
def run(self):
    self.running = True

    # Set up the menu items and menu context
    menu_items = [MenuItem(drink["name"]) for drink in drink_list]
    main_menu = Menu(menu_items, self.led, self)
    menu_context = MenuContext(main_menu)

    # Configure button interrupts for menu navigation
    GPIO.add_event_detect(self.btn1Pin, GPIO.FALLING, callback=menu_context.advance, bouncetime=LEFT_PIN_BOUNCE)
    GPIO.add_event_detect(self.btn2Pin, GPIO.FALLING, callback=menu_context.select, bouncetime=RIGHT_BTN_BOUNCE)

    # Handle errors, logging, and clean up
    try:
        while self.running:
            menu_context.show()
            time.sleep(0.1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
    finally:
        GPIO.cleanup()

    if __name__ == "__main__":
        bartender = Bartender()
        bartender.run()