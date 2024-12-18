#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_INA219.h>
#include <DHT.h>
#include <TimeLib.h>

// DHT11 Sensor Pin
#define DHTPIN 2
// Define DHT 11
#define DHTTYPE DHT11
// INA219 Sensor Object
Adafruit_INA219 ina219;
// DHT Sensor Object
DHT dht(DHTPIN, DHTTYPE);

// Relay Pin 3
#define relayPin 3

// ANomaly Lamp pin 4
#define LEDPin 4

void setup() 
{
  // put your setup code here, to run once:
  // Serial Comunication
  Serial.begin(9600);

  // INA219 Sensor
  if (!ina219.begin())
  {
    Serial.println("Unable to find INA219 Sensor!");
    while(1)
    {
      delay(10);
    }
  }

  dht.begin();

  Serial.println("Setup is ready to go!");

  // Output mode
  pinMode(relayPin, OUTPUT);
  pinMode(LEDPin, OUTPUT);

  // Time set
  setTime(17, 36, 0, 3, 12, 2024); // hmsdmy
}

void loop() {
  // put your main code here, to run repeatedly:
  float shuntVoltage = 0;
  float busVoltage = 0;
  float current_mA = 0;
  float loadVoltage = 0;
  float power_mW = 0;

  shuntVoltage = ina219.getShuntVoltage_mV();
  busVoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadVoltage = busVoltage + (shuntVoltage / 1000);

  // Print INA219 Sensor Reading
  Serial.print("Bus Voltage: "); Serial.println(busVoltage);
  Serial.print("Shunt Voltage: "); Serial.println(shuntVoltage); 
  Serial.print("Current: "); Serial.println(current_mA); 
  Serial.print("Power: "); Serial.println(power_mW); 
  Serial.print("Load Voltage: "); Serial.println(loadVoltage); 
  Serial.println("");

  // Read Temperature and Humidity from DHT11 Sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature))
  {
    Serial.println("DHT11 Sensor Read failed!!");
    return;
  } 

  Serial.print("Humidity: "); Serial.println(humidity);
  Serial.print("Temperature: "); Serial.println(temperature);
  // digitalWrite(LEDPin, HIGH);
  // Anomaly Signal from Python
  if (Serial.available() > 0) 
  {
    char data = Serial.read(); //Incoming singal
    Serial.print("Received data: ");  // Debug print
    Serial.println(data);  // Debug print
    if (data == '1') {
        digitalWrite(LEDPin, HIGH); // Turn on the LED
        Serial.println("LED ON");  // Debug print
    } else 
    {
        digitalWrite(LEDPin, LOW); // Turn off the LED
        Serial.println("LED OFF");  // Debug print
    }
  }


  //Turn on relay between 18 and 6 oclock
  int currentHour = hour();
  int currentMinute = minute();
  Serial.print(currentHour);
  // digitalWrite(relayPin, LOW);
  if ((currentHour >= 16 && currentHour <= 23) || (currentHour >= 0 && currentHour < 6))
  {
    Serial.println("Turning Relay On");
    digitalWrite(relayPin, LOW);
  }else
  {
    Serial.println("Turning Relay Off");
    digitalWrite(relayPin, HIGH);
  }

  // Relay Test
  // Serial.println("Turning relay ON");
  // digitalWrite(relayPin, HIGH);
  // delay(1000);
  // Serial.println("Turning relay OFF");
  // digitalWrite(relayPin, LOW);
  // delay(1000);

  delay(1000);
}
