# Agario with Phidgets using CMU graphics
# Version 2.0 - Two player mode
# G. Hutchison
# August 16, 2022

from cmu_graphics import *
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.HumiditySensor import *

import random

phidgets_connected = False

# Setup all Phidget devices
try:
    temp = TemperatureSensor()
    temp.openWaitForAttachment(5000)

    humid = HumiditySensor()
    humid.openWaitForAttachment(5000)

    red = DigitalOutput()
    red.setIsHubPortDevice(True)
    red.setHubPort(1)

    green = DigitalOutput()
    green.setIsHubPortDevice(True)
    green.setHubPort(4)

    red.openWaitForAttachment(5000)
    green.openWaitForAttachment(5000)

    vertical_p1 = VoltageRatioInput()
    vertical_p1.setHubPort(3)
    vertical_p1.setChannel(0)

    button = DigitalInput()
    button.setHubPort(3)

    horizontal_p1 = VoltageRatioInput()
    horizontal_p1.setHubPort(3)
    horizontal_p1.setChannel(1)

    vertical_p2 = VoltageRatioInput()
    vertical_p2.setHubPort(2)
    vertical_p2.setChannel(0)

    horizontal_p2 = VoltageRatioInput()
    horizontal_p2.setHubPort(2)
    horizontal_p2.setChannel(1)

    button2 = DigitalInput()
    button2.setHubPort(2)

    horizontal_p1.openWaitForAttachment(1000)
    vertical_p1.openWaitForAttachment(1000)

    horizontal_p2.openWaitForAttachment(1000)
    vertical_p2.openWaitForAttachment(1000)

    button.openWaitForAttachment(1000)
    button2.openWaitForAttachment(1000)

    vertical_p1.setDataInterval(vertical_p1.getMinDataInterval())
    horizontal_p1.setDataInterval(horizontal_p1.getMinDataInterval())
    vertical_p2.setDataInterval(vertical_p2.getMinDataInterval())
    horizontal_p2.setDataInterval(horizontal_p2.getMinDataInterval())
    
    phidgets_connected = True

except PhidgetException as ex:
    print("")
    print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

# CMU graphics
app.background = gradient('aliceBlue', rgb(10,10,100))
app.stepsPerSecond = 60

#Size of canvas
HEIGHT = 1000 #1000
WIDTH = 1000 #1860
app.width = WIDTH
app.height = HEIGHT

if phidgets_connected:
    game_over = False
    game_won = False
    winner = ""

    circles = Group()

    NUM_CIRCLES = 5
    PLAYER_RADIUS = 15

    player = Circle(WIDTH/2, HEIGHT/2+100, PLAYER_RADIUS, fill="red")
    player2 = Circle(WIDTH/2, HEIGHT/2-100, PLAYER_RADIUS, fill="green")

    reset_button =Rect(WIDTH/2, 200, 400, 100, align='center', fill="green")
    reset_label = Label("Click to Play", WIDTH/2, 200, size=40, fill="white") 

    reset_button.visible = True
    reset_label.visible = True

    msg = Label('', WIDTH/2, HEIGHT/2, size=80, border="black", borderWidth=1, fill="red", visible=False)
    temp_msg = Label('', WIDTH/2, 50, font="grenze",size=50, border="black", borderWidth=1, fill="white", visible=False)

    new_game = True
else:
    Label("Connect your Phidgets",WIDTH/2,HEIGHT/2, size=80, fill="red")

def reset():
    global game_over, game_won, winner
    game_over = False
    game_won = False
    winner = ""
    
    # turn off LEDs
    red.setState(False)
    green.setState(False)
    
    app.background = gradient('aliceBlue', rgb(10,10,100))
    
    #player.pos = (WIDTH/2, HEIGHT/2+100)
    #player2.pos = (WIDTH/2, HEIGHT/2-100)

    # Position player 1 and player 2
    player.speed=30
    player.radius = PLAYER_RADIUS

    # Create player 2    
    player2.speed=30
    player2.radius=PLAYER_RADIUS

    button_pressed = False
    
    while not button_pressed:
        if (button.getState() or button2.getState()):
           
            button_pressed = True
            
            # remove the Play button
            reset_button.visible = False
            reset_label.visible = False
            
    circles.clear()

    for _ in range(NUM_CIRCLES):
        c = Circle(random.randint(50,WIDTH/2-50),random.randint(50,HEIGHT-50),PLAYER_RADIUS)
        c.speed = random.randint(5,10)
        c.xdir = random.choice((1,-1))
        c.ydir = random.choice((1,-1))
        c.radius = random.choice((10,12,13, 25,30))
        circles.add(c)
        
    for _ in range(NUM_CIRCLES):
        c = Circle(random.randint(WIDTH/2+50,WIDTH-50),random.randint(50,HEIGHT-50),PLAYER_RADIUS)
        c.speed = random.randint(5,10)
        c.xdir = random.choice((1,-1))
        c.ydir = random.choice((1,-1))
        c.radius = random.choice((10,12,13,25,30))
        circles.add(c)

def onStep():
    global game_over
    global game_won
    global winner    

    if phidgets_connected:
        temperature = temp.getTemperature()
        temperature_F = (temperature* 9/5) + 32 # convert to Fahrenheit
        humidity = humid.getHumidity()
        temp_msg.value = f"Temp is {temperature:.1f} C"
        temp_msg.visible = True
        
        if (not game_over and not game_won):
            
            # Player 1 event handling
            v1 = vertical_p1.getVoltageRatio()
            h1 = horizontal_p1.getVoltageRatio()
            
            if (h1 > .3):
                player.centerX += player.speed
            elif (h1 < -.3):
                player.centerX -= player.speed
                
            if (v1 > .3): # opposite directions
                player.centerY -= player.speed
            elif (v1 < -.3):
                player.centerY += player.speed
            
            # player 2 event handling
            v2 = vertical_p2.getVoltageRatio()
            h2 = horizontal_p2.getVoltageRatio()
            
            if (h2 > .3):
                player2.centerX += player2.speed
            elif (h2 < -.3):
                player2.centerX -= player2.speed
                
            if (v2 > .3): # opposite directions
                player2.centerY -= player2.speed
            elif (v2 < -.3):
                player2.centerY += player2.speed
                
            # wrap players
            if (player.left>WIDTH):
                player.right = 0
            elif (player.right<0):
                player.left = WIDTH
                
            if (player.bottom<0):
                player.top = HEIGHT
            elif (player.top>HEIGHT):
                player.bottom=0
            
            if (player2.left>WIDTH):
                player2.right = 0
            elif (player2.right<0):
                player2.left = WIDTH
                
            if (player2.bottom<0):
                player2.top = HEIGHT
            elif (player2.top>HEIGHT):
                player2.bottom=0

            # move the opponents
            for c in circles:
                c.centerX = c.centerX+(c.xdir*c.speed)
                c.centerY = c.centerY+(c.ydir*c.speed)
                
                # bounce for fun
                if c.right>WIDTH or c.left<0:
                    c.xdir*=-1
                    
                if c.bottom>HEIGHT or c.top<0 :
                    c.ydir*=-1
                    
            for c in circles:
                # player 1 hits shapes
                if (player.hitsShape(c)):
                    if player.radius>c.radius:
                        circles.remove(c)
                        player.radius +=c.radius/2
                        
                        if (player.speed>6):
                            player.speed -=1 # slow down
                    else:
                        # you hit an object that was too big
                        game_over = True
                        winner = "Player 2"
                
                # player 2 hits shapes
                
                if (player2.hitsShape(c)):
                    if player2.radius>c.radius:
                        circles.remove(c)
                        player2.radius +=c.radius/2
                        
                        if (player2.speed>6):
                            player2.speed -=1 # slow down
                    elif player2.radius<c.radius:
                        # you hit an object that was too big
                        game_over = True
                        winner = "Player 1"
                        
            if player.hitsShape(player2):
                if player.radius>player2.radius:
                    winner = "Player 1"
                elif player.radius<player2.radius:
                    winner = "Player 2"
                else:
                    winner = "TIE"
                    
                game_over = True
                
            # no more objects to consume... you must be a winner
            if (len(circles)==0):
                if player.radius>player2.radius:
                    winner = "Player 1"
                elif player2.radius>player.radius:
                    winner = "Player 2"
                game_won = True
               
                    
        else:        
            if (game_over):
                if (winner == "Player 1"):
                    msg.value = 'WINNER IS RED'
                    red.setState(True)
                elif (winner == "Player 2"):
                    msg.value = 'WINNER IS GREEN'
                    green.setState(True)
                else:
                    msg.value = 'TIE'
                    green.setState(True)
                    red.setState(True)
            elif (game_won):
                if (player.radius>player2.radius):
                    msg.value = 'WINNER IS RED'
                    red.setState(True)
                elif (player.radius<player2.radius):
                    msg.value = 'WINNER IS GREEN'
                    green.setState(True)
                else:
                    msg.value = ""
            
            reset_button.visible = True
            reset_label.visible = True
            msg.visible = True
            
            if (button.getState() or button2.getState()):
                player.pos = (WIDTH/2, HEIGHT/2+100)
                player2.pos = (WIDTH/2, HEIGHT/2-100)
                msg.visible = False # remove message
                reset()   

cmu_graphics.loop()