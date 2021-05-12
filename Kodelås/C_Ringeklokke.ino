void Ringeklokke(){
  lcd.clear();
  //Skriver navnene til beboerne på lcd-skjermen, knyttet til et nummer
  for(int i = 0; i < 4;i++){
    lcd.setCursor(0, i);
    lcd.print(personID[i]);
    lcd.print(" - ");
    lcd.print(navn[i]);
  }
  
  //Ut fra hvilket nummer som blir trykt, sjekkes data for valgt beboer
  //Riktig beboer velges ut med switch-case
  switch(waitForKeyDeepSleep(deepSleepTime)){
    case '1':
      Beboer_gjest(0);
      break;
    case '2':
      Beboer_gjest(1);
      break;
    case '3':
      Beboer_gjest(2);
      break;
    case '4':
      Beboer_gjest(3);
      break;
  }
}

void Beboer_gjest(int i){
  //Brukes for å gi beskjed om hvor beboern oppholder seg. Indeksering på arrayet stemmer over ens med signalet fra CoT
  String rom[] = {"ute","stuen","kjokkenet","badet","soverommet"};
  //Leser valgt beboers beboersignal
  String respons = readCOT(key[i], token[i]);
  //Henter ut verdiene vi ønsker
  int gjester = respons.substring(4,5).toInt();
  int romIdx = respons.substring(1,2).toInt();

  //Betyr at beboern ikke er hjemme, og slipper ikke inn gjest
  if(romIdx == 0){
    lcd.clear();
    lcd.print(navn[i] + " er ute");
    lcd.setCursor(0,1);
    lcd.print("Kom igjen senere");
    delay(5000);
    lcd.clear();
  }
  //Beboern har ikke booket noen gjester, og slipper ikke inn gjest
  else if (gjester <= 0){
    lcd.clear();
    lcd.print("Ingen gjester booket");
    lcd.setCursor(0,1);
    lcd.print("paa " + navn[i]); 
    lcd.setCursor(0,2);
    lcd.print("Kom igjen senere");
    delay(5000);
    lcd.clear();
  }
  //Kommer koden seg hit, betyr det at beboer er hjemme med aktiv gjestebooking, og gjest slipper inn
  else {
    lcd.clear();
    lcd.print("Velkommen inn!");
    lcd.setCursor(0,1);
    lcd.print(navn[i] + " er paa/i"); 
    lcd.setCursor(0,2);
    //Gir beskjed om hvilket rom beboer er i
    lcd.print(rom[romIdx]);
    openDoor(5000);
    lcd.clear();
  }
}
