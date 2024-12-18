import pandas as pd
import tkinter as tk
import serial
import threading
import csv
import time
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from datetime import datetime

# Initialize serial port, my laptop is /dev/ttyUSB0
try:
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")


#1. Datasets featuring
df = pd.read_csv('/home/umar/Documents/Kuliah/Semester 5/Praktikum Sistem Penggerak/Ard Project 2/MLAPanelSurya/Datasets/CSV/final_data.csv')
print(df.columns)

# I think Bus Voltage, Shunt Voltage, Power, and Date Time is not really important imho
# So i decide to drop it out
df = df.drop(columns= ['Date Time', 'Bus Voltage(V)'])
print(df.head())

# Handling Shit zeroes
imputer = SimpleImputer(strategy='mean')
imputed_data = imputer.fit_transform(df)

# And then i scales the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(imputed_data)
print(scaled_data)

#2. -------------------------------------------RANDOM FOREST
iso_forest = IsolationForest(contamination=0.05, random_state=37)
iso_forest.fit(scaled_data)

def detect_anomaly(data):
  data_df = pd.DataFrame([data], columns= df.columns)  
  imputed_data = imputer.transform(data_df) # Imputed data to yeeting the f nan values lmao
  scaled_data = scaler.transform(imputed_data)
  prediction = iso_forest.predict(scaled_data)
  return prediction[0] == -1

#3. I create dict to store the sensor readings
sensor_data = {
    "Date Time": "",
    "Temperature": "N/A",
    "Humidity": "N/A",
    "Bus Voltage": "N/A",
    "Shunt Voltage": "N/A",
    "Current": "N/A",
    "Power": "N/A",
    "Load Voltage": "N/A"
}

# Function to read serial data & update the labels
def read_serial():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').rstrip() # Read signal from the port that used with ardunion
            print(f"Raw Data: {line}")  # Print command is the most Torvalds way to debug
            update_labels(line)
            


# This is the function to update the labels with new data and log updates
def update_labels(data):
    global sensor_data
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Data formatting
    sensor_data["Date Time"] = current_time
    
    if "Bus Voltage:" in data:
        bus_voltage_label.config(text=data)
        sensor_data["Bus Voltage"] = data.split(": ")[1]
    elif "Shunt Voltage:" in data:
        shunt_voltage_label.config(text=data)
        sensor_data["Shunt Voltage"] = data.split(": ")[1]
    elif "Current:" in data:
        current_label.config(text=data)
        sensor_data["Current"] = data.split(": ")[1]
    elif "Power:" in data:
        power_label.config(text=data)
        sensor_data["Power"] = data.split(": ")[1]
    elif "Load Voltage:" in data:
        load_voltage_label.config(text=data)
        sensor_data["Load Voltage"] = data.split(": ")[1]
    elif "Humidity:" in data:
        humidity_label.config(text=data)
        sensor_data["Humidity"] = data.split(": ")[1]
    elif "Temperature:" in data:
        temperature_label.config(text=data)
        sensor_data["Temperature"] = data.split(": ")[1]
    
    def safe_float(nile):
        try:
            return float(nile)
        except ValueError:
            return 0.0

    # Anomalies checker
    data_value = {
        "Temperature(oC)": safe_float(sensor_data['Temperature']),
        "Shunt Voltage(mV)": safe_float(sensor_data['Humidity']),
        "Humidity(%)": safe_float(sensor_data['Humidity']),
        "Current(mA)": safe_float(sensor_data['Current']),
        "Power(mW)": safe_float(sensor_data['Power']),
        "Load Voltge(V)": safe_float(sensor_data['Load Voltage']),

        # TEST THE ANOMALY DETECTION IF IT WORKS OR NOT
        # "Temperature(oC)": 34.2,
        # "Shunt Voltage(mV)": 62,
        # "Humidity(%)": 9.61,
        # "Current(mA)": 96.0,
        # "Power(mW)": 72,
        # "Load Voltge(V)": 0.98

        # "Temperature(oC)": 0,
        # "Shunt Voltage(mV)": 0,
        # "Humidity(%)": 0,
        # "Current(mA)": 0,
        # "Power(mW)": 0,
        # "Load Voltge(V)": 0
    }    
    is_anomaly = detect_anomaly(data_value)

    if is_anomaly:
        anomaly_label.config(text = "Anomaly Detected", fg= 'red')
        ser.write(b'1') # Send signal 1 to ardunio
    else:
        anomaly_label.config(text = "Anomaly Not Detected", fg= 'green')
        ser.write(b'0') # Send no signal to arduino

    # Add anomaly status to the sensor_data dictionary
    sensor_data["Anomaly"] = "Yes" if is_anomaly else "No"

    # Debugging is my way
    print(f"Updated Sensor Data: {sensor_data}")

#4. Export data to CSV file
def write_to_csv():
    file_exists = False
    try:
        with open('/home/umar/Documents/Kuliah/Semester 5/Praktikum Sistem Penggerak/Ard Project 2/MLAPanelSurya/datalog_new.csv', mode='r') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open('/home/umar/Documents/Kuliah/Semester 5/Praktikum Sistem Penggerak/Ard Project 2/MLAPanelSurya/datalog_new.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(sensor_data.keys())
        writer.writerow(sensor_data.values())

# Function to periodically write to CSV
def periodically_write_to_csv():
    while True:
        write_to_csv()
        time.sleep(5) # Write the log data every 5s 

# Function to start serial reading in a separate thread
def start_reading():
    threading.Thread(target=read_serial, daemon=True).start()

# Function to start periodically writing to CSV in a separate thread
def start_periodically_writing():
    threading.Thread(target=periodically_write_to_csv, daemon=True).start()


#5. GUI PLAYGROUND
# Create the main window
root = tk.Tk()
root.title("Mini Solar Panel")
root.geometry("600x400")

# Create a frame to hold the labels
frame = tk.Frame(root, bg= "#282c34")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create labels to display the data with enhanced styles
label_style = {"font": ("Helvetica", 12, "bold"), "fg": "#61dafb", "bg": "#282c34", "padx": 10, "pady": 5, "bd": 2, "relief": "groove"}

bus_voltage_label = tk.Label(frame, text="Bus Voltage: Waiting for Data", **label_style)
bus_voltage_label.pack(fill=tk.BOTH, expand=True, pady=5)

shunt_voltage_label = tk.Label(frame, text="Shunt Voltage: Waiting for Data", **label_style)
shunt_voltage_label.pack(fill=tk.BOTH, expand=True, pady=5)

current_label = tk.Label(frame, text="Current: Waiting for Data", **label_style)
current_label.pack(fill=tk.BOTH, expand=True, pady=5)

power_label = tk.Label(frame, text="Power: Waiting for Data", **label_style)
power_label.pack(fill=tk.BOTH, expand=True, pady=5)

load_voltage_label = tk.Label(frame, text="Load Voltage: Waiting for Data", **label_style)
load_voltage_label.pack(fill=tk.BOTH, expand=True, pady=5)

humidity_label = tk.Label(frame, text="Humidity: Waiting for Data", **label_style)
humidity_label.pack(fill=tk.BOTH, expand=True, pady=5)

temperature_label = tk.Label(frame, text="Temperature: Waiting For Data", **label_style)
temperature_label.pack(fill=tk.BOTH, expand=True, pady=5)

anomaly_label = tk.Label(frame, text= 'Waiting Data', font=("Helvetica", 14, "bold"), fg="White", bg="#282c34")
anomaly_label.pack(fill=tk.BOTH, expand=True, pady=5)

# Start reading serial data
start_reading()
# Start periodically writing to CSV
start_periodically_writing()

# Start the GUI main loop
root.mainloop()
