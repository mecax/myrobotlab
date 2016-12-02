import random
import codecs
import socket
import sys
from java.lang import String
import urllib2
import random
import threading
import io
import itertools
import random
import time
from time import sleep
import textwrap
import codecs
import socket
import os
import shutil
import hashlib
import subprocess
import json
import time
import csv
import feedparser
import re
#import xml.dom.minidom
#from xml.dom.minidom import Node
#import xml.etree.ElementTree  #parser xml
from datetime import datetime
from subprocess import Popen, PIPE
from org.myrobotlab.service import Servo





#check runing folder
oridir=os.getcwd().replace("\\", "/")+"/"

#fix programab aimlif problems : remove all aimlif files
#print oridir+'ProgramAB/bots/'+myAimlFolder+'/aimlif'
try:
	shutil.rmtree(oridir+'ProgramAB/bots/steve/aimlif')
except: 
	pass


execfile(u'config.py')
execfile(u'opencv.py')
execfile(u'wikiDataFetcher.py')
execfile(u'traduction.py')
execfile(u'news.py')

query = "suisse"

#demmarage des services
ardu1 = Runtime.start("arduino1","Arduino")
servo01 = Runtime.start("servo01","Servo")
opencv = Runtime.start("opencv","OpenCV")
python = Runtime.start("python","Python")

chatBot = Runtime.createAndStart("chatBot", "ProgramAB")
ear = Runtime.createAndStart("ear", "WebkitSpeechRecognition")
mouth=Runtime.createAndStart("mouth", "AcapelaSpeech")
htmlFilter=Runtime.createAndStart("htmlFilter","HtmlFilter")
webgui = Runtime.create("WebGui","WebGui")
wdf=Runtime.createAndStart("wdf", "WikiDataFetcher") # WikiDataFetcher cherche des données sur les sites wiki




pid = Runtime.createAndStart("pid","Pid")
pid.setPID("x",0.1, 0, 0.1)
pid.setMode("x",1)
pid.setOutputRange("x",-2, 2)
pid.setControllerDirection("x",0)
pid.setSetpoint("x",70)




wdf.setLanguage("fr") # on cherche en français
wdf.setWebSite("frwiki") # On fait des recherches sur le site français de wikidata

sleep(0.5)

ear.setLanguage("fr-FR")
mouth.setLanguage("FR") # on parle francais !
mouth.setVoice(Voice) # on choisis une voix ( voir la liste des voix sur http://www.acapela-group.com/?lang=fr
 
chatBot.startSession("ProgramAB","Defaut","steve")

sleep(0.5)
 
ear.addTextListener(chatBot) # On creer une liaison de webKitSpeechRecognition vers Program AB
chatBot.addTextListener(htmlFilter) # On creer une liaison de Program AB vers html filter
htmlFilter.addTextListener(mouth) # On creer une liaison de htmlfilter vers mouth


 
def onStartSpeaking(text):
	ear.stopListening()
	print "Start Speaking"
 
def onEndSpeaking(text): 
	ear.startListening()
	print "Stop speaking"

webgui.autoStartBrowser(False)
webgui.startService()

sleep(1)
webgui.startBrowser("http://localhost:8888/#/service/ear")

 


#start arduino

ardu1.connect("COM3")



#start servo
servo01.setMinMax(20,170)
servo01.attach(ardu1.getName(),servoPin)
servo01.setRest(100)
servo01.setSpeed(0.5)
sleep(1)
mouth.speakBlocking("reset servo")
servo01.rest()
sleep(1)
servo01.setSpeed(1)
mouth.speakBlocking(u"reset servo terminé")











 
# add python as a listener to OpenCV data
# this tells the framework - whenever opencv.publishOpenCVData is invoked
# python.onOpenCVData will get called
python.subscribe("opencv", "publishOpenCVData")
python.subscribe("mouth", "publishEndSpeaking")
python.subscribe("mouth", "publishStartSpeaking") 

  

#mouth.speakBlocking("salut! bienvenu dans ce programme de test.")


#opencv.addFilter("PyramidDown")
#opencv.addFilter("Gray")
#opencv.addFilter("FaceDetect")
#opencv.setDisplayFilter("FaceDetect")
sleep(2)
mouth.speakBlocking(u"fin de l'initialisation")





#fr=opencv.addFilter("FaceRecognizer")
#opencv.setDisplayFilter("FaceRecognizer")
#sleep(5)
#fr.train()# it takes some time to train and be able to recognize face
#sleep(4)
#opencv.removeFilters()
#opencv.stopCapture()





def setModeVision(data) :
	global MODEVIDEO 
	if data==1 :
		MODEVIDEO = 1
		opencv.capture()
	if data==0 :
		MODEVIDEO = 10
		


