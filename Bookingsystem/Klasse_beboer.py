# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 23:13:08 2021

Ved å bruke klasse for beboerne ble programmet komprimert betraktelig. I starten ble listen med beboere lest inn hver gang noe skulle gjøres.
Nå leses den inn i starten av programmet, og holder på verdiene som trengs i instanser/objekter av klassen Bebeoere. Som er mye lettere å nå.

@author: Jonas
"""
from datetime import timedelta as timedelta
from datetime import datetime as dt
from pandas import pandas as pd

import Funksjoner_cot as cot


class Beboere:
    
    #Ved oppstart lages instansene ved hjelp av denne funksjonen
    def __init__(self, personID, cotKeyBeboer, cotKeyKonsoll, cotToken, navn, alder, rom):
        self.personID = personID
        self.cotKeyBeboer = cotKeyBeboer
        self.cotKeyKonsoll = cotKeyKonsoll
        self.cotToken = cotToken
        self.navn = navn
        self.rom = rom
    
    #Bruker sine egne funksjoner for å hente spesifikke verdier
    def get_temperatur(self):
        signal = self.get_beboerSignal()
        return signal["temperatur"]
    def set_temperatur(self, temperatur):
        self.set_beboerSignal(temperatur=temperatur)
        
        
    #Bruker sine egne funksjoner for å hente spesifikke verdier
    def get_room(self):
        signal = self.get_beboerSignal()
        return signal["rom"]
    def set_room(self, rom):
        self.set_beboerSignal(rom=rom)
        
    
    #Bruker sine egne funksjoner for å hente spesifikke verdier
    def get_guest(self):
        signal = self.get_beboerSignal()
        return signal["gjester"]
    def set_guest(self, antallGjester):
        self.set_beboerSignal(gjester=antallGjester)
        
    #Noen ganger ønsker programmet å hente u-dekodet signal, har derfor en egen funksjon for dette
    def get_konsollSignal_raw(self):
        signal_raw = str(cot.read_value(self.cotKeyKonsoll, self.cotToken))
        return signal_raw
    #Henter singalet fra CoT, for så å dekode det
    def get_konsollSignal(self):
        signal_raw = str(cot.read_value(self.cotKeyKonsoll, self.cotToken))
        try:
            personID = str(signal_raw[0])
            bookingTid = dt.strptime('2021'+signal_raw[1:9], "%Y%m%d%H%M")
            bookingVarighet = timedelta(minutes=int(signal_raw[9:11]))
            rom = str(signal_raw[11])
            ovntemperatur = str(signal_raw[12:15])
            bookingStatus = str(signal_raw[15])
            dekodetSignal = {'personID':personID, 'bookingTid':bookingTid, 'bookingVarighet':bookingVarighet, 
                         'rom':rom, 'ovntemperatur':ovntemperatur, 'bookingStatus':bookingStatus}
            return dekodetSignal
        except Exception as e:
            #resetter strukturen på signalet
            print("Error: {0}".format(e))
            print(signal_raw)
            resattStruktur = self.personID + '010112000010005'
            self.set_konsollSignal_raw(resattStruktur)
            return
    #Setter konsollsignalet til ønsket verdi, f.eks. ved respons på booking
    def set_konsollSignal_raw(self, signalRaw):
        cot.write_value(self.cotKeyKonsoll, self.cotToken, signalRaw)
        
    #Noen ganger ønsker programmet å hente u-dekodet signal, har derfor en egen funksjon for dette
    def get_beboerSignal_raw(self):
        signal_raw = str(cot.read_value(self.cotKeyBeboer, self.cotToken))
        return signal_raw
    #Henter singalet fra CoT, for så å dekode det
    def get_beboerSignal(self):
        signal_raw = str(cot.read_value(self.cotKeyBeboer, self.cotToken))
        try:
            personID = str(signal_raw[0])
            rom = str(signal_raw[1])
            temperatur = str(signal_raw[2:4])
            gjester = int(signal_raw[4])
            dekodetSignal = {'personID':personID, 'rom':rom, 'temperatur':temperatur, 'gjester':gjester}
            return dekodetSignal
        except Exception as e:
            #resetter strukturen på signalet
            print("Error: {0}".format(e))
            print(signal_raw)
            resattStruktur = {'rom':'4', 'temperatur':'12', 'gjester':'0'}
            self.set_beboerSignal_raw(resattStruktur)
            return resattStruktur
    
    #Setter konsollsignalet til ønsket verdi, f.eks. ved respons på booking
    def set_beboerSignal_raw(self, verdiRaw):
        signal = self.personID + verdiRaw['rom'] + verdiRaw['temperatur'] + verdiRaw['gjester']   
        cot.write_value(self.cotKeyBeboer, self.cotToken, signal)
    #Om programmet ønsker å endre kun noen verdier i signalet kan dette gjøres gjennom denne funksjonen
    def set_beboerSignal(self, rom=None, temperatur=None, gjester=None):
        lestSignal = self.get_beboerSignal()
        signal = self.personID
        if not rom == None:
            signal += rom
        else:
            signal += str(lestSignal["rom"])
        if not temperatur == None:
            signal += temperatur
        else:
            signal += str(lestSignal["temperatur"])
        if not gjester == None:
            signal += gjester
        else:
            signal += str(lestSignal["gjester"])
            
        cot.write_value(self.cotKeyBeboer, self.cotToken, signal)
    
    
    # def kill
def les_inn_beboere():    
    df_beboere = pd.read_csv("Beboere.csv", dtype=str)
    
    global beboere
    beboere = {}
    for index, beboer in df_beboere.iterrows():
        navn = beboer["navn"]
        personID = beboer["personID"]
        cotKeyBeboer = beboer["cotKeyBeboer"]
        cotKeyKonsoll = beboer["cotKeyKonsoll"]
        cotToken = beboer["cotToken"]
        alder = beboer["alder"]
        rom = beboer["rom"]
        beboere.update({personID: Beboere(personID, cotKeyBeboer, cotKeyKonsoll, cotToken, navn, alder, rom)})