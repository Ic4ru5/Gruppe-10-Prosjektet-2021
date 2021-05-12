char Start_screen(){

  //Skriver hva bruker skal gjøre på lcd-skjermen
  lcd.clear();
  lcd.print("Skriv inn kode,");
  lcd.setCursor(0, 1);
  lcd.print("eller trykk *");

  //Venter her helt til en knapp er trykt, eller deep sleep blir aktivert
  char key = waitForKeyDeepSleep(deepSleepTime);
  return key;
}
