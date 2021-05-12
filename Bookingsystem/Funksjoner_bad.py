# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:36:01 2021

Funksjonene for de forskjellige bookingmulighetene er nok så like. En naturlig fremgangsmåte hadde derfor vært å kombinere disse til en funksjon.
Dette ble ikke gjort fordi alle funksjonene har alle sine små finurligheter som differere dem. Dette hadde gitt ca. samme mengde kode, men kombinert i samme 
funksjon med masse if-løkker. Syns derfor det er mye mer oversiktelig å dele de opp slik det er gjort nå.

@author: Jonas
"""

from datetime import timedelta as timedelta
from datetime import datetime as dt
from pandas import pandas as pd

import Funksjoner_romsignal as romSignal
import Klasse_beboer as cBeboere

#Forhåndsdefinerte tilbakemeldingsstatuser
#Globale fordi de brukes i alle funksjonene
statuser = {'suksess':3, 'opptatt':4, 'feil':5}

def book_bad(signal):
    
    #Laster inn bookinger som allerede ligger inne fra csv-fil.
    df_booking_bad = pd.read_csv("Booking_bad.csv", dtype=str)
    df_booking_bad["tidspunktStart"] = pd.to_datetime(df_booking_bad["tidspunktStart"])
    df_booking_bad["tidspunktSlutt"] = pd.to_datetime(df_booking_bad["tidspunktSlutt"])

    #Henter ut nødvendig data fra konsollsignalet
    personID = signal["personID"]
    dtStart = signal["bookingTid"]
    varighet = signal["bookingVarighet"]
    dtSlutt = dtStart + varighet
    
    #Beboerns ønskede temperatur ligger i beboersignalet. Den hentes gjennom instansen opprettet for gjeldene beboer
    temp = cBeboere.beboere[personID].get_temperatur() #Klassetest
    
    
    
    #Sjekker om datoen er ikke er fortid
    if dtSlutt < dt.now():
        return {'melding':"Feil, velg en dato frem i tid", 'status':statuser['feil']}
    #Sjekker om ønsket tid overlapper med noen annens
    for i in range(len(df_booking_bad)):
        if dtStart <= df_booking_bad["tidspunktSlutt"][i] and dtSlutt >= df_booking_bad["tidspunktStart"][i]:
            nyVarighet = '99'
            
            #Hvis det finnes en booking som starter etter denne, så regner programmet ut tid mellom bookingene
            #Om tiden mellom bookingene overstiger 99 min, kan ikke signalet sende et høyere tall som forslag til varighet
            try: 
                tidMellomBookinger = df_booking_bad["tidspunktStart"][i+1] - df_booking_bad["tidspunktSlutt"][i]
                if (tidMellomBookinger <= timedelta(minutes=100)):
                    nyVarighet = "{0:0=2d}".format(int(tidMellomBookinger.seconds/60))
                    
            #Det finnes ingen senere booking, foreslår 99 minutter varighet automatisk        
            except:
                pass
            
            #Legger til et minutt for slutttiden er fortsatt opptatt
            nyttTidspunkt = df_booking_bad["tidspunktSlutt"][i] + timedelta(minutes=1)
            nyTid = nyttTidspunkt.strftime("%m%d%H%M") + nyVarighet
            return {'melding':"Feil, allerede booket", 'status':statuser['opptatt'], 'nyTid':nyTid}
    
    #Returnerer ny tid + status for bookingen
    #Og skriver booking til csv-fil
    df_new_booking = pd.DataFrame([[personID,dtStart,dtSlutt,temp]], columns=df_booking_bad.keys())
    df_booking_bad = df_booking_bad.append(df_new_booking, ignore_index=True)
    df_booking_bad = df_booking_bad.sort_values(by=["tidspunktStart"])
    df_booking_bad.to_csv("Booking_bad.csv", index=False)
    return {'melding':"Suksess, din tid er nå booket", 'status':statuser['suksess']}

def kanseller_bad(signal):
    
    #Leser inn bookinger fra csv-fil
    df_booking_bad = pd.read_csv("Booking_bad.csv", dtype=str)
    
    #Henter nødvendig data fra innkommende signal
    personID = signal["personID"]
    navn = cBeboere.beboere[personID].navn 
    
    #Sjekker om beboer har eksisterende booking
    if personID not in df_booking_bad["personID"].values:
        return {'melding':"Ingen booking på " + navn, 'status':statuser['feil']}
    
    #Fjerner alle bookinger ved gitt personID
    df_booking_bad = df_booking_bad[df_booking_bad.personID != personID]
    df_booking_bad.to_csv("Booking_bad.csv", index=False)
    return {'melding':"Bookingene til " + navn + " har blitt fjernet", 'status':statuser['suksess']}

def skanne_bookinger_bad():
    
    #Setter normalverdier for om rommet ikke er i bruk
    normalverdiTempBad = '12'
    lysAv = '0'
    lysPaa = '1'
        
    #Leser inn alle bookinger
    df_booking_bad = pd.read_csv("Booking_bad.csv", dtype=str)
    df_booking_bad["tidspunktStart"] = pd.to_datetime(df_booking_bad["tidspunktStart"])
    df_booking_bad["tidspunktSlutt"] = pd.to_datetime(df_booking_bad["tidspunktSlutt"])
    
    #Brukes for å lagre evt beboere med booking
    personIDmedBooking = None
    
    #Ser etter aktive bookinger, og setter romsignalet deretter   
    for i in range(len(df_booking_bad)):
        if df_booking_bad["tidspunktStart"][i] < dt.now() and df_booking_bad["tidspunktSlutt"][i] > dt.now():
            personIDmedBooking = df_booking_bad["personID"].iloc[i]
            
            romSignal.bad(df_booking_bad["temperatur"].iloc[i], lysPaa)
    
    #Om det ikke er noen med booking settes rom til normalverdier
    if personIDmedBooking == None:
        romSignal.bad(normalverdiTempBad, lysAv)
    
    #Om en beboer har en aktiv booking her og er på soverommet, endres beboerens signal til å være på det aktuelle rommet
    #Om beboeren er i det aktuelle rommet og ikke lengre har en booking, endres signalet tilbake til å være på soverommet
    for key in cBeboere.beboere.keys():
        currentRoom = cBeboere.beboere[key].get_room()
        if currentRoom == '4' and key == personIDmedBooking:
            cBeboere.beboere[key].set_room('3')
        if currentRoom == '3' and not key == personIDmedBooking:
            cBeboere.beboere[key].set_room('4')
            