
#include <Servo.h>
#include <CircusESP32Lib.h>

//kobling til CoT gjennom personlig nettverk
char ssid[] = "SanderPC"; //"Telenor9142per", "SanderPC"
char passord[]= "Kultpassord"; //"Kjempeskulpturene2Avsondret5", "Kultpassord"
char server[] = "www.circusofthings.com";

//tokens
char tFellesrom[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4";
char tVaermeld[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0";
//char t_soverom[] =

//keys
char kStue[] = "4028";
char kKjokken[] = "23658";
char kBad[] = "3657";
char kUteTemp[] = "5917";
//char kSoverom[] = 

//Ovner i form av LEDs?
const int stueOvn = 27;
const int kjokkenOvn = 32;
//const int badOvn =  12;
int ovn[] = {stueOvn, kjokkenOvn}; //badOvn

//servo
static const int servopinStue= 19;
static const int servopinKjokken =15;
static const int servopinBad = 4;

Servo stueServo;
Servo kjokkenServo;
//Servo badServo;

int servoPosStue = 0;
int servoPosKjokken = 0;
//int servoPosBad = 0;


CircusESP32Lib cot(server,ssid,passord);

void setup() {
cot.begin();
Serial.begin(115200);
for(int i=0; i<2; i++){
  pinMode(ovn[i], OUTPUT);}
stueServo.attach(servopinStue);
kjokkenServo.attach(servopinKjokken);
//badServo.attach();
}

void loop() {

 //Henter signalveridene fra CoT, og konverterer dem til String.
  //Konverter for å hente ut bestemte idekser av signalet
  int stueTemp = cot.read(kStue,tFellesrom);
  String stueTempString = String(stueTemp);
  
  int kjokkenTemp = cot.read(kKjokken,tFellesrom);
  String kjokkenTempString = String(kjokkenTemp);
  
  int badTemp = cot.read(kBad,tFellesrom);
  String badTempString = String(badTemp);

  int uteTemp = cot.read(kUteTemp,tVaermeld);
  String utetempString = String(uteTemp);

  //Henter ut ønsket data med indeksering. 
  //Konverterer String til Int igjen for å kunne bruke verdiene videre i programmet
  int stueTempInt = stueTempString.substring(0,2).toInt();
  int beboerStatusStue = stueTempString.substring(2,3).toInt();
  
  int kjokkenTempInt = kjokkenTempString.substring(0,2).toInt();
  int beboerStatusKjokken= kjokkenTempString.substring(4,5).toInt();
  
  int badTempInt = badTempString.substring(0,2).toInt();
  //int beboerStatusBad = badTempString.substring(1,2)
  
  int utetemp = utetempString.substring(1,3).toInt();


  
  
  
  // Dersom betingelsene for if setninge slår inn vil en led lyse, det skal symbolisere at ovnen er på 
  // og rommet varmes opp
    
  if (stueTempInt > utetemp){
    digitalWrite(ovn[0], HIGH);
    if(servoPosStue == 90){
      for (servoPosStue = 0; servoPosStue >= 90; servoPosStue -= 1){ 
        stueServo.write(servoPosStue);            
        delay(15); 
      }
    }
  }
  if (kjokkenTempInt > utetemp){
    digitalWrite(ovn[1], HIGH);
    if(servoPosKjokken == 90){
      for (servoPosKjokken = 0; servoPosKjokken >= 90; servoPosKjokken -= 1){ 
        stueServo.write(servoPosKjokken);            
        delay(15); 
      }
    }
  }
  if (badTemp > utetemp){
    digitalWrite[ovn[2], HIGH];
    if(servoPosBad == 45){
      lukkeVindu(servoPosBad, tid);   
    }
  }
  
  if ((stueTempInt < utetemp)){
    if(beboerStatusStue == 1){
      digitalWrite(ovn[0], LOW);
      for (servoPosStue = 0; servoPosStue <= 90; servoPosStue += 1){ 
        stueServo.write(servoPosStue);
        delay(15);
     }
    }  
    else{
      digitalWrite(ovn[0], LOW);
    }
    }
  
  if (kjokkenTempInt < utetemp){
    if(beboerStatusKjokken == 1){
      digitalWrite(ovn[1], LOW);
      for (servoPosKjokken = 0; servoPosKjokken <= 90; servoPosKjokken += 1){ 
        kjokkenServo.write(servoPosKjokken);              
        delay(15); 
      }
    }
    else{
      digitalWrite(ovn[1], LOW);
    }
  }
  
  if (badTempInt < utetemp){
    if(beboerStatusbad ==1){
      digitalWrite[ovn[2], LOW];
      for (servoPosBad = 0; servoPosBad <= 90; servoPosBad += 1){ 
        badServo.write(servoPosBad);              
        delay(15); 
      }
    }
  delay(200);
  }
