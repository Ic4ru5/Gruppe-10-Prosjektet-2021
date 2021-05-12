# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 23:57:08 2021

Denne koden ligger ikke i programmet som kjøres hele tiden. Men kjøres for hver gang man vil legge til, eller fjerne noen fra kollektivet.
Tanken er at man må bruke sentralenhet direkte for å legge til, eller fjerne beboere.

@author: Jonas
"""

from pandas import pandas as pd

import Funksjoner_cot as cot

def legg_til_beboer():
    
    #Ber ny beboer om å fylle inn nødvendig data for å være del av smartkollektivet
    
    #Leser inn eksisterende beboere
    df_beboere = pd.read_csv("Beboere.csv")
    
    #Er kollektivet fullt får en baskjed om det
    if len(df_beboere.index) >= 5:
        return "Kollektivet er fullt, fjern en beboer for å legge til flere"
    
    #Den første beboeren får ID = 1
    if len(df_beboere.index) <= 0:
        personID = 1
    else:
        #Påfølgende personer får et nummer høyere
        personID = df_beboere["personID"].sort_values().iloc[-1] + 1
    
    #Ber om CoT-info
    cotKeyBeboer = input("CoT-nøkkel for beboersignal: ")
    cotKeyKonsoll = input("CoT-nøkkel for personelig konsoll: ")
    cotToken = input("Personelig CoT-token: ")
    
    navn = input("Ditt navn: ")
    #Sjekker om navn er opptatt
    if navn in df_beboere["navn"].to_string():
        return "Valgt navn er opptatt"
    
    alder = input("Din alder: ")
    temperatur = input("Foretrukne romtemperatur (kan endre i konsoll): ")
    rom = int(input("Ditt romnummer: "))
    #Sjekker om rom er opptatt
    if rom in df_beboere["rom"].astype(int):
        return "Valgt rom er opptatt"
    if rom < 1 or rom > 5:
        return "Velg et romnummer mellom 1 - 5"
    
    
    #Legger til ny beboer
    df_ny_beboer = pd.DataFrame([[personID,cotKeyBeboer,cotKeyKonsoll,cotToken,navn,alder,rom]], columns=df_beboere.keys())  
    df_beboere = df_beboere.append(df_ny_beboer, ignore_index=True)
    df_beboere.to_csv("Beboere.csv", index=False)
    
    #Oppretter riktig format på CoT-signaler
    beboerValue = str(personID)+'0'+temperatur+'0'
    cot.write_value(cotKeyBeboer, cotToken, beboerValue)
    konsollValue = str(personID)+'010100000000000'
    cot.write_value(cotKeyKonsoll, cotToken, konsollValue)
    
    return "Gratulerer " + navn + ", du har blitt lagt til som ny beboer"
    
def fjern_beboer():
    
    #Leser inn eksisterende beboere
    df_beboere = pd.read_csv("Beboere.csv")
    
    #Spør om hvem som skal fjernes
    navn = str(input("Beboer som skal slettes: "))
    
    #Sjekker om beboer eksisterer
    if not navn in df_beboere["navn"].values:
        return "Ingen beboer ved navn " + navn
    
    #Fjerner alle beboere ved gitt navn
    #To beboere kan ikke ha samme navn, så det går bra å fjerne alle ved gitt navn
    df_beboere = df_beboere[df_beboere.navn != navn]
    df_beboere.to_csv("Beboere.csv", index=False)
    return navn + " har blitt fjernet som beboer"
    

# def signal(personID, rom=None, temperatur=None, gjester=None):
#     df_beboere = pd.read_csv("Beboere.csv", dtype=str)
#     df_beboer = df_beboere[df_beboere["personID"] == personID]
#     lestSignal = str(cot.read_value(df_beboer["cotKeyBeboer"].iloc[0], df_beboer["cotToken"].iloc[0]))
#     signal = personID
#     if not rom == None:
#         signal += rom
#     else:
#         signal += lestSignal[1]
#     if not temperatur == None:
#         signal += temperatur
#     else:
#         signal += lestSignal[2:4]
#     if not gjester == None:
#         signal += gjester
#     else:
#         signal += lestSignal[4]
        
#     cot.write_value(df_beboer["cotKeyBeboer"].iloc[0], df_beboer["cotToken"].iloc[0], signal)
    