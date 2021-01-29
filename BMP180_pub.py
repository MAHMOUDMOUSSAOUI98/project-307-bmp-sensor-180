#Affichage de la temperature,pression et altitude mesurees par le BMP180, publication des valeurs des altitudes dans le canal "Information"

import bmpsensor
import paho.mqtt.client as paho
import time
import math

 
client= paho.Client()

if client.connect("mojito.homedruon.com",1883,60)!=0:
    print("reessayer !!")
    
    
while True:
    T, P, A = bmpsensor.readBmp180() %recuperation des donnees du capteur a partir du fichier bmpsensor
    print(" Temperature : ",T)  # Temperature en degree
    print("Pression : ",P*pow(10,-5)) #Pression en bar
    print("Altitude : \n",A) # Altitude in meters

    client.publish("Informations",A,0) # la publication des altitudes 
    time.sleep(0.5)
    
client.disconnect()