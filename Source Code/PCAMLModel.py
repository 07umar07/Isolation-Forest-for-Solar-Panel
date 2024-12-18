import pandas as pd
import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor

# Serial port connection
# ser = serial.Serial('/dev/ttyUSB0', 9600)
# time.sleep(2)

# Datasets featuring
df = pd.read_csv('/home/umar/Documents/Kuliah/Semester 5/Praktikum Sistem Penggerak/Ard Project 2/MLAPanelSurya/Datasets/CSV/final_data.csv')
print(df.columns)
print(df.shape)


# I think Bus Voltage, Shunt Voltage, Power, and Date Time is not really important imho
# So i decide to drop it out
df = df.drop(columns= ['Date Time', 'Bus Voltage(V)', 'Shunt Voltage(mV)'])
print(df.head())

first_10_rows = df.iloc[14:25]

# Create a figure and axis
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')

# Create the table
table = ax.table(cellText=first_10_rows.values, colLabels=first_10_rows.columns, cellLoc='center', loc='center')

# Adjust the font size and layout
table.auto_set_font_size(False)
table.set_fontsize(18)
table.scale(1.2, 1.2)

# Display the table
plt.show()

# Handling Shit zeroes
imputer = SimpleImputer(strategy='mean')
imputed_data = imputer.fit_transform(df)

# And then i scales the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(imputed_data)
print(scaled_data)

# # Principal Component Analysis
# pca = PCA(n_components= 2)
# principal_components = pca.fit_transform(scaled_data)
# # And i convert back to pandas dataframe
# principal_components_df = pd.DataFrame(data= principal_components, columns=['PC1', 'PC2'])

# # Show PCA Data
# plt.figure(figsize=(10, 7))
# plt.scatter(principal_components_df['PC1'], principal_components_df['PC2'], s=50)
# plt.xlabel('Principal Components I')
# plt.ylabel('Principal Components II')
# plt.title('Principal Component Analysis')
# plt.show()

# #----------------------------------------------------------------------------------------------------
# #Local Outlier Factor Boundaries to predict anomaly
# local_outlier_factor = LocalOutlierFactor(n_neighbors= 20)
# predictor = local_outlier_factor.fit_predict(principal_components)
# df['anomalies'] = predictor

# # Calculate how many times anomaly occured
# print(df['anomalies'].value_counts()[-1])

# # Give it to serial bus
# for a in df['anomalies']:
#   ser.write(str(a).encode)
#   ser.write(b'\n')

#-------------------------------------------RANDOM FOREST
iso_forest = IsolationForest(contamination=0.01, random_state=37)
iso_forest.fit(scaled_data)
df['anomaly']= iso_forest.predict(scaled_data)
print(df.head())

# Visualizing Anomalies
normal = df[df['anomaly'] == 1]
anomaly = df[df['anomaly'] == -1]
total_anomalies = anomaly.shape[0]
total_data = df.shape[0]
anomaly_percentage = (total_anomalies/total_data) * 100 
print(f"{anomaly_percentage} %")

plt.figure(figsize=(14, 8))
plt.scatter(normal['Humidity(%)'], normal['Temperature(oC)'], label='Normal', c='blue', s=20)
plt.scatter(anomaly['Humidity(%)'], anomaly['Temperature(oC)'], label='Anomaly', c='red', s=20)
plt.title('Isolation Forest Anomaly Detection')
plt.xlabel('Humidity (%)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()

plt.figure(figsize=(14, 8))
plt.scatter(normal['Current(mA)'], normal['Load Voltge(V)'], label='Normal', c='blue', s=20)
plt.scatter(anomaly['Current(mA)'], anomaly['Load Voltge(V)'], label='Anomaly', c='red', s=20)
plt.title('Isolation Forest Anomaly Detection')
plt.xlabel('Current (mA)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.show()

# sns.pairplot(df, hue='anomaly', diag_kind='kde', markers=['o', 's'], 
#              plot_kws={'alpha': 0.5, 's': 20})

# plt.suptitle('Isolation Forest Anomaly Detection', y=1.02)
# plt.show()




def detect_anomaly(data):
    # Convert the data to DataFrame if it's not already
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame([data])  # Convert dictionary to DataFrame with a single row

    # Ensure columns match the order and names of the original DataFrame used for training
    data = data[df.columns[:-1]]  # Exclude 'anomaly' if added

    # Transform the data using the previously fitted imputer and scaler
    imputed_data = imputer.transform(data)
    scaled_data = scaler.transform(imputed_data)
    
    # Predict using the trained isolation forest
    prediction = iso_forest.predict(scaled_data)
    return prediction[0]  # Return -1 (anomaly) or 1 (normal)

# Sample input data
# data_value = {
#     "Temperature(oC)": 0.0,
#     "Shunt Voltage(mV)": 0.0,
#     "Humidity(%)": 0.0,
#     "Current(mA)": 0.0,
#     "Power(mW)": 0.0,
#     "Load Voltge(V)": 0.0
# }
# df_new = pd.DataFrame([data_value])
# print(detect_anomaly(df_new))


