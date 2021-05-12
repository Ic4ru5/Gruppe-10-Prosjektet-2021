#include <Servo.h>
#include <CircusESP32Lib.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

//Det som treng for samhandling med CoT legges her
char ssid[] = "Get-2G-B637FF"; //"SanderPC";
char password[] = "rzytz4mt4k"; //"Kultpassord";
char server[] = "www.circusofthings.com";
char token[][85] = {"eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4",
                "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0",
                "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTkxIn0.67_wTOsrUBgKMcvhMVi7AS-yFOsJWRrtQzDs9fEu4zM",
                "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjE1In0.pLf4zCRh8J0ZA1MBsp7hIYGJGqSbc93B4e_KAjUNivk"};
char key[][6] = {"13254", "8056", "11150", "29471"};
CircusESP32Lib circusESP32(server,ssid,password);

//Verdiene som hører sammen legges på samme plass for å gjøre kodingen lettere
String koder[] = {"1111", "2222", "3333", "4444"};
String navn[] = {"Jonas", "Sander", "Ovidius", "Elias"};
char personID[] = {'1','2','3','4'};

//Servo for dørlås kobles på pinne 4
const int servoPin = 4;
//Utgangen som styrer transistoren som igjen skrur av og på lcd-skjermen er koblet på pinne 32
const int lcdControllPin = 32;
// Denne konstanten angir tid med inaktivitet før deep sleep aktiveres
const int deepSleepTime = 10000;

//Verdier for tastaturet
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {27, 26, 25, 33};
byte colPins[COLS] = {13, 12, 14};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS); 

//Oppretter lcd-skjerm med I2C-adresse 0x27
LiquidCrystal_I2C lcd(0x27,20,4);

//Oppretter servo
Servo servo;

void setup(){
  //Skrur på lcd-skjermen, via transistor
  pinMode(lcdControllPin, OUTPUT);
  digitalWrite(lcdControllPin, HIGH);

  //Starter lcd-skjerm
  lcd.begin();
  lcd.backlight();
  lcd.print("Starter opp...");

  //Setter igang serial med baudrate 115200Hz
  Serial.begin(115200);

  //Kobler CoT mot internett
  circusESP32.begin();

  //Knytter servo mot pinne servoPin = 4 
  servo.attach(servoPin);

  //Knytter pinne 34 mot vekking av ESP32 fra deep sleep
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_34,1);
  
}
  
void loop(){

  //Start_screen() stopper programmet til en knapp er trykt. Eller går i deep sleep etter angitt tid
  char key = Start_screen();

  //Om det ble trykt noe annet enn '*' tolkes det som starten på koden
  //Ble '*' trykt blir ringeklokkefunksjon aktivert
  if(key != '*'){
    Sjekk_kode(key);
  }
  else{
    Ringeklokke();
  }
}
