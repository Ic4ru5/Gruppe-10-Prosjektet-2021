# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 17:23:46 2021

@author: Jonas
"""
from time import time, sleep

import Funksjoner_bad as bad
import Funksjoner_stue as stue
import Funksjoner_kjokken as kjokken
import Funksjoner_gjest as gjest
import Funksjoner_met as met
import Funksjoner_stromforbruk as stromforbruk
import Funksjoner_stromgenerering as stromgenerering
import Klasse_beboer as cBeboere


def sjekk_for_booking():
    
    #Ittererer gjennom beboerene
    for key in cBeboere.beboere.keys(): 
        #Henter dekodet konsollsignal
        konsollSignal = cBeboere.beboere[key].get_konsollSignal() 
        
        
        #Ser etter innkomende booking for rom 1 (Stue)
        if konsollSignal['bookingStatus'] == '1' and konsollSignal['rom'] == '1': #Signaliserer inkommende booking og hvilket rom
            #Konsollsignalet inneholder data for den ønskede bookingen. Og sendes til book_stue() for å 
            # sjekke om det er ledig.
            respons = stue.book_stue(konsollSignal)
            #Hvis bookingen IKKE var suksessfull inneholder respons variabelen "nyTid"
            #Respons blir brukt for å gi tilbakemelding på hvordan bookingen gikk, evt med ny tid
            if 'nyTid' in respons:
                value = (str(konsollSignal['personID'])+str(respons['nyTid'])+
                         str(konsollSignal['rom'])+str(konsollSignal['ovntemperatur'])+str(respons['status']))
            else:
                value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                         str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                         str(konsollSignal['ovntemperatur'])+str(respons['status']))
            #Skriver respons til CoT
            cBeboere.beboere[key].set_konsollSignal_raw(value)
        #Ser etter innkommende kansellering av bookinger på rom 1 (stue)
        elif konsollSignal['bookingStatus'] == '2' and konsollSignal['rom'] == '1': #Signaliserer inkommende kansellering og hvilket rom
            #For å kansellere stuebookinger kjøres "kanseller_stue"
            respons = stue.kanseller_stue(konsollSignal)
            value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                     str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                     str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
        
        #Sjekker for rom 2 (Kjokken)
        #Kommentarer for stue gjelder også her
        if konsollSignal['bookingStatus'] == '1' and konsollSignal['rom'] == '2': #Signaliserer inkommende booking og hvilket rom
            respons = kjokken.book_kjokken(konsollSignal)
            print(respons)
            if 'nyTid' in respons:
                value = (str(konsollSignal['personID'])+str(respons['nyTid'])+
                         str(konsollSignal['rom'])+str(konsollSignal['ovntemperatur'])+str(respons['status']))
            else:
                value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                         str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                         str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
        elif konsollSignal['bookingStatus'] == '2' and konsollSignal['rom'] == '2': #Signaliserer inkommende kansellering og hvilket rom
            respons = kjokken.kanseller_kjokken(konsollSignal)
            value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                     str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                     str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
            print(respons)
            
        #Sjekker for rom 3 (Bad)
        #Kommentarer for stue gjelder også her
        if konsollSignal['bookingStatus'] == '1' and konsollSignal['rom'] == '3': #Signaliserer inkommende booking og hvilket rom
            respons = bad.book_bad(konsollSignal)
            print(respons)
            if 'nyTid' in respons:
                value = (str(konsollSignal['personID'])+str(respons['nyTid'])+
                         str(konsollSignal['rom'])+str(konsollSignal['ovntemperatur'])+str(respons['status']))
            else:
                value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                         str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                         str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
        elif konsollSignal['bookingStatus'] == '2' and konsollSignal['rom'] == '3': #Signaliserer inkommende kansellering og hvilket rom
            respons = bad.kanseller_bad(konsollSignal)
            value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                     str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                     str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
            print(respons)
            
        #Sjekker for gjester 4
        #Kommentarer for stue gjelder også her
        if konsollSignal['bookingStatus'] == '1' and konsollSignal['rom'] == '4': #Signaliserer inkommende booking og hvilket rom
            respons = gjest.book_gjest(konsollSignal)
            print(respons)
            if 'nyTid' in respons:
                value = (str(konsollSignal['personID'])+str(respons['nyTid'])+
                         str(konsollSignal['rom'])+str(konsollSignal['ovntemperatur'])+str(respons['status']))
            else:
                value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                         str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                         str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
        elif konsollSignal['bookingStatus'] == '2' and konsollSignal['rom'] == '4': #Signaliserer inkommende kansellering og hvilket rom
            respons = gjest.kanseller_gjest(konsollSignal)
            value = (str(konsollSignal['personID'])+konsollSignal['bookingTid'].strftime("%m%d%H%M")+
                     str(int(konsollSignal['bookingVarighet'].seconds//60)).zfill(2)+str(konsollSignal['rom'])+
                     str(konsollSignal['ovntemperatur'])+str(respons['status']))
            cBeboere.beboere[key].set_konsollSignal_raw(value)
            print(respons)
        
        #Om romsignalet inneholder et ubrukt romnr. returneres signalet med en feilmelding
        elif konsollSignal['rom'] != '1' and konsollSignal['rom'] != '2' and konsollSignal['rom'] != '3' and konsollSignal['rom'] != '4':
            if konsollSignal['bookingStatus'] == '1' or konsollSignal['bookingStatus'] == '2':
                value = (str(konsollSignal['personID'])+str(konsollSignal['bookingTid'])+str(konsollSignal['bookingVarighet'])+
                         str(konsollSignal['rom'])+str(konsollSignal['ovntemperatur'])+'5')
                cBeboere.beboere[key].set_konsollSignal_raw(value)
            
            
#Leser inn beboere, og lager en dictionary med beboer-objekter
cBeboere.les_inn_beboere()
# Den neste samplingstiden må bestemmes før while-løkka. Bestemmes av ventetidTimer.
ventetidTimer1 = 1
ventetidTimer2 = 10
timer1 = time()
timer2 = time()
sleep(0.1)
while(True): # Kjøres "uendelig".
    
    #Fanger exceptions som funksjonene ikke ordner selv. Printer hva som gikk galt, og venter 15 sek
    # før programmet prøver på nytt. Dette gir mulighet for å fikse feilen uten at en må inn på 
    # serveren/PIen for å sette igang programmet.
    try:
        #Timer 1 kjører på eget intervall
        if timer1 < time(): # Kjøres på et fast intervall.
            sjekk_for_booking() #Sjekker CoT for innkommende bookinger
            # Sett neste samplingstid.
            timer1 += ventetidTimer1
            
        if timer2 < time():
            stue.skanne_bookinger_stue() #Sjekker bookingsystem for aktive bookinger
            kjokken.skanne_bookinger_kjokken() #Sjekker bookingsystem for aktive bookinger
            bad.skanne_bookinger_bad() #Sjekker bookingsystem for aktive bookinger
            gjest.skanne_bookinger_gjest() #Sjekker bookingsystem for aktive bookinger
            met.getForecast() #Oppdaterer værdata
            stromforbruk.oppdater_stromforbruk(ventetidTimer2) #Oppdaterer strømforbruk, mht varigheten mellom hver gang den kjøres
            stromgenerering.wHgenerertfunct(ventetidTimer2, nullstill=0)
            # Sett neste samplingstid.
            timer2 += ventetidTimer2
    except Exception as e:
        print("Error: {0}".format(e), 'Programmet starter på nytt etter 15 sekunder')
        sleep(15)
        