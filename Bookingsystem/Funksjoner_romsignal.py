# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 19:09:04 2021

Brukes hovedsakelig for å holde styr på rommenes keys og tokens på ett sted.

@author: Jonas
"""

import Funksjoner_cot as cot

cotKey = {'bad':'3657', 'stue':'4028', 'kjokken':'23658'}
cotToken = {'bad':'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4',
            'stue':'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4',
            'kjokken':'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4'}


#Disse funksjonene brukes for å endre romsignalene
def bad(temperatur, lys):
    value = temperatur + lys
    cot.write_value(cotKey["bad"], cotToken["bad"], value)
    
def stue(temperatur, lys):
    value = temperatur + lys
    cot.write_value(cotKey["stue"], cotToken["stue"], value)
    
def kjokken(temperatur, ovnTemp, lys):
    value = temperatur + ovnTemp + lys
    cot.write_value(cotKey["kjokken"], cotToken["kjokken"], value)
    
def soverom(romnr, temperatur, lys):
    value = romnr + temperatur + lys
    cot.write_value(cotKey["sov"], cotToken["sov"], value)