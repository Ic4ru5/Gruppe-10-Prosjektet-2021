# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 22:57:35 2021

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

def book_stue(konsollsignal):
    
    #Laster inn bookinger som allerede ligger inne fra csv-fil.
    df_booking_stue = pd.read_csv("Booking_stue.csv", dtype=str)
    df_booking_stue["tidspunktStart"] = pd.to_datetime(df_booking_stue["tidspunktStart"])
    df_booking_stue["tidspunktSlutt"] = pd.to_datetime(df_booking_stue["tidspunktSlutt"])

    #Henter ut nødvendig data fra konsollsignalet
    personID = konsollsignal["personID"]
    dtStart = konsollsignal["bookingTid"]
    varighet = konsollsignal["bookingVarighet"]
    dtSlutt = dtStart + varighet
    
    #Beboerns ønskede temperatur ligger i beboersignalet. Den hentes gjennom instansen opprettet for gjeldene beboer
    temp = cBeboere.beboere[personID].get_temperatur()
    
    #Sjekker at booking ikke er i fortid
    if dtSlutt < dt.now():
        return {'melding':"Feil, velg en dato frem i tid", 'status':statuser['feil']}
    
    #Sjekker om ønsket tid overlapper med noen annens
    #For stuen er 3 overlapper tillatt
    overlappendeBookinger = 0
    for i in range(len(df_booking_stue)):
        #Ittererer seg gjennom bookinger, og teller antall overlapper
        if dtStart <= df_booking_stue["tidspunktSlutt"][i] and dtSlutt >= df_booking_stue["tidspunktStart"][i]:
            overlappendeBookinger += 1
            
        #Om antall overlapper er 3 eller mer blir en ny tid foreslått for booking
        if overlappendeBookinger >= 3:
            #Setter maks varighet for bookingforslag
            nyVarighet = '99'
            
            #Hvis det finnes en booking som starter etter denne, så regner programmet ut tid mellom bookingene
            #Om tiden mellom bookingene overstiger 99 min, kan ikke signalet sende et høyere tall som forslag til varighet
            try:
                tidMellomBookinger = df_booking_stue["tidspunktStart"][i+1] - df_booking_stue["tidspunktSlutt"][i]
                if (tidMellomBookinger <= timedelta(minutes=100)):
                    nyVarighet = "{0:0=2d}".format(int(tidMellomBookinger.seconds/60))
                    
            #Det finnes ingen senere booking, foreslår 99 minutter varighet automatisk        
            except:
                pass
            #Legger til et minutt for slutttiden er fortsatt opptatt
            #Og returnerer ny tid + status for bookingen
            nyttTidspunkt = df_booking_stue["tidspunktSlutt"][i] + timedelta(minutes=1)
            nyTid = nyttTidspunkt.strftime("%m%d%H%M") + nyVarighet
            return {'melding':"Feil, allerede booket", 'status':statuser['opptatt'], 'nyTid':nyTid}
    
    #Om programmet ikke finner 3 overlappende bookinger fortsetter den hit
    #Her blir ny booking lagt til i dataframen, og skrevet til csv-filen.
    #Funksjonen returnerer status for bookingen
    df_new_booking = pd.DataFrame([[personID,dtStart,dtSlutt,temp]], columns=df_booking_stue.keys())
    df_booking_stue = df_booking_stue.append(df_new_booking, ignore_index=True)
    df_booking_stue = df_booking_stue.sort_values(by=["tidspunktStart"])
    df_booking_stue.to_csv("Booking_stue.csv", index=False)
    return {'melding':"Suksess, din tid er nå booket", 'status':statuser['suksess']}

def kanseller_stue(konsollsignal):
    
    #Laster inn bookingene på stuen
    df_booking_stue = pd.read_csv("Booking_stue.csv", dtype=str)
    
    #Henter nødvendig data fra konsollsignal
    personID = konsollsignal["personID"]
    
    #Henter navnet til gjeldende beboer for å gi mer presis feilmelding. Praktisk for feilsøking.
    navn = cBeboere.beboere[personID].navn
    
    #Sjekker om beboer har eksisterende booking. Returnerer feilmelding om ikke.
    if personID not in df_booking_stue["personID"].values:
        return {'melding':"Ingen booking på " + navn, 'status':statuser['feil']}
    
    #Fjerner alle bookinger ved gitt personID
    df_booking_stue = df_booking_stue[df_booking_stue.personID != personID]
    df_booking_stue.to_csv("Booking_stue.csv", index=False)
    return {'melding':"Bookingene til " + navn + " har blitt fjernet", 'status':statuser['suksess']}

def skanne_bookinger_stue():
    
    #Setter normalverdier for om rommet ikke er i bruk
    normalverdiTempstue = '12'
    lysAv = '0'
    lysPaa = '1'
    
    #Leser inn alle bookinger
    df_booking_stue = pd.read_csv("Booking_stue.csv", dtype=str)
    df_booking_stue["tidspunktStart"] = pd.to_datetime(df_booking_stue["tidspunktStart"])
    df_booking_stue["tidspunktSlutt"] = pd.to_datetime(df_booking_stue["tidspunktSlutt"])
    df_booking_stue["temperatur"] = pd.to_numeric(df_booking_stue["temperatur"])
    
    #Lager en tom dataframe med samme kolonnenavn som "df__booking_stue"
    df_aktiveBookinger = pd.DataFrame(columns=df_booking_stue.keys())
    
    
    for i in range(len(df_booking_stue)):
        if df_booking_stue["tidspunktStart"][i] < dt.now() and df_booking_stue["tidspunktSlutt"][i] > dt.now():
            df_aktiveBookinger = df_aktiveBookinger.append(df_booking_stue.iloc[i])
            
    if len(df_aktiveBookinger) > 0:
        temp = str(int(df_aktiveBookinger["temperatur"].mean()))
        romSignal.stue(temp, lysPaa)
    else:
        romSignal.stue(normalverdiTempstue, lysAv)
    
    #Om en beboer har en aktiv booking her og er på soverommet, endres beboerens signal til å være på det aktuelle rommet
    #Om beboeren er i det aktuelle rommet og ikke lengre har en booking, endres signalet tilbake til å være på soverommet
    personIDmedBooking = df_aktiveBookinger["personID"].unique().tolist()
    for key in cBeboere.beboere.keys():
        currentRoom = cBeboere.beboere[key].get_room()
        if currentRoom == '4' and key in personIDmedBooking:
            cBeboere.beboere[key].set_room('1')
        if currentRoom == '1' and key not in personIDmedBooking:
            cBeboere.beboere[key].set_room('4')