import pandas as pd
import pygame
import os
import time
import random
import subprocess
import signal
import threading
import playMusic
import sys
import broadcastDisplay
from broadcastDisplay import mainTitle, troubleTitle, pulseRed, pulseOrange, pulseWhite, pulseYellow, pulseGreen, pulseBlue, sparkleRed, whiteFlagOuter, redFlagOuter, orangeFlagOuter, blueFlagOuter, greenFlagOuter, yellowFlagOuter, setHit, getHit, refresh, showStop, stopbutton, redFlagLeftOrig, orangeFlagLeftOrig, whiteFlagLeftOrig, yellowFlagLeftOrig, greenFlagLeftOrig, blueFlagLeftOrig, setRedFlagSame, setOrangeFlagSame, setWhiteFlagSame, setGreenFlagSame, setBlueFlagSame, setYellowFlagSame
from funAudio import welcomeMessage
import paho.mqtt.client as mqtt
from games import startTargetGame, startKnockOutGame, startCaptureGame, askReady, startPopupGame
#sys.path.append('/Users/s1034274/Desktop/globals/')
sys.path.append('/home/pi/Desktop/globals/')

from constants import monHipHop, tuesRock, wedWayBack, thursThrowback, fridayHits, satDisco, sunCountry, numSongs, numStations, holiday, michealJ, yacht


mix = pygame.Rect(10, 10, 99, 39)
lights = pygame.Rect(115, 10, 99, 39)
games = pygame.Rect(220, 10, 99, 39)
control = pygame.Rect(325, 10, 109, 39)

red = (255,0,0)
orange = (255,128,0)
blue = (0,0,255)
yellow = (255,255,0)
green = (0,255,0)
white = (255,255,255)
darkred = (255/2,0,0)
darkorange = (255/2,128/2,0)
darkblue = (0,0,255/2)
darkyellow = (255/2,255/2,0)
darkgreen = (0,255/2,0)
grey = (128,128,128)
black = (0,0,0)
pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)
screen = pygame.display.set_mode((750, 550))
clock = pygame.time.Clock()
pygame.display.set_caption("Main Menu")
state = 0

mixText = font.render('MIX', True, black)
lightsText = font.render('Lights', True, black)
gamesText = font.render('Games', True, black)
controlText = font.render('Control', True, black)

# Load the main Menu
def main():
    while True:
        
        screen.fill([0,0,0])
        
        for event in pygame.event.get():
            
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                checkEventMain(mouse_pos)

        if (state == 1):
            lightsOptions()
        # elif (state == 2):
            
        elif (state == 3):
            gameOptions()
        elif (state == 4):
            controlOptions()
        troubleShootOptions()
        lightUpdate()
        
            

        pygame.display.flip()
        
        clock.tick(60)


songName = font.render('Hit Me', True, white)
song = 1

endButton = pygame.Rect(10, 230, 99, 39)
endText = font.render('Shutdown', True, black)
sendButton = pygame.Rect(330, 410, 99, 39)
sendText = font.render('Send', True, black)
sendAllButton = pygame.Rect(330, 450, 99, 39)
sendAllText = font.render('Send All', True, black)

pastSong = pygame.Rect(115, 130, 45, 39)
pastSongText = font.render('<-', True, black)
nextSong = pygame.Rect(170, 130, 45, 39)
nextSongText = font.render('->', True, black)
playButton = pygame.Rect(115, 170, 100, 39)
playButtonText = font.render('Play', True, black)

pandoraButton = pygame.Rect(115, 210, 100, 39)
pandoraButtonText = font.render('Pandora', True, black)

stationText = font.render('Top 40', True, white)
station = 1
playStation = 4

pastStation = pygame.Rect(115, 290, 45, 39)
pastStationText = font.render('<-', True, black)
nextStation = pygame.Rect(170, 290, 45, 39)
nextStationText = font.render('->', True, black)

periodTitleText = font.render('Period', True, white)
periodButton = pygame.Rect(115, 370, 100, 39)
periodText = font.render('11 mins', True, black)
period = 11
playBoth = pygame.Rect(115, 410, 100, 39)
playBothText = font.render('Both', True, black)

monday = pygame.Rect(450, 50, 140, 39)
mondayText = font.render('Monday', True, black)
tuesday = pygame.Rect(450, 90, 140, 39)
tuesdayText = font.render('Tuesday', True, black)
wednesday = pygame.Rect(450, 130, 140, 39)
wednesdayText = font.render('Wednesday', True, black)
thursday = pygame.Rect(450, 170, 140, 39)
thursdayText = font.render('Thursday', True, black)
friday = pygame.Rect(450, 210, 140, 39)
fridayText = font.render('Friday', True, black)
saturday = pygame.Rect(450, 250, 140, 39)
saturdayText = font.render('Saturday', True, black)
sunday = pygame.Rect(450, 290, 140, 39)
sundayText = font.render('Sunday', True, black)

restartText = font.render('Restart', True, black)
restartRed = pygame.Rect(440, 130, 70, 20)
restartOrange = pygame.Rect(440, 200, 70, 20)
restartWhite = pygame.Rect(440, 270, 70, 20)
restartYellow = pygame.Rect(440, 340, 70, 20)
restartGreen = pygame.Rect(440, 410, 70, 20)
restartBlue = pygame.Rect(440, 480, 70, 20)
restartAll = pygame.Rect(440, 520, 70, 20)
restartAllText = font.render('Restart All', True, black)

def troubleShootOptions():
    pygame.draw.rect(screen, white, restartAll)  # draw button
    screen.blit(restartAllText, restartAll)
    pygame.draw.rect(screen, white, restartRed)  # draw button
    screen.blit(restartText, restartRed)
    pygame.draw.rect(screen, white, restartOrange)  # draw button
    screen.blit(restartText, restartOrange)
    pygame.draw.rect(screen, white, restartWhite)  # draw button
    screen.blit(restartText, restartWhite)
    pygame.draw.rect(screen, white, restartGreen)  # draw button
    screen.blit(restartText, restartGreen)
    pygame.draw.rect(screen, white, restartYellow)  # draw button
    screen.blit(restartText, restartYellow)
    pygame.draw.rect(screen, white, restartBlue)  # draw button
    screen.blit(restartText, restartBlue)
    


def lightUpdate():
    broadcastDisplay.setRedFlag(red, red, red, redFlagOuter)
    broadcastDisplay.setOrangeFlag(orange, orange, orange, orangeFlagOuter)
    broadcastDisplay.setWhiteFlag(white, white, white, whiteFlagOuter)
    broadcastDisplay.setGreenFlag(green, green, green, greenFlagOuter)
    broadcastDisplay.setYellowFlag(yellow, yellow, yellow, yellowFlagOuter)
    broadcastDisplay.setBlueFlag(blue, blue, blue, blueFlagOuter)
    pygame.draw.rect(screen, white, mix)  # draw button
    pygame.draw.rect(screen, white, lights)  # draw button
    pygame.draw.rect(screen, white, games)  # draw button
    pygame.draw.rect(screen, white, control)  # draw button
    screen.blit(mixText, mix)
    screen.blit(lightsText, lights)
    screen.blit(gamesText, games)
    screen.blit(controlText, control)
    pygame.draw.rect(screen, white, endButton)  # draw button
    screen.blit(endText, endButton)
    pygame.draw.rect(screen, white, welcomeButton)  # draw button
    screen.blit(welcomeText, welcomeButton)
    pygame.draw.rect(screen, white, testButton)  # draw button
    screen.blit(testText, testButton)

    pygame.draw.rect(screen, white, startButton)  # draw button
    screen.blit(startText, startButton)
    pygame.draw.rect(screen, white, stopButton)  # draw button
    screen.blit(stopText, stopButton)

def lightsOptions():
    global songName, stationText, song, station, period, periodText, playStation
    if (song == 1):
        songName = font.render('Serious', True, white)
    elif (song == 2):
        songName = font.render('Thunderstruck', True, white)
    elif (song == 3):
        songName = font.render('Part.Rok', True, white)
    elif (song == 4):
        songName = font.render('Hit Me', True, white)
    elif (song == 5):
        songName = font.render('Enter S', True, white)
    elif (song == 6):
        songName = font.render('Beat It', True, white)
    elif (song == 7):
        songName = font.render('Lil bit', True, white)
    elif (song == 8):
        songName = font.render('Beggin', True, white)
    elif (song == 9):
        songName = font.render('Yeah!', True, white)
    elif (song == 10):
        songName = font.render('Uptown', True, white)
    elif (song == 11):
        songName = font.render('AOK', True, white)
    elif (song == 12):
        songName = font.render('Sing.Lad', True, white) #Mon. Mash or Sing.Lad
    elif (song == 13):
        songName = font.render('I.L.Rok', True, white) # Thrller or I.L.Rok
    elif (song == 14):
        songName = font.render('Edemame', True, white) #Halloween or Edemame
    elif (song == 15):
        songName = font.render('Squid', True, white)
    elif (song == 16):
        songName = font.render('immabe', True, white)
    elif (song == 17):
        songName = font.render('Sheesh!', True, white) # DeckThe or Sheesh!
    elif (song == 18):
        songName = font.render('ChittyB.', True, white) # Jin.Roc or ChittyBang
    elif (song == 19):
        songName = font.render('ENEMY', True, white) # mele.k or ENEMY
    elif (song == 20):
        songName = font.render('Motto', True, white) # 12days or motto
    
    if (station == 1):
        stationText = font.render('Hip Hop', True, white)
        playStation = monHipHop
    elif (station == 2):
        stationText = font.render('Rock', True, white)
        playStation = tuesRock
    elif (station == 3):
        stationText = font.render('Way Back', True, white)
        playStation = wedWayBack
    elif (station == 4):
        stationText = font.render('Throwback', True, white)
        playStation = thursThrowback
    elif (station == 5):
        stationText = font.render('Top Hits', True, white)
        playStation = fridayHits
    elif (station == 6):
        stationText = font.render('Disco', True, white)
        playStation = satDisco
    elif (station == 7):
        stationText = font.render('Country', True, white)
        playStation = sunCountry
    elif (station == 8):
        stationText = font.render('Holiday', True, white)
        playStation = holiday
    elif (station == 9):
        stationText = font.render('Yacht Rock', True, white)
        playStation = yacht
    elif (station == 10):
        stationText = font.render('Micheal J', True, white)
        playStation = michealJ

    pygame.draw.rect(screen, white, pastSong)  # draw button
    pygame.draw.rect(screen, white, nextSong)  # draw button
    pygame.draw.rect(screen, white, playButton)  # draw button
    pygame.draw.rect(screen, white, pandoraButton)  # draw button
    pygame.draw.rect(screen, white, pastStation)  # draw button
    pygame.draw.rect(screen, white, nextStation)  # draw button
    pygame.draw.rect(screen, white, periodButton)  # draw button
    screen.blit(songName, (115, 90))
    screen.blit(pastSongText, pastSong)
    screen.blit(nextSongText, nextSong)
    screen.blit(playButtonText, playButton)
    screen.blit(pandoraButtonText, pandoraButton)
    screen.blit(stationText, (115, 250))
    screen.blit(pastStationText, pastStation)
    screen.blit(nextStationText, nextStation)
    screen.blit(periodTitleText, (115, 330))
    screen.blit(periodText, periodButton)
    pygame.draw.rect(screen, white, playBoth)  # draw button
    screen.blit(playBothText, playBoth)

knockButton = pygame.Rect(220, 50, 100, 39)
knockGameName = font.render('KnockOut', True, black)
targetButton = pygame.Rect(220, 90, 100, 39)
targetGameName = font.render('Target', True, black)
captureButton = pygame.Rect(220, 130, 100, 39)
captureGameName = font.render('Capture', True, black)
popupButton = pygame.Rect(220, 170, 100, 39)
popupGameName = font.render('Pop Up', True, black)
welcomeButton = pygame.Rect(10, 270, 100, 39)
welcomeText = font.render('Welcome', True, black)
testButton = pygame.Rect(10, 310, 100, 39)
testText = font.render('Test', True, black)

startButton = pygame.Rect(10, 110, 70, 39)
startText = font.render('Start', True, black)

soundEffect = "pew"
soundButton = pygame.Rect(225, 250, 90, 39)
soundEffectText = font.render(soundEffect, True, black)

def gameOptions():
    global knockGameName, targetGameName, captureGameName, soundEffect
    soundEffectText = font.render(soundEffect, True, black)
    pygame.draw.rect(screen, white, knockButton)  # draw button
    pygame.draw.rect(screen, white, targetButton)  # draw button
    pygame.draw.rect(screen, white, captureButton)  # draw button
    screen.blit(knockGameName, knockButton)
    pygame.draw.rect(screen, white, popupButton)  # draw button
    screen.blit(popupGameName, popupButton)
    screen.blit(targetGameName, targetButton)
    screen.blit(captureGameName, captureButton)
    pygame.draw.rect(screen, white, soundButton)  # draw button
    screen.blit(soundEffectText, soundButton)

redT = pygame.Rect(325, 50, 100, 39)
redTtext = font.render('Red', True, black)
oraT = pygame.Rect(325, 90, 100, 39)
oraTtext = font.render('Orange', True, black)
yelT = pygame.Rect(325, 130, 100, 39)
yelTtext = font.render('Yellow', True, black)
bluT = pygame.Rect(325, 170, 100, 39)
bluTtext = font.render('Blue', True, black)
greT = pygame.Rect(325, 210, 100, 39)
greTtext = font.render('Green', True, black)
whiT = pygame.Rect(325, 250, 100, 39)
whiTtext = font.render('White', True, black)


selectedFlag = 1
selectedColor = 1
redSelector = pygame.Rect(325, 290, 34, 39)
oraSelector = pygame.Rect(360, 290, 34, 39)
yelSelector = pygame.Rect(395, 290, 34, 39)
bluSelector = pygame.Rect(325, 330, 34, 39)
greSelector = pygame.Rect(360, 330, 34, 39)
whiSelector = pygame.Rect(395, 330, 34, 39)
purSelector = pygame.Rect(325, 370, 34, 39)
pinSelector = pygame.Rect(360, 370, 34, 39)
offSelector = pygame.Rect(395, 370, 34, 39)

stopButton = pygame.Rect(10, 160, 69, 39)
stopText = font.render('Stop', True, black)

def controlOptions():
    global knockGameName, targetGameName, captureGameName, selectedColor, selectedFlag
    if selectedFlag == "red":
        pygame.draw.rect(screen, white, redT)  # draw button
    else:
        pygame.draw.rect(screen, grey, redT)  # draw button
    if selectedFlag == "orange":
        pygame.draw.rect(screen, white, oraT)  # draw button
    else:
        pygame.draw.rect(screen, grey, oraT)  # draw button
    if selectedFlag == "yellow":
        pygame.draw.rect(screen, white, yelT)  # draw button
    else:
        pygame.draw.rect(screen, grey, yelT)  # draw button
    if selectedFlag == "blue":
        pygame.draw.rect(screen, white, bluT)  # draw button
    else:
        pygame.draw.rect(screen, grey, bluT)  # draw button
    if selectedFlag == "green":
        pygame.draw.rect(screen, white, greT)  # draw button
    else:
        pygame.draw.rect(screen, grey, greT)  # draw button
    if selectedFlag == "white":
        pygame.draw.rect(screen, white, whiT)  # draw button
    else:
        pygame.draw.rect(screen, grey, whiT)  # draw button

    if selectedColor == 1:
        pygame.draw.rect(screen, red, redSelector)  # draw button
    else:
        pygame.draw.rect(screen, darkred, redSelector)  # draw button
    if selectedColor == 2:
        pygame.draw.rect(screen, orange, oraSelector)  # draw button
    else:
        pygame.draw.rect(screen, darkorange, oraSelector)  # draw button
    if selectedColor == 3:
        pygame.draw.rect(screen, yellow, yelSelector)  # draw button
    else:
        pygame.draw.rect(screen, darkyellow, yelSelector)  # draw button
    if selectedColor == 4:
        pygame.draw.rect(screen, blue, bluSelector)  # draw button
    else:
        pygame.draw.rect(screen, darkblue, bluSelector)  # draw button
    if selectedColor == 5:
        pygame.draw.rect(screen, green, greSelector)  # draw button
    else:
        pygame.draw.rect(screen, darkgreen, greSelector)  # draw button
    if selectedColor == 6:
        pygame.draw.rect(screen, white, whiSelector)  # draw button
    else:
        pygame.draw.rect(screen, grey, whiSelector)  # draw button
    if selectedColor == 7:
        pygame.draw.rect(screen, (128, 0, 128), purSelector)  # draw button
    else:
        pygame.draw.rect(screen, (64,0,64), purSelector)  # draw button
    if selectedColor == 8:
        pygame.draw.rect(screen, (255, 192, 203), pinSelector)  # draw button
    else:
        pygame.draw.rect(screen, (128,98,100), pinSelector)  # draw button
    if selectedColor == 9:
        pygame.draw.rect(screen, (94,94,94), offSelector)  # draw button
    else:
        pygame.draw.rect(screen, (64,64,64), offSelector)  # draw button
    pygame.draw.rect(screen, white, sendButton)  # draw button
    screen.blit(sendText, sendButton)
    pygame.draw.rect(screen, white, sendAllButton)  # draw button
    screen.blit(sendAllText, sendAllButton)
    screen.blit(oraTtext, oraT)
    screen.blit(bluTtext, bluT)
    screen.blit(yelTtext, yelT)
    screen.blit(greTtext, greT)
    screen.blit(whiTtext, whiT)
    screen.blit(redTtext, redT)
    
    


def checkEventMain(mouse_pos):
    global troubleTitle, mainTitle, state, song, station, period, periodText, selectedColor, selectedFlag, soundEffect, playStation
    if soundButton.collidepoint(mouse_pos):
        if (soundEffect == "pew"):
            soundEffect = "ka-ching"
        elif (soundEffect == "ka-ching"):
            soundEffect = "shatter"
        else:
            soundEffect = "pew"
    if redT.collidepoint(mouse_pos):
        selectedFlag = "red"

    if oraT.collidepoint(mouse_pos):
        selectedFlag = "orange"

    if yelT.collidepoint(mouse_pos):
        selectedFlag = "yellow"

    if bluT.collidepoint(mouse_pos):
        selectedFlag = "blue"

    if greT.collidepoint(mouse_pos):
        selectedFlag = "green"

    if whiT.collidepoint(mouse_pos):
        selectedFlag = "white"
    
    if redSelector.collidepoint(mouse_pos):
        selectedColor = 1

    if oraSelector.collidepoint(mouse_pos):
        selectedColor = 2

    if yelSelector.collidepoint(mouse_pos):
        selectedColor = 3

    if bluSelector.collidepoint(mouse_pos):
        selectedColor = 4

    if greSelector.collidepoint(mouse_pos):
        selectedColor = 5

    if whiSelector.collidepoint(mouse_pos):
        selectedColor = 6

    if purSelector.collidepoint(mouse_pos):
        selectedColor = 7

    if pinSelector.collidepoint(mouse_pos):
        selectedColor = 8

    if offSelector.collidepoint(mouse_pos):
        selectedColor = 9

    if playButton.collidepoint(mouse_pos):
        playMusic.playSong(song, 0)

    if pandoraButton.collidepoint(mouse_pos):
        playMusic.playPandora(playStation, period, soundEffect)

    if playBoth.collidepoint(mouse_pos):
        playMusic.play(playStation, period, soundEffect, 9)

    if mix.collidepoint(mouse_pos):
        print("MIX: OFF FOR NOW" + soundEffect)
        #startTargetGame(fridayHits, soundEffect)
                        
    if lights.collidepoint(mouse_pos):
        if (state!=1):
            state = 1
            print("lightsOptions")
        else:
            state = 0

    if games.collidepoint(mouse_pos):
        if (state!=3):
            state = 3
            print("game option")
        else:
            state = 0


    if control.collidepoint(mouse_pos):
        if (state!=4):
            state = 4
            print("Control option")
        else:
            state = 0

    if nextSong.collidepoint(mouse_pos):
        if (song < numSongs):
            song+=1
            print(song)

    if pastSong.collidepoint(mouse_pos):
        if (song > 1):
            song-=1
            print(song)

    if nextStation.collidepoint(mouse_pos):
        if (station < numStations):
            station+=1
            print(playStation)

    if pastStation.collidepoint(mouse_pos):
        if (station > 0):
            station-=1
            print(playStation)
    
    if sendButton.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + str(selectedFlag) + str(selectedColor))

    if sendAllButton.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "red" + str(selectedColor))
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "orange" + str(selectedColor))
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "white" + str(selectedColor))
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "green" + str(selectedColor))
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "yellow" + str(selectedColor))
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "blue" + str(selectedColor))


    if periodButton.collidepoint(mouse_pos):
        if (period == 7):
            period = 11
            periodText = font.render('11 mins', True, black)
        elif (period == 11):
            period = 30
            periodText = font.render('30 mins', True, black)
        elif (period == 30):
            period = 90
            periodText = font.render('180 mins', True, black)
        elif (period == 90):
            period = 500
            periodText = font.render('500 mins', True, black)
        elif (period == 500):
            period = 0
            periodText = font.render('0 mins', True, black)
        else:
            period = 7
            periodText = font.render('7 mins', True, black)
    if endButton.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "shutdown")
        playMusic.shutdownMessage()
    
    if knockButton.collidepoint(mouse_pos):
        print("Knockout: OFF FOR NOW")
        #startKnockOutGame(playStation, soundEffect)
    if targetButton.collidepoint(mouse_pos):
        print("Target: OFF FOR NOW")
        #startTargetGame(playStation, soundEffect)
    if captureButton.collidepoint(mouse_pos):
        print("Capture: OFF FOR NOW")
        #startCaptureGame(playStation, soundEffect)
    if popupButton.collidepoint(mouse_pos):
        print("Pop Up: OFF FOR NOW")
        #startPopupGame(playStation, soundEffect)
    
    stationT = fridayHits
    if sunday.collidepoint(mouse_pos):
        stationT = sunCountry

    if welcomeButton.collidepoint(mouse_pos):
        welcomeMessage()
    
    if testButton.collidepoint(mouse_pos):
        askReady()

    if stopButton.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "stop")

    if startButton.collidepoint(mouse_pos):
        print("Starting")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "start")
        askReady()
        welcomeMessage()
        playMusic.play(stationT, period, soundEffect, 20)
    
    if restartRed.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:red")
    if restartOrange.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:orange")
    if restartWhite.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:white")
    if restartGreen.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:green")
    if restartYellow.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:yellow")
    if restartBlue.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:blue")
  
    if restartAll.collidepoint(mouse_pos):
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:red")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:orange")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:white")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:green")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:yellow")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "restart:blue")
        os.system("mosquitto_pub -h localhost -t test_channel -m " + "endstop")


os.system("mosquitto_pub -h localhost -t test_channel -m " + "start")
main()