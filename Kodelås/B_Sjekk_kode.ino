void Sjekk_kode(char key){
  String kode = "";
  String dCode = "";
  
  lcd.clear();
  //Når '#' blir trykt tolkes koden som ferdig, og koden bryter ut av while-løkka
  while (true){
    if(key == '#'){break;}
    kode += key;
    dCode += '#';
    lcd.clear();
    lcd.print(dCode);
    key = waitForKeyDeepSleep(deepSleepTime);
  }
  //Sjekker om koden befinner seg i array med beboernes koder
  for(int i=0;i<4;i++){
    if(koder[i] == kode){
      //Om programmet finner en gyldig kode sjekkes personen med samme indeks inn/ut
      Sjekk_inn_ut_beboer(i);
      return;
    }
  }
  //Om koden ikke finns i arrayet for koder blir adgang nektet, og programmet går tilbake
  lcd.clear();
  lcd.print("Access denied");
  delay(1000);
  lcd.clear();
  return;
}

void Sjekk_inn_ut_beboer(int i){

  //Leser verdien fra CoT til en string
  String respons = readCOT(key[i], token[i]);

  //Er personen ute i følge signalet, så blir samme signalet oppdater til å være inne
  if(respons[1] == '0'){
    respons[1] = '4';
    writeCOT(respons, key[i], token[i]);
    lcd.clear();
    lcd.print("Du er sjekket inn!");
    lcd.setCursor(0,1);
    lcd.print("Velkommen inn ");
    lcd.setCursor(0,2);
    lcd.print(navn[i]);
    openDoor(5000);
    lcd.clear();
  }
  //Er personen inne i følge signalet, så blir samme signalet oppdater til å være ute
  else{
    respons[1] = '0';
    writeCOT(respons, key[i], token[i]);
    lcd.clear();
    lcd.print("Du er sjekket ut!");
    lcd.setCursor(0,1);
    lcd.print("Velkommen tilbake ");
    lcd.setCursor(0,2);
    lcd.print(navn[i]);
    openDoor(5000);
    lcd.clear();
  }
  
}
