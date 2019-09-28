/* This code use the DHT-22 sensor with Arduino uno
   Temperature and humidity sensor
   MARATHON UPC project */

//Libraries
#include <DHT.h>

//Constants
#define DHTPIN 4     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino


//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

void setup()
{
  Serial.begin(9600);
  dht.begin();
}

void loop()
{
    //int chk = DHT.read22(DHTPIN);
    //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp= dht.readTemperature(false);
     
    // check if returns are valid, if they are NaN (not a number) then something went wrong!
    if (isnan(temp) || isnan(hum)) {
      Serial.println("Failed to read from DHT");
    } 
    else {
      //Print temp and humidity values to serial monitor
      Serial.print("Humidity: ");
      Serial.print(hum);
      Serial.print(" %, Temp: ");
      Serial.print(temp);
      Serial.println(" Celsius");
      delay(2000); //Delay 2 sec.
    } 
}

   
