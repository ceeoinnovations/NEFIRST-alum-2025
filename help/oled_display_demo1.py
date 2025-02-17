from machine import Pin, I2C
import ssd1306

# Specify the I2C id as 1, and appropriate pins for SDA and SCL on I2C1
# Use GPIO 26 for SDA, GPIO 27 for SCL, based on the Extra port.
i2c = I2C(1, scl=Pin(27), sda=Pin(26))
#address 0x3c

# Initialize the display with the I2C interface object
display = ssd1306.SSD1306_I2C(128, 32, i2c) 

# Display a message
display.text('Hello, World!', 0, 0, 1)
display.show()

# Print a message to confirm the program execution
print("OLED display should now show 'Hello, World!'")
