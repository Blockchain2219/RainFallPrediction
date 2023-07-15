import serial
import csv
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Google Drive API credentials
credentials = service_account.Credentials.from_service_account_file('C:/Users/rahul/Downloads/iotproject-392011-04e27b781790.json')
drive_service = build('drive', 'v3', credentials=credentials)

# Establish serial connection
ser = serial.Serial('COM3', 9600)

# Create a CSV file
csv_file_path = 'C:/Users/rahul/OneDrive/Documents/ML.csv'
csv_file = open(csv_file_path, 'a', newline='')  # Open in append mode
csv_writer = csv.writer(csv_file)

# Google Drive file details
file_id = '1P5fgSlUe8hi-CBGSfTqWpz3CakuB-PRH'  # ID of the existing file on Google Drive

try:
    # Check if the file is empty
    file_empty = os.stat(csv_file_path).st_size == 0

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('latin-1').rstrip()
            data = line.split(',')
            if len(data) == 3:
                temperature = float(data[0])
                humidity = float(data[1])

                # Append data to CSV file
                if file_empty:
                    csv_writer.writerow(["Temperature", "Humidity"])  # Add header row
                    file_empty = False

                csv_writer.writerow([temperature, humidity])
                csv_file.flush()

                # Update CSV file on Google Drive
                media_body = os.path.join(os.getcwd(), csv_file_path)
                drive_service.files().update(
                    fileId=file_id,
                    media_body=media_body
                ).execute()

except KeyboardInterrupt:
    pass

finally:
    # Close the serial connection and CSV file
    ser.close()
    csv_file.close()
