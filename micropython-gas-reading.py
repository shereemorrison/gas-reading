import urequests
from time import sleep_ms
import time
from machine import Pin, SPI
from mfrc522 import MFRC522
import json
import network

TIMEOUT_DURATION = 2 * 60

SSID = "addyournetwork"
PASSWORD = "addyourpassword"

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object in station mode
    wlan.active(True)  # Activate the WLAN interface
    wlan.connect(SSID, PASSWORD)  # Connect to WiFi network

    # Wait for connection
    print("Connecting to WiFi...")
    timeout = 30  # Set a timeout period (in seconds)
    start_time = time.time()

    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print("WiFi connection timeout.")
            return False  # Timeout after 30 seconds
        time.sleep(1)  # Wait for a successful connection
        print("Still connecting...")

    print("Connected to WiFi")
    print("IP Address:", wlan.ifconfig()[0])  # Print the assigned IP address
    return True

# Try connecting to WiFi
if connect_wifi():
    print("Wi-Fi connection successful!")
else:
    print("Failed to connect to Wi-Fi.")

# SPI setup for MFRC522
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(1, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

# Supabase REST API URL and headers for authentication
SUPABASE_URL = "https://pywpljuuoecmoshimynl.supabase.co/rest/v1/Members"
HEADERS = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5d3BsanV1b2VjbW9zaGlteW5sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE0NTI4NDAsImV4cCI6MjA0NzAyODg0MH0.kA_26qqxNGc4DUkeXALn2BnhCqcxbJbIyTAV_jvQzzU",  # Replace with your Supabase public key
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5d3BsanV1b2VjbW9zaGlteW5sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMTQ1Mjg0MCwiZXhwIjoyMDQ3MDI4ODQwfQ.at_ASBciIWnPeboysqrDRk3lw1zyILHX3rz8PsbrAew",  # Replace with your actual Supabase access token
}

try:
    response = urequests.get("http://httpbin.org/get")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Error during connection test: {e}")


def reset_reader():
    sda.value(0)  # Assert chip select (low)
    sleep_ms(100)
    sda.value(1)  # Deassert chip select (high)

# Function to check if card number exists in Supabase Members table
def check_card_number(cardnumber_str, url, headers):
    query = f"?cardnumber=eq.{cardnumber_str}"
    full_url = f"{url}{query}"

    try:
        response = urequests.get(full_url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if 200 <= response.status_code < 300:
            try:
                # Manually parse the JSON from the response text
                response_data = json.loads(response.text)

                if isinstance(response_data, list) and len(response_data) > 0:
                    user = response_data[0]
                    print(f"User found: {user['name']}")
                    return True
                else:
                    print(f"Card number {cardnumber_str} not found.")
                    return False
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                return False
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")
            return False
    except OSError as e:
        print(f"Network-related error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return False
    finally:
        if response:
            response.close()

# Function to update user status in Supabase
def update_user_status(cardnumber_str, logged_in, url, headers):
    # Construct the update URL and payload
    query = f"?cardnumber=eq.{cardnumber_str}"
    full_url = f"{url}{query}"  # URL to update the user row
    data = {
        "logged_in": logged_in  # Update the logged_in field to True or False
    }

    print("Full URL:", full_url)  # Log the full URL to check if it's correct

    try:
        response = urequests.patch(full_url, json=data, headers=headers)  # PATCH request to update user status
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        if 200 <= response.status_code < 300:
            print(f"User {cardnumber_str} status updated to {logged_in}")
        else:
            print(f"Failed to update user status. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error occurred while updating user status: {e}")


# Function to process RFID scan and update user status
def process_rfid_scan(cardnumber_str):
    # After reading the card number, update the user's logged-in status
    update_user_status(cardnumber_str, True, SUPABASE_URL, HEADERS)

# Function to read and check RFID cards
def do_read():
    try:
        reset_reader()
        sleep_ms(500)
        rdr = MFRC522(spi, sda)

        while True:
            print("Waiting for a card...")
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                print("Card detected, checking UID...")
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    print("Card UID:", uid)
                    # Pass UID to check card number and process login
                    if check_card_number(uid, SUPABASE_URL, HEADERS):
                        print(f"User with UID {uid} logged in.")
                        process_rfid_scan(uid)  # Update the user login status
                    else:
                        print(f"Card {uid} not found in the database.")
                else:
                    print("Collision or read error")
            sleep_ms(500)
    except Exception as e:
        print("An error occurred:", e)
    except KeyboardInterrupt:
        print("Exiting...")

# Start reading cards
do_read()
