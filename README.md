# Anomaly Detection using Isolation Forest with Arduino

## Overview
This project implements an anomaly detection system using the **Isolation Forest** algorithm to detect unusual sensor readings from an **Arduino** device. The system includes:
- **Data Collection** from Arduino via serial communication
- **Preprocessing** (handling missing values, scaling, etc.)
- **Anomaly Detection** using **Isolation Forest**
- **Real-time Monitoring** through a **Tkinter GUI**

## Features
- Automatic detection of anomalies in sensor readings
- Graphical interface for real-time data visualization
- Efficient and lightweight anomaly detection
- Serial communication between **Arduino** and **Python**

## Installation
### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- Arduino IDE (for flashing the Arduino)
- Required Python libraries:
  ```bash
  pip install numpy pandas scikit-learn pyserial tkinter
  ```

## Usage
### 1. Upload Arduino Code
- Open the Arduino IDE
- Load the corresponding Arduino sketch (e.g., `arduino_sensor.ino`)
- Upload the code to your Arduino board

### 2. Run Python Script
- Ensure the Arduino is connected to your PC via USB
- Open a terminal and run:
  ```bash
  python anomaly_detection.py
  ```

### 3. Monitor the Output
- The Tkinter GUI will display real-time sensor readings
- Anomalies will be highlighted based on the Isolation Forest model

## Project Structure
```
├── arduino_sensor.ino      # Arduino sketch for data collection
├── anomaly_detection.py    # Python script for anomaly detection
├── data_preprocessing.py   # Preprocessing utilities
├── requirements.txt        # Required Python libraries
├── README.md               # Project documentation
```

## How It Works
1. The **Arduino** collects sensor data and sends it to the **Python script** via **serial communication**.
2. The **Python script** preprocesses the data, applies the **Isolation Forest algorithm**, and detects anomalies.
3. The **Tkinter GUI** displays the data and flags anomalies in real-time.

## Future Improvements
- Support for multiple sensors
- Logging detected anomalies for further analysis
- Advanced visualization (e.g., interactive graphs with **Matplotlib**)

## Contributing
Contributions are welcome! Feel free to fork the repository, submit issues, or open pull requests.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---
🚀 **Developed with passion for anomaly detection & embedded systems!**

