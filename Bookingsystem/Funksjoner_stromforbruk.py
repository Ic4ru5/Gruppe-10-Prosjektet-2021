# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:09:12 2021

@author: Jonas
"""
import Funksjoner_cot as cot
import Klasse_beboer as cBeboere

def oppdater_stromforbruk(sekunder):
      
    cotKey = {"vaermelding":'5917', "stromforbruk":'20086'}
    cotToken = {"vaermelding":'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0',
                "stromforbruk":'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4'}
    
    periodensForbruk = 0
    gammeltForbruk = cot.read_value(cotKey["stromforbruk"], cotToken['stromforbruk'])
    
    uteTemp = int(str(cot.read_value(cotKey["vaermelding"], cotToken['vaermelding']))[1:3])
    
    #Fra SSB.no(2021) var energiforbruk pr. m2 pr. år 149kWh. Dette gir i gjennomsnitt et forbruk på 
    #pr sekund på 4.72*10^-3 Wh/s.
    #Fordelt på 4 beboere blir 1.18 mWh/s
    #Dette tallet blir ganget opp med antall sekunder venteperioden er på, en temperaturkoeffisient
    #og en koeffisient ut i fra hvor beboeren er.
    # Antar at kollektivet er på 70 m2. Antatt forbruk pr beboer er derfor 82.68 mWh/s
    forbruksKonstant = 0.08268
    
    #Fra yr.no var gjennomsnittstemperaturen i Trøndelag 4.4C over ett år. Med utgangspunkt i
    # differansen mellom faktisk utetemperatur og gjennomsnittelig har vi utledet en koeffisient
    # som øker strømforbruket etter utetemperatur. 
    tempKoeffisient = 1 - ((uteTemp-4.4)*0.02)
    
    #En beboer vil bruke mer eller mindre ettersom hvor personen befinner seg. Forbruksberegningen
    # tar derfor hensyn til dette ved å se på hvor personen er.
    romKoeffisienter = {'0':0.2, '1':1.2, '2':1.4, '3':1.4, '4':1.0}

    #Programmet ittererer seg gjennom beboerne, og endrer romkoeffisient etter hvor de er.
    for key in cBeboere.beboere.keys():
        romNr = str(cBeboere.beboere[key].get_room())
        romKoeffisient = romKoeffisienter[romNr]
        periodensForbruk += forbruksKonstant * tempKoeffisient * romKoeffisient * sekunder
        
    #Legger til denne priodens forbruk til totalen, og laster opp til CoT
    totalForbruk = periodensForbruk + gammeltForbruk
    cot.write_value(cotKey["stromforbruk"], cotToken["stromforbruk"], totalForbruk)