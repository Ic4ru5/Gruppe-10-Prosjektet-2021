# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:47:00 2021

@author: nygar
"""
import requests
import json
from pysolar import solar
import datetime 

def wHgenerertfunct(sekunder, nullstill):

    """Leser værmelding-signal fra CoT"""
                                     
    key1 = '5917'
    token1 = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0'
    
    les = requests.get('https://circusofthings.com/ReadValue', params = {'Key':key1, 'Token':token1})
    verdi = json.loads(les.content)
     
    ## Værmeldingen inneholder temperatur og skydekkeprosent: eks.format: 105020 ->05 grader og 20% skydekke.
    vaermeld = verdi['Value']
     
    ## Henter ut verdier fra signalet. Datatypen til signalet er int, og må konverteres til string for å 
    ## hente ut indekserte verdier. For å kunne bruke dem videre konverteres dem tilbake til int.
    skydekke = str(vaermeld)
    uteTemp = str(vaermeld)
     
    skydekke = (skydekke[3:6])
    uteTemp = (uteTemp[1:3])
     
    skydekke = int(skydekke)
    uteTemp = int(uteTemp)
    
    """Leser total-effekt-produsert signal fra CoT"""                                
    key2 = '32630'
    token2 = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4'
    
    les = requests.get('https://circusofthings.com/ReadValue', params = {'Key':key2, 'Token':token2})
    verdi = json.loads(les.content)
     
    ## Må hente denne verdien for å kunne summere total effekt generert.
    ## Mulighet for nullstilling
    effektProdusert = verdi['Value']
    if (nullstill == 1):
        effektProdusert = 0

     
    """Solcellepanel - totaleffekt i wH generert av solcellepanel basert på stråling,solprosent, areal, moduleffektivitet og ytelsesforhold"""
    # Posisjon for solvinkel og tidspunkt.
    ## Importerer biblioteket * fra pysolar. Installeres i anaconda promten ved pip3 install pysolar.
    ## Bruker bibliteket til finne strålingstyrke og vinkel til solen. 
    ### Antar at solcellepanelet ligger statisk på et flatt tak til en hver tid.
    breddegrad = 63.435998
    lengdegrad = 10.427082
    dato = datetime.datetime.now(datetime.timezone.utc)
    solvinkel = solar.get_altitude(breddegrad, lengdegrad, dato)
     
    # Ved manuel input av stråling kan disse solvinkelkoeffisientene(sVK1,sVK2) brukes som en forholdsprosent. 
    ## Ved optimalt forhold er solvinkel lik 90 grader og det tilsvarer 100%. 
    ## Dersom solvinkel<=90 brukes sVK1, dersom solvinkel>90 brukes sVK2.
    ## sVK2 = 2- sVK1, der 2=180grader
    #KODE: sVK1 = solvinkel/90
    #KODE: sVK2 = 2 - solvinkel/90
     
    # Temperaturforhold
    ## Solcellepanelet opptrer optimalt under enkelte forhold.
    ## Definerer temperaturvariabel som bruker optimal temperatur som referanse.
    ## For hver grad over- eller under optimal temperatur (25 grader), vil ytelsen synke med 0,4%.
    tempKoef = 0.996
    tempOptimal = 25
    ytelseTemp = abs((uteTemp-tempOptimal)*tempKoef)/100
     
    # Variabler som brukes i regnestykket for effekten som produseres.
    ## Stråling finnes ved hjelp av tidspunkt og solvinkel
    ## Bruker solprosent som en variabel for hvor mye stråling som treffer panelet. Prosenten baseres på skydekkprosenten.
    ## Kollektivets takareal er 70 kvm. Vi vurderer 40 kvm som utnyttbart.
    ## solcellepanelet har en modul effektivitet på 17,7%, kun 17,7% av strålingen kan generes til brukende strøm under optimale forhold.
    ## Antar en ytelsesprosent. Biblioteket tar ikke høyde for utetemperatur eller hvor mye skyer det er. 
    straaling =  solar.radiation.get_radiation_direct(dato, solvinkel)
    solProsent = 1-(skydekke/100)
    solcellerAreal = 40
    modulEffektivitet = 0.177
    ytelsesForhold = solProsent+ytelseTemp
     
    # Verdien for hver kjøring.
    ## Enheter: [wh]=[m^2]*[%]*[w/m^2]*[%]*[h].
    ## Mulighet for nullstilling.
    effekt = solcellerAreal*modulEffektivitet*straaling*ytelsesForhold*(sekunder/3600)
    if(nullstill==1):
        effekt = 0
    
    
    # Summerer verdien som er lagret i CoT med verdien som akkumuleres den nåværende timen
    # Mulighet for nullstilling
    totalEffektProdusert = effektProdusert + effekt
    if (nullstill == 1):
        totalEffektProdusert = 0
    
    # Hvis prgrammet nullstilles (def(Arg1,Arg2=1)), skal det arg2 automatisk skiftes til 0
    if(effekt==0):
        if(effektProdusert==0):
            if(totalEffektProdusert==0):
                nullstill=0
      
    """Skriver ny verdi til total-effekt-produsert-signal i CoT"""
    token2 = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4"
    key2 = "32630" 
    data = {'Key':key2, 'Value':totalEffektProdusert, 'Token':token2}
    requests.put('https://circusofthings.com/WriteValue',
                 data = json.dumps(data),
                 headers = {'Content-Type': 'application/json'})
    
    # print("Hadde: " + str(effektProdusert) + " wH")
    # print("Legger til: " + str(effekt) + " wH")
    # print("Solpanelet har generet: " + str(totalEffektProdusert) + " wH")
        
    return
