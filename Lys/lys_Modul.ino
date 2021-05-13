
#include <CircusESP32Lib.h> // CoT library

// libs. for internet klokke
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Ruter logginn og påkobling til CoT med selvbeskrivende konstanter
char server[] = "www.circusofthings.com";
char ssid[] = "SSID";
char password[] = "hunter2";
CircusESP32Lib circusESP32(server, ssid, password);

// // // // FUNKSJONER // // // //

// Setup av internet klokke
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 7200, 3600000);

void wifiKlokke() {
  Serial.println();
  WiFi.begin(ssid, password);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  timeClient.begin();
}

// Statemaskin for lysene brukt med knapp.

byte lightPower;
byte lightState[] = { 0, 0, 0, 0 };
byte previousLightState[] = { 0, 0, 0, 0 };
byte pressNumb[] = { 0, 0, 0, 0 }; // Array for hvor mange ganger knappet ble trykt for hvert rom.
const byte LED_LIGHTS[] =  { 12, 14, 27, 26, 25, 2, 4 }; // Stue, Kjøkken, Bad, Soverom(3 - 6)
const byte LED_CHANNEL[] = { 0, 1, 2, 3, 4, 5, 6 }; // kanal for PWM.

enum modusStates {
  defaultState,
  enabledState,
  disabledState
};

/**
	En funksjon brukt for ISR. Endrer statuser til beboerrommene basert på den aktive statusen, og vipper til det motsatte
	statusen. Om trykt tre ganger blir telleren satt til "0" som er defaultState. Funksjonen halter ikke systemet helt, bare endrer status.
	byte "a" henvise til beboerromet mens byte "b" er beboerlyset til rommet.
*/

void manualOverwrite(byte a, byte b) {
  if (pressNumb[a] <= 1) {
    if ((lightState[a] == enabledState) || (previousLightState[a] == disabledState)) {
      digitalWrite(LED_LIGHTS[b], LOW);
      ledcWrite(LED_CHANNEL[b], 0);
      lightState[a] = disabledState;
      previousLightState[a] = enabledState;
      pressNumb[a] += 1;
    }
    else if ((lightState[a] == disabledState) ||  (previousLightState[a] == enabledState)) {
      digitalWrite(LED_LIGHTS[b], HIGH);
      ledcWrite(LED_CHANNEL[b], 255);
      lightState[a] = enabledState;
      previousLightState[a] = disabledState;
      pressNumb[a] += 1;
    }
  }
  else {
    digitalWrite(LED_LIGHTS[b], lightPower);
    ledcWrite(LED_CHANNEL[b], lightPower);
    lightState[a] = defaultState;
    pressNumb[a] = 0;
  }
}
/**

  ISR funksjoner som bruker funksjonen "manualOverwrite".
  Første byte henvise til beboerrom statuser
  mens den andre byte er lyset til rommet.

*/

void IRAM_ATTR ISR0() {
  manualOverwrite(0, 3);
}
void IRAM_ATTR ISR1() {
  manualOverwrite(1, 4);
}
void IRAM_ATTR ISR2() {
  manualOverwrite(2, 5);
}
void IRAM_ATTR ISR3() {
  manualOverwrite(3, 6);
}


const byte LDR_SET[] = { 32, 35, 34 };

/**
  Setup for diverse pins på ESP32.
*/

void lysSetup() {
  const byte INTERRUPT_PINS[] = { 16, 17, 18, 19 }; // interrupt pins; rom 1, 2, 3, 4.
  const int FREQ = 5000;
  const byte RESOLUTION = 8;

  for (byte i = 0; i <= 6; i++) {
    pinMode(LED_LIGHTS[i], OUTPUT);
    ledcSetup(LED_CHANNEL[i], FREQ, RESOLUTION);
    ledcAttachPin(LED_LIGHTS[i], LED_CHANNEL[i]);
    if (i <= 2) {
      pinMode(LDR_SET[i], INPUT);
    }
    if (i <= 3) {
      pinMode(INTERRUPT_PINS[i], INPUT);
      lightState[i] = defaultState;
    }
  }
  attachInterrupt(INTERRUPT_PINS[0], ISR0, FALLING);
  attachInterrupt(INTERRUPT_PINS[1], ISR1, FALLING);
  attachInterrupt(INTERRUPT_PINS[2], ISR2, FALLING);
  attachInterrupt(INTERRUPT_PINS[3], ISR3, FALLING);
}


/**
  Funksjon for å endre statusene til diverse rom; brukt med for løkker.
*/

void romFunksjon (byte a, byte b) {

  if (a == 1) {
    digitalWrite(LED_LIGHTS[b], lightPower);
    ledcWrite(LED_CHANNEL[b], lightPower);
  }
  else {
    digitalWrite(LED_LIGHTS[b], 0);
    ledcWrite(LED_CHANNEL[b], 0);
  }
}

// CoT Token for verdier fra meteorologisk institutt for skyforhold.
char token_sky[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0";
char key_sky[] = "5917"; // Tokenet for skyforhold.

// Token for fellesrom signaler
char tokenCommon[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4";
char keyStue[] = "4028"; // Key for stuen
char keyKjokken[] = "23658"; // Key for kjøkkenet
char keyBad[] = "3657"; // Key for badet

/**
  Hovedfunksjon som går i loop. Oppdatere statuser fra CoT signalene og LDR lesinger.
  Endrer statuser til alle pins på ESP32.
*/

void lysFunksjon() {
  //  Sky variabelen lest fra CoT. Dette har en verdi fra 0 til 100.
  int skyForhold = circusESP32.read(key_sky, token_sky);

  // CoT signaler //
  word stueBook =  circusESP32.read(keyStue, tokenCommon); // Stuen
  int kjokkenBook =  circusESP32.read(keyKjokken, tokenCommon); // Kjøkkenet
  word badBook =  circusESP32.read(keyBad, tokenCommon); // Badet

  // Henter tid fra WiFi
  String tidDagFormatert = timeClient.getFormattedTime();
  byte tidDag = timeClient.getHours();

  /**
    booleanske verdier for når fellesrommene er i bruk. Originale signalene er brukt til sammenligning i print(),
    så de ønskede verdier blir separert til booleanske verdier for status endringer.
    0 eller 1 om rommet er i bruk.
  */
  bool stueState = stueBook % 10;
  bool kjokkenState = kjokkenBook % 10;
  bool badState = badBook % 10;

  // LDR set som regner ut gjennomsnittet av lys forholdene i rommet.
  word ldr0Read = analogRead(LDR_SET[0]);
  word ldr1Read = analogRead(LDR_SET[1]);
  word ldr2Read = analogRead(LDR_SET[2]);
  word ldrMean = (ldr0Read + ldr1Read + ldr2Read) / 3;
  word constrainedMean = constrain(ldrMean, 0, 800);
  byte ldrPWM = map(constrainedMean, 0, 800, 255, 0);

  /** PWM til lysene blir lav etter at solen har gått ned.
  */
  if ((tidDag >= 5) && (tidDag <= 21)) {
    /**
      LightPower variabelen etablert med skyForhold variabelen.
      Verdien fra skyForhold blir konvertert til en prosent og multiplisert med maks PWM verdi.
    */
    lightPower = ((skyForhold % 100) / 100.00) * 255;
  }
  // Om tiden er utenom if(), vil lyset bli styrt av lys forholdene i rommet.
  else {
    lightPower = ldrPWM;
  }

  // Fellesrommene endrer status basert på booking
  romFunksjon(stueState, 0); // Stua
  romFunksjon(kjokkenState, 1); // Kjøkken
  romFunksjon(badState, 2); // Bad


  //// Egen seksjon for beboerrommene

  int roomBook[4];
  bool roomBookState[4];
  char cotTokens[][86] = {
    "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4", // Beboer rom 1: 0
    "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0", // Beboer rom 2: 1
    "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTkxIn0.67_wTOsrUBgKMcvhMVi7AS-yFOsJWRrtQzDs9fEu4zM", // Beboer rom 3: 2
    "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjE1In0.pLf4zCRh8J0ZA1MBsp7hIYGJGqSbc93B4e_KAjUNivk"  // Beboer rom 4: 3
  };
  char cotKeys[][6] = {
    "13254", // Beboer rom 1: 0
    "8056", // Beboer rom 2: 1
    "11150", // Beboer rom 3: 2
    "29471" // Beboer rom 4: 3
  };


  /**
	Løkken oppdatere alle beboerrommene for statusendringer. 
	Kontrolere og opprettholde manualOverwrite() funksjonen med å sjekke endring av lysstatuser fra ISR funksjonen.
  */
  for (byte a = 0; a <= 3; a++) {
    roomBook[a] = circusESP32.read(cotKeys[a], cotTokens[a]);
    roomBook[a] = (roomBook[a] / 1000) % 10;
    if (roomBook[a] == 4) {
      roomBookState[a] = 1;
      if (lightState[a] == defaultState) {
        previousLightState[a] = disabledState;
      }
    }
    else {
      roomBookState[a] = 0;
      if (lightState[a] == defaultState) {
        previousLightState[a] = enabledState;
      }
    }
    // Etter klokka 23:00 skal alle sove, og da slås alle beboer lysene av. Antatt at alle skal våkne klokken 7.
    if ((tidDag >= 23) && (tidDag <= 7)) {
      romFunksjon(roomBookState[0], (a + 3));
      previousLightState[a] = disabledState;
    }
    else if (lightState[a] == defaultState) {
      romFunksjon(roomBookState[a], (a + 3));
    }
  }

  // For testing om verdier stemmer med innkommende signaler
  Serial.println("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓");
  Serial.println();
  Serial.println(String(" BEBOER 1: ") + roomBookState[0] + String(" ┊ BEBOER 2: ") + roomBookState[1] + String(" ┊ BEBOER 3: ") + roomBookState[2] + String(" ┊ BEBOER 4: ") + roomBookState[3]);
  Serial.println(String("Booked status: ") + stueState + String(" ┊ original input: ") + stueBook);
  Serial.println(String("Booked status: ") + kjokkenState + String(" ┊ original input: ") + kjokkenBook);
  Serial.println(String("Booked status: ") + badState + String(" ┊ original input: ") + badBook);
  Serial.println(String("PWM størrelse: ") + lightPower);
  Serial.println(String("Time: ") + tidDag + String(" ┊ original input: ") + tidDagFormatert);
  Serial.println(String("LDR read 1: ") + ldr0Read + String(" ┊ LDR read 2: ") + ldr1Read + String(" ┊ LDR read 3: ") + ldr2Read);
  Serial.println(String("LDR Constrained mean: ") + constrainedMean + String(" ┊ LDR Mean: ") + ldrMean + String(" ┊ LDR PWM: ") + ldrPWM);
  Serial.println(String("sky forhold: ") + skyForhold % 100 + String("%") + String(" Lys styrke: ") + lightPower);
  Serial.println();
  Serial.println("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛");
}

void setup() {
  Serial.begin(9600);
  circusESP32.begin();
  wifiKlokke();
  lysSetup();
}

void loop() {
  timeClient.update();
  lysFunksjon();
}
