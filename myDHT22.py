import gspread
import time
import board
import adafruit_dht
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import matplotlib.pyplot as plt

# Define the scope of the API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load the API credentials from the JSON file
credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/bpalmer/just-json-things/client_secret_932936657185-jls6cch87tosejphtdcee125od6sl9u7.apps.googleusercontent.com", scope)

# Authorize the API credentials
gc = gspread.authorize(credentials)

# Open the Google Sheet by name
sheet = gc.open("DHT22 Sheet").sheet1

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D18)

print("Started")

#Add a header row
header = ["Current Date", "Current Time", "Temperature C", "Temperature F", "Humidity"]
sheet.append_row(header)

while True:
    try:
        # Take the sensor readings
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        # Get the current date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")

        # Write the sensor readings and date/time to the sheet
        row = [current_date, current_time, temperature_c, temperature_f, humidity]
        sheet.append_row(row)

        # Get the temperature and humidity data from the sheet
        temp_values = sheet.col_values(3)[1:]
        humid_values = sheet.col_values(5)[1:]

        # Convert the temperature values from strings to floats
        temp_values = [float(x) for x in temp_values]

        # Convert the humidity values from strings to floats
        humid_values = [float(x) for x in humid_values]

        # Create a new figure and plot the temperature and humidity data
        fig, ax = plt.subplots()
        ax.plot(temp_values, label='Temperature (C)')
        ax.plot(humid_values, label='Humidity')
        ax.legend()

        # Set the x-axis label
        ax.set_xlabel('Time')

        # Set the y-axis labels
        ax.set_ylabel('Temperature (C) / Humidity')

        # Set the title of the graph
        ax.set_title('Temperature and Humidity Data')

        # Display the graph
        plt.show()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    # Wait for one minute
    time.sleep(60)
