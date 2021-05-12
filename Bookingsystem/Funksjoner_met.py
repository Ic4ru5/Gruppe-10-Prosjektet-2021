# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:05:45 2021

@author: nygar
"""
import json
import requests
from metno_locationforecast import Place, Forecast


def getForecast():
    #Må brukes for å hente informasjon fra MET API
    USER_AGENT = "metno_locationforecast/1.0 sanderln@stud.ntnu.no"
    
    #Ønsket sted for værmelding, ved bruk av kooordinater
    Trondheim = Place("Trondheim", 63.435998, 10.427082, 15)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    
    #Oppretter en tom liste som skal brukes til å sortere 
    vaerMeldListe = []
    Trondheim_forecast.update()
    
    #Sjekker måling for nåtidens angitte timeintervall. f.eks. mellom 11:00 og 12:00
    vaerMeld = Trondheim_forecast.data.intervals[2]
    temp = vaerMeld.variables["air_temperature"]
    temp= int(round(temp.value,0))
    skydekk = vaerMeld.variables["cloud_area_fraction"]
    skydekk= int(round(skydekk.value,0))

    #Trenger kun temperatur og skydekkeprosenten fra værmeldingen.
    #Koden sorterer og henter ut nødvendig informasjon
    #Oppretter en tom liste som skal brukes til å legge inn verdiene for temperatur og skydekke.
    vaerMeldListe = []
    
    #For-løkka skal oppdatere lista for hver måling
    #Bruker pop til å luke ut verdiene som tidligere lå inne i lista
    for i in vaerMeldListe:
        # skriver samme linje to ganger da det blir den samme indeksen som fjernes
        vaerMeldListe.pop(0)
        vaerMeldListe.pop(0)
        
    #Legger til seneste verdier for temperatur og skydekke
    #Må ta høyde for at tallveriden kan endres mellom en og to og tre siffer --> hvordan?
    vaerMeldListe.append(temp)
    vaerMeldListe.append(skydekk)
    
    #Konverterer 
    temp = str(vaerMeldListe[0]).zfill(2) 
    skyDekk = str(vaerMeldListe[1]).zfill(3)
            
    #Formatterer signalverdi 
    #Tenkt format: 1xxxxx (1-tallet er bare det som start tall da CoT ikke tillater ledende null)
    #Konkatinerer tre strenger til ønsket signalformat
    signal = ("1" + temp + skyDekk)
    
    #Skriver resultatet i riktig format til Cot 
    token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0"
    key = "5917" 
    data = {'Key':key, 'Value':signal, 'Token':token}
    requests.put('https://circusofthings.com/WriteValue',
                            data = json.dumps(data),
                            headers = {'Content-Type': 'application/json'})
    return
