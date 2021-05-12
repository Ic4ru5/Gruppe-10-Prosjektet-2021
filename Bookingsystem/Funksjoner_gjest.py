# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 00:10:19 2021

Funksjonene for de forskjellige bookingmulighetene er nok så like. En naturlig fremgangsmåte hadde derfor vært å kombinere disse til en funksjon.
Dette ble ikke gjort fordi alle funksjonene har alle sine små finurligheter som differere dem. Dette hadde gitt ca. samme mengde kode, men kombinert i samme 
funksjon med masse if-løkker. Syns derfor det er mye mer oversiktelig å dele de opp slik det er gjort nå.

@author: Jonas
"""

from datetime import timedelta as timedelta
from datetime import datetime as dt
from pandas import pandas as pd

import Klasse_beboer as cBeboere

#Forhåndsdefinerte tilbakemeldingsstatuser
#Globale fordi de brukes i alle funksjonene
statuser = {'suksess':3, 'opptatt':4, 'feil':5}

def book_gjest(signal):
    
    #Laster inn bookinger som allerede ligger inne fra csv-fil.
    df_booking_gjest = pd.read_csv("Booking_gjest.csv", dtype=str)
    df_booking_gjest["tidspunktStart"] = pd.to_datetime(df_booking_gjest["tidspunktStart"])
    df_booking_gjest["tidspunktSlutt"] = pd.to_datetime(df_booking_gjest["tidspunktSlutt"])

    #Henter ut nødvendig data fra konsollsignalet
    personID = signal["personID"]
    dtStart = signal["bookingTid"]
    varighet = signal["bookingVarighet"]
    dtSlutt = dtStart + varighet
    antallGjester = int(signal["ovntemperatur"])
    
    
    #Sjekker om datoen er ikke er fortid
    if dtSlutt < dt.now():
        return {'melding':"Feil, velg en dato frem i tid", 'status':statuser['feil']}
    
    #Sjekker om det bookes gjester innenfor 1 - 5 stk
    if antallGjester <= 0 or antallGjester > 5:
        return {'melding':"Feil, velg et gyldig antall gjester (1-5)", 'status':statuser['feil']}
    
    #Sjekker om ønsket tid overlapper med noen annens
    #Starter med antallet som skal bookes, og sjekker opp mot tidligere bookinger
    overlappendegjester = antallGjester 
    for i in range(len(df_booking_gjest)):
        if dtStart <= df_booking_gjest["tidspunktSlutt"][i] and dtSlutt >= df_booking_gjest["tidspunktStart"][i]:
            overlappendegjester += int(df_booking_gjest["antall"][i])
    
    #Om antall overlapper er 5 eller mer blir en ny tid foreslått for booking
    if overlappendegjester > 5:
        nyVarighet = '99'
        
        #Hvis det finnes en booking som starter etter denne, så regner programmet ut tid mellom bookingene
        #Om tiden mellom bookingene overstiger 99 min, kan ikke signalet sende et høyere tall som forslag til varighet
        try: 
            tidMellomBookinger = df_booking_gjest["tidspunktStart"][i+1] - df_booking_gjest["tidspunktSlutt"][i]
            if (tidMellomBookinger <= timedelta(minutes=100)):
                nyVarighet = "{0:0=2d}".format(int(tidMellomBookinger.seconds/60))
                
        #Det finnes ingen senere booking, foreslår 99 minutter varighet automatisk        
        except:
            pass
        #Legger til et minutt for slutttiden er fortsatt opptatt
        nyttTidspunkt = df_booking_gjest["tidspunktSlutt"][i] + timedelta(minutes=1)
        nyTid = nyttTidspunkt.strftime("%m%d%H%M") + nyVarighet
        return {'melding':"Feil, allerede booket", 'status':statuser['opptatt'], 'nyTid':nyTid}
    else:
        #Om ovelappende gjester ikke overstiger 5, så blir booking lagt til csv-fil
        # og returnere status
        df_new_booking = pd.DataFrame([[personID,antallGjester,dtStart,dtSlutt]], columns=df_booking_gjest.keys())
        df_booking_gjest = df_booking_gjest.append(df_new_booking, ignore_index=True)
        df_booking_gjest = df_booking_gjest.sort_values(by=["tidspunktStart"])
        df_booking_gjest.to_csv("Booking_gjest.csv", index=False)
        return {'melding':"Suksess, din tid er nå booket", 'status':statuser['suksess']}

def kanseller_gjest(signal):
    
    #Leser inn bookinger fra csv-fil
    df_booking_gjest = pd.read_csv("Booking_gjest.csv", dtype=str)
    
    #Henter nødvendig data fra innkommende signal
    personID = signal["personID"]
    navn = cBeboere.beboere[personID].navn
    
    #Sjekker om beboer har eksisterende booking
    if personID not in df_booking_gjest["personID"].values:
        return {'melding':"Ingen booking på " + navn, 'status':statuser['feil']}
    
    #Fjerner alle bookinger ved gitt personID
    df_booking_gjest = df_booking_gjest[df_booking_gjest.personID != personID]
    df_booking_gjest.to_csv("Booking_gjest.csv", index=False)
    return {'melding':"Bookingene til " + navn + " har blitt fjernet", 'status':statuser['suksess']}

def skanne_bookinger_gjest():
    
    #Leser inn alle bookinger
    df_booking_gjest = pd.read_csv("Booking_gjest.csv", dtype=str)
    df_booking_gjest["tidspunktStart"] = pd.to_datetime(df_booking_gjest["tidspunktStart"])
    df_booking_gjest["tidspunktSlutt"] = pd.to_datetime(df_booking_gjest["tidspunktSlutt"])
    
    #Leser inn beboerne i kollektivet, og lager en tom datafram til senere
    df_beboere = pd.read_csv("Beboere.csv", dtype=str)
    df_aktiveBookinger = pd.DataFrame()
    
    #Ser etter bookinger som er aktive nå
    for i in range(len(df_booking_gjest)):
        if df_booking_gjest["tidspunktStart"][i] < dt.now() and df_booking_gjest["tidspunktSlutt"][i] > dt.now():
            df_aktiveBookinger = df_aktiveBookinger.append(df_booking_gjest.iloc[i])
    
    #Endrer beboersignal til å ha riktig antall gjester på hver enkelt beboer
    if len(df_aktiveBookinger) > 0:
        personIDmedBooking = df_aktiveBookinger["personID"].unique()
        df_personIDutenBooking = df_beboere.loc[~df_beboere["personID"].isin(personIDmedBooking)]
        for i in range(len(personIDmedBooking)):
            personID = personIDmedBooking[i]
            antallGjester = 0
            for j in range(len(df_aktiveBookinger)):
                antallGjester += int(df_aktiveBookinger["antall"].iloc[j])
            cBeboere.beboere[personID].set_guest(str(antallGjester))
        
        for i in range(len(df_personIDutenBooking)):
            personID = df_personIDutenBooking["personID"].iloc[i]
            antallGjester = 0
            cBeboere.beboere[personID].set_guest(str(antallGjester))
    else:
        #Setter alle sin gjestestatus til null
        for i in range(len(df_beboere)):
            personID = df_beboere["personID"].iloc[i]
            antallGjester = 0
            cBeboere.beboere[personID].set_guest(str(antallGjester))