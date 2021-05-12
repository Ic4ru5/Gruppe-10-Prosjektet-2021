/* En egen fane for funksjoner som brukes over hele "sketchbook'en" er en ryddig måte holde styr dem*/

String readCOT(char key[], char token[]){
  //Henter og returnerer signal fra CoT, samtidig som den skriver til lcd-skjerm
  lcd.clear();
  lcd.print("Henter data...");
  String respons = String(circusESP32.read(key, token), 0);
  delay(500);
  lcd.clear();
  return respons;
}

void writeCOT(String value, char key[], char token[]){
  //Oppdaterer signal til CoT, samtidig som den skriver til lcd-skjerm
  lcd.clear();
  lcd.print("Sender data...");
  circusESP32.write(key, value.toInt(), token);
  delay(500);
  lcd.clear();
}
void openDoor(int tid){
  //Enkel kode for å åpne dør i angitt tid
  //Selv om koden er ser det mer ryddig ut, og navnet beskriver hva funksjonen skal gjøre
  servo.write(90);
  delay(tid);
  servo.write(0);
}

char waitForKeyDeepSleep(int deepSleepTimer){
  //keypad.getKey() returnere NO_KEY hvis ingen knapp trykkes
  char key = keypad.getKey();
  //Deepsleep-timer settes angitt periode fram i tid
  deepSleepTimer += millis();
  //Så lenge ingen knapp trykkes forblir koden i while-løkka
  while(key == NO_KEY){
    key = keypad.getKey();
    //Om millis() rekker å ta igjen deepSleepTimer blir ESP32 satt i deep sleep-modus
    if (deepSleepTimer < millis()){
      lcd.clear();
      esp_deep_sleep_start();
    }
  }
  //Trykkes en knapp inn bryter koden ut av while-løkka, og funksjonen returnerer trykt knapp
  return key;
}
