#recuperation des informations du publisher (l'altitude) a travers le serveur mqtt
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(17,GPIO.OUT)
Servo_Moteur = GPIO.PWM(17,50) # le PWM est dans le port 17, frequence=50

#si on perd la connexion l'abonnement va se renouveler automatiquement
def on_connect(client, userdata, flags, rc):
    print("Connexion "+str(rc))
    client.subscribe("Informations")#souscription au canal Informations 
#exploitation des informations recues pour commander le moteur
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if float(msg.payload) >= -34.00: # definir la condition sur l'altitude
        Servo_Moteur.start(0)
        Servo_Moteur.ChangeDutyCycle(2+(160/18))
        print("the altitude is higher than -34")
        time.sleep(0.2)
        Servo_Moteur.ChangeDutyCycle(0)
        
    else :
        print("the altitude is lower than -34")
        Servo_Moteur.start(0)
        Servo_Moteur.ChangeDutyCycle(2)
        time.sleep(0.2)
        Servo_Moteur.ChangeDutyCycle(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mojito.homedruon.com", 1883, 60)
client.loop_forever()
GPIO.cleanup()
