# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 01:50:35 2021

Disse funksjonene brukes for å lese og skrive til CoT. Det er lagt inn en pause på 0.5 sek for å dempe trykket på CoT sine servere.


@author: Jonas
"""

from datetime import timedelta as timedelta
from datetime import datetime as dt
from time import sleep
import requests
import json


#
def read_value(key, token):
    response = requests.get('https://circusofthings.com/ReadValue', {'Key':key, 'Token':token})
    response = json.loads(response.content)
    sleep(0.5)
    return response['Value']

def write_value(key, token, value):
    data = {'Key':key, 'Token':token, 'Value':value}
    requests.put('https://circusofthings.com/WriteValue', data = json.dumps(data),
                            headers= {'Content-Type': 'application/json'})
    sleep(0.5)
    
# def konsollsignal_dekoder(signal):
#     try:
#         personID = str(signal[0])
#         bookingTid = dt.strptime('2021'+signal[1:9], "%Y%m%d%H%M")
#         bookingVarighet = timedelta(minutes=int(signal[9:11]))
#         rom = str(signal[11])
#         ovntemperatur = str(signal[12:15])
#         bookingStatus = str(signal[15])
#         dekodetSignal = {'personID':personID, 'bookingTid':bookingTid, 'bookingVarighet':bookingVarighet, 
#                      'rom':rom, 'ovntemperatur':ovntemperatur, 'bookingStatus':bookingStatus}
        
#         return dekodetSignal
#     except:
#         #resetter strukturen på signalet
#         print("Feil struktur på signal til " + str(personID))
#         print(signal)
        
# def beboersignal_dekoder(signal):
    
#     try:
#         personID = str(signal[0])
#         rom = str(signal[1])
#         temperatur = str(signal[2:4])
#         gjester = int(signal[4])
#         dekodetSignal = {'personID':personID, 'rom':rom, 'temperatur':temperatur, 'gjester':gjester}
#         return dekodetSignal
#     except Exception as e:
#         #resetter strukturen på signalet
#         print("Error: {0}".format(e))
#         print(signal)
    
    