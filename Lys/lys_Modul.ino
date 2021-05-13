
#include <CircusESP32Lib.h> // CoT library

// libs. for internet klokke
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Setup av internet klokke
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 7200, 3600000);

// Ruter logginn og påkobling til CoT
char server[] = "www.circusofthings.com";
char ssid[] = "Get-2G-DC8AE1";
char password[] = "AFXABQKCMG";
CircusESP32Lib circusESP32(server, ssid, password);

// Diverse pins påkobblet til ESP32
const byte ledLights[] =  { 12, 14, 27, 26, 25, 2, 4 }; // Stue, Kjøkken, Bad, Soverom(3 - 6)
const byte interruptPins[] = { 16, 17, 18, 19 }; // interrupt pins; rom 1, 2, 3, 4.
const byte ledChannel[] = { 0, 1, 2, 3, 4, 5, 6 }; // kanal for PWM.
const byte ldrSet[] = { 32, 35, 34 }; // LDR pins.
byte lightState[] = { 0, 0, 0, 0 }; // manuel lysbryter beboer status
byte previousLightState[] = { 0, 0, 0, 0 }; // manuel lysbryter beboer status
byte pressNumb[] = { 0, 0, 0, 0 }; // manuel lysbryter beboer status
byte lightPower;

// Tokens og keys for CoT
// Token for fellesrom signaler
char tokenCommon[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4";
char keyStue[] = "4028"; // Key for stuen
char keyKjokken[] = "23658"; // Key for kjøkkenet
char keyBad[] = "3657"; // Key for badet

// CoT Token for verdier fra meteorologisk institutt for skyforhold.
char token_sky[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0";
char key_sky[] = "5917"; // Tokenet for skyforhold.
//

char cotTokens[][86] = {
  "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4", // Beboer rom 1: 0
  "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0", // Beboer rom 2: 1
  "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTkxIn0.67_wTOsrUBgKMcvhMVi7AS-yFOsJWRrtQzDs9fEu4zM", // Beboer rom 3: 2
  "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjE1In0.pLf4zCRh8J0ZA1MBsp7hIYGJGqSbc93B4e_KAjUNivk"
};

char cotKeys[][6] = {
  "13254", // Beboer rom 1: 0
  "8056", // Beboer rom 2: 1
  "11150", // Beboer rom 3: 2
  "29471" // Beboer rom 4: 3
};

enum modusStates {
  defaultState,
  enabledState,
  disabledState
};


//// FUNKSJONER ////


// Setup funksjoner //

void wifiKlokke() {
  Serial.println();
  WiFi.begin(ssid, password);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  timeClient.begin();
}

void manualOverwrite(byte a, byte b) {
  
 if (pressNumb[a] <= 1) {
    if ((lightState[a] == enabledState) || (previousLightState[a] == disabledState)) {
      digitalWrite(ledLights[b], LOW);
      ledcWrite(ledChannel[b], 0);
      lightState[a] = disabledState;
      previousLightState[a] = enabledState;
      pressNumb[a] += 1;

    }
    else if ((lightState[a] == disabledState) ||  (previousLightState[a] == enabledState)) {
      digitalWrite(ledLights[b], HIGH);
      ledcWrite(ledChannel[b], 255);
      lightState[a] = enabledState;
      previousLightState[a] = disabledState;
      pressNumb[a] += 1;

    }
  }
  else {
    digitalWrite(ledLights[b], lightPower);
    ledcWrite(ledChannel[b], lightPower);
    lightState[a] = defaultState;
    pressNumb[a] = 0;
  }
}

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

void lysSetup() {
  // For løkke som etablere diverse pins for ouput, setter en kanal for PWM,
  // og deretter kobbler sammen output pins sammen med kanalen.
  const int freq = 5000; // Frekvensen for PWM kanalen på ESP32.
  const int resolution = 8; // bit størrelsen som passer for frekvensen over.
  for (int i = 0; i <= 6; i++) {
    pinMode(ledLights[i], OUTPUT);
    ledcSetup(ledChannel[i], freq, resolution);
    ledcAttachPin(ledLights[i], ledChannel[i]);
    if (i <= 2) {
      pinMode(ldrSet[i], INPUT);
    }
    if (i <= 3) {
      pinMode(interruptPins[i], INPUT);
      lightState[i] = defaultState;
    }

  }
  attachInterrupt(interruptPins[0], ISR0, FALLING);
  attachInterrupt(interruptPins[1], ISR1, FALLING);
  attachInterrupt(interruptPins[2], ISR2, FALLING);
  attachInterrupt(interruptPins[3], ISR3, FALLING);
}



void romFunksjon (byte a, byte b) {

  if (a == 1) {
    digitalWrite(ledLights[b], lightPower);
    ledcWrite(ledChannel[b], lightPower);
  }
  else {
    digitalWrite(ledLights[b], 0);
    ledcWrite(ledChannel[b], 0);
  }
}

// Lys funksjon som looper

void lysFunksjon() {

  int skyForhold = circusESP32.read(key_sky, token_sky); //  Sky variabelen lest fra CoT. Dette har en verdi fra 1 til 100.
  // CoT signaler som blir sendt fra rPi til CoT
  word stueBook =  circusESP32.read(keyStue, tokenCommon); // Stuen
  int kjokkenBook =  circusESP32.read(keyKjokken, tokenCommon); // Kjøkkenet
  word badBook =  circusESP32.read(keyBad, tokenCommon); // Badet

  // Diverse variabler
  bool state = false;
  byte roomUsed;
  String tidDagFormatert = timeClient.getFormattedTime();
  byte tidDag = timeClient.getHours();
  byte minuttDag = timeClient.getMinutes();
  // booleanske verdier for når fellesrommene er i bruk. Originale signalene er brukt andre plasser,
  // så de ønskedde verdier blir separert til booleanske verdier.
  // 0 eller 1 om rommet er i bruk.
  bool stueState = stueBook % 10;
  bool kjokkenState = kjokkenBook % 10;
  bool badState = badBook % 10;

  // LDR set som regner ut gjennomsnittet av lys forholdene i rommet.

  word ldr0Read = analogRead(ldrSet[0]);
  word ldr1Read = analogRead(ldrSet[1]);
  word ldr2Read = analogRead(ldrSet[2]);
  word ldrMean = (ldr0Read + ldr1Read + ldr2Read) / 3;
  word constrainedMean = constrain(ldrMean, 0, 800); // Justeres etter forholder i rommet. Kan si er som en filter.
  byte ldrPWM = map(constrainedMean, 0, 800, 255, 0); // Bruker gjennomsnittsverdiene til å styre lys PWM.

  // if setning slik at PWM til lysene blir lys etter at solen har gått ned.
  // Det er innstilt slik at mellom klokka 19:00 og 05:00, så blir PWM til -
  // - uavhengig av sky forholds variabelen, dermed blir de makset ut.
  if ((tidDag >= 5) && (tidDag <= 18)) {

    lightPower = ((skyForhold % 100) / 100.00) * 255; // Her blir lightPower variabelen etablert med skyForhold variabelen.
    // Verdien fra skyForhold blir konvertert til en brøk og multiplisert med maks PWM verdi.

  }
  else {
    lightPower = ldrPWM; // Om tiden er utenom if(), vil lyset bli styrt av lys forholdene i rommet.
  }

  // Når en av felles rommene blir aktiv blir lysene i det rommet aktivert og vice versa.
  romFunksjon(stueState, 0); // Stua
  romFunksjon(kjokkenState, 1); // Kjøkken
  romFunksjon(badState, 2); // Bad

  // For beboer rommene. Man skal ikke booke sine egne rom, men man skal booke når man drar fra huset.
  // Slår lys av om beboer er ikke i rommet: beboer er ute, i kjøkkenet, stua eller badet.

  // for løkke for oppdatering av beboerstatusene

  int roomBook[4];
  bool roomBookState[4];
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
    // Etter klokka 23:00 skal alle sove, og da slås alle beboer lysene av. Godnatt! :)
    if ((tidDag >= 23) && (tidDag <= 7)) {
      romFunksjon(roomBookState[0], (a + 3));
      previousLightState[a] = disabledState;
    }
    else if (lightState[a] == defaultState) {
      romFunksjon(roomBookState[a], (a + 3));

    }
    else {
      lightState[a] == defaultState;
    }

  }

  // For testing om verdier stemmer med innkommende signaler
  Serial.println("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓");
  Serial.println();
  Serial.println(String(" BEBOER 1: ") + roomBookState[0] + String(" ┊ BEBOER 2: ") + roomBookState[1] + String(" ┊ BEBOER 3: ") + roomBookState[2] + String(" ┊ BEBOER 4: ") + roomBookState[3]);
  Serial.println(String("Booked status: ") + stueState + String(" ┊ original input: ") + stueBook);
  Serial.println(String("Booked status: ") + kjokkenState + String(" ┊ original input: ") + kjokkenBook);
  Serial.println(String("Booked status: ") + badState + String(" ┊ original input: ") + badBook);
  Serial.println(String("Knapp status: ") + state + String(" ┊ PWM størrelse: ") + lightPower);
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
