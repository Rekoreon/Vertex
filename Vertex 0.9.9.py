#Vertex
#24/01/2018
#Joe Casci
import pygame
import time
import random
import string
pygame.init()
displayHeight = 600
displayWidth = 620
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Vertex')
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
magenta = (255,0,255)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
yellow = (255,255,0)
clock = pygame.time.Clock()
FPS = 60

def resetPos(diamondSize,lifeWidth):
    xPos = displayWidth/2-diamondSize/2+lifeWidth/2
    yPos = displayHeight/2-diamondSize/2
    xPosChange = 0
    yPosChange = 0
    lifePos = displayHeight
    return xPos,yPos,xPosChange,yPosChange,lifePos

def createFlashNum(flashNum,mode):
    flashNums = []
    if mode == "normal":
        flashNumMin=0
        flashNumMax=5
    elif mode == "special":
        flashNumMin=0
        flashNumMax=9
    for i in range(flashNumMax):
        if i != flashNum and i > flashNumMin:
            flashNums.append(i)
    flashNum = random.choice(flashNums)
    return flashNum

def makeCoords(flashNum,flashGreen,flashRed,diamondSize,lifeWidth,flashHeight,flashWidth):
    leftCoords = [lifeWidth, displayHeight/2-diamondSize/2]
    topCoords = [displayWidth/2-diamondSize/2+lifeWidth/2, 0]
    rightCoords = [displayWidth-diamondSize, displayHeight/2-diamondSize/2]
    bottomCoords = [displayWidth/2-diamondSize/2+lifeWidth/2, displayHeight-diamondSize]
    leftFlashCoords = [lifeWidth, displayHeight/2-flashHeight/2]
    topFlashCoords = [displayWidth/2-flashWidth+lifeWidth/2, 0]
    rightFlashCoords = [displayHeight-flashWidth+lifeWidth, displayHeight/2-flashHeight/2]
    bottomFlashCoords = [displayWidth/2-flashWidth+lifeWidth/2, displayHeight-flashWidth]
    deathCoords = []
    if flashNum == 1:
        flash = flashGreen
        pointCoords = leftCoords
        flashCoords = leftFlashCoords
        deathCoords.extend([topCoords,rightCoords,bottomCoords])
    elif flashNum == 2:
        flash = pygame.transform.rotate(flashGreen,270)
        pointCoords = topCoords
        flashCoords = topFlashCoords
        deathCoords.extend([leftCoords,rightCoords,bottomCoords])
    elif flashNum == 3:
        flash = pygame.transform.rotate(flashGreen,180)
        pointCoords = rightCoords
        flashCoords = rightFlashCoords
        deathCoords.extend([leftCoords,topCoords,bottomCoords])
    elif flashNum == 4:
        flash = pygame.transform.rotate(flashGreen,90)
        pointCoords = bottomCoords
        flashCoords = bottomFlashCoords
        deathCoords.extend([leftCoords,topCoords,rightCoords])
    elif flashNum == 5:
        flash = flashRed
        flashCoords = leftFlashCoords
        pointCoords = rightCoords
        deathCoords.extend([leftCoords,topCoords,bottomCoords])         
    elif flashNum == 6:
        flash = pygame.transform.rotate(flashRed,270)
        flashCoords = topFlashCoords
        pointCoords = bottomCoords
        deathCoords.extend([leftCoords,topCoords,rightCoords])
    elif flashNum == 7:
        flash = pygame.transform.rotate(flashRed,180)
        flashCoords = rightFlashCoords
        pointCoords = leftCoords
        deathCoords.extend([topCoords,rightCoords,bottomCoords])
    elif flashNum == 8:
        flash = pygame.transform.rotate(flashRed,90)
        flashCoords = bottomFlashCoords
        pointCoords = topCoords
        deathCoords.extend([leftCoords,rightCoords,bottomCoords])    
    return flash, flashCoords, pointCoords, deathCoords

def blitMessage(message,colour,shadow,xPos,yPos,size,selected):
    font = pygame.font.SysFont(None, size)
    screenMessage = font.render(message, True, colour)
    screenShadow = font.render(message,True,shadow)
    width = screenMessage.get_width()
    height = screenMessage.get_height()
    if selected:
        arrow = pygame.image.load("menuArrow.png")
        arrowWidth = arrow.get_width()
        arrowHeight = arrow.get_height()
        gameDisplay.blit(arrow, [(xPos-width/2-arrowWidth*2),yPos-arrowHeight/2])
        screenMessage = font.render(message,True,yellow)
        screenShadow = font.render(message,True,red)
    gameDisplay.blit(screenShadow, [(xPos-width/2)+1,(yPos-height/2)+1])
    gameDisplay.blit(screenMessage, [(xPos-width/2),(yPos-height/2)])
    
def writeToFile(name,score,written,mode,gameOverMessage):
    if mode == "normal":
        file = open("leaderboardNormal.txt","r")
    elif mode == "special":
        file = open("leaderboardSpecial.txt","r")
    leaderboard = []
    for line in file:
        temp = line.split(",")
        temp[1]=int(temp[1][0:-1])
        leaderboard.append(temp)
    file.close()
    count = 0
    place = 0
    for i in leaderboard:
        if score <= int(i[1]) and name == i[0]:
            written = True
            if count == 0:
                position = "1st"
            elif count ==1:
                position = "2nd"
            elif count ==2:
                position = "3rd"
            else:
                position = "{0}th".format(count+1)
            gameOverMessage = "Your old score is higher, you're still {0}".format(position)
            place = 10
        elif score > int(i[1]) and not written:
            leaderboard.insert(count,[name,score])
            written = True
            place = count
            while count < len(leaderboard)-1:
                count+=1
                if name == leaderboard[count][0]:
                    del leaderboard[count]
            if len(leaderboard) > 10:
                leaderboard = leaderboard[0:-1]      
        count+=1
    if not written:
        place = 10
        written = True
    if mode == "normal":
        file = open("leaderboardNormal.txt","w")
    elif mode == "special":
        file = open("leaderboardSpecial.txt","w")
    for i in leaderboard:
        file.write("{0},{1}\n".format(i[0],i[1]))
    file.close()
    return written, place, gameOverMessage

def start():
    blitMessage("L O A D I N G . . .",green,magenta,displayWidth/2,displayHeight*0.5,72, False)
    pygame.display.update()
    pygame.mixer.init()
    titleMusic = pygame.mixer.Sound("Jerry Five.ogg")
    startBool = True
    signInBool = True
    name = ""
    startMenu = [1,0,0,0,0]
    pointer = 0
    caps = False
    playingMusic = False
    while startBool:
        while signInBool:
            gameDisplay.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    try:
                        key = chr(event.key)
                        check = pygame.key.get_pressed()
                        if check[pygame.K_LSHIFT] or check[pygame.K_CAPSLOCK]:
                            key = key.upper()
                    except ValueError:
                        key = ""
                    if key =="\r":
                        signInBool=False
                        key = ""
                    elif key =="\x08":
                        name = name[0:-1]
                        key = ""
                    if len(name) <15:
                        if not key in string.printable:
                            key = ""
                        name+=key        
            blitMessage("Please enter a username (Max 15 Characters):",green,magenta,displayWidth/2,displayHeight*0.45,36, False)        
            blitMessage(name,cyan,blue,displayWidth/2,displayHeight*0.5,36, False)
            pygame.display.update()
        if playingMusic == False:
            titleMusic.play(-1)
            playingMusic = True
        gameDisplay.fill(black)
        blitMessage("V E R T E X",green,magenta,displayWidth/2,displayHeight*0.15,144, False)
        blitMessage("Welcome, {0}!".format(name),cyan,blue,displayWidth/2,displayHeight*0.35,54, False)
        blitMessage("PLAY NORMAL MODE",green,magenta,displayWidth/2,displayHeight*0.5,48, startMenu[0])
        blitMessage("PLAY SPECIAL MODE",green,magenta,displayWidth/2,displayHeight*0.6,48, startMenu[1])
        blitMessage("VIEW LEADERBOARD",green,magenta,displayWidth/2,displayHeight*0.7,48, startMenu[2])
        blitMessage("SIGN OUT",green,magenta,displayWidth/2,displayHeight*0.8,36, startMenu[3])
        blitMessage("QUIT",green,magenta,displayWidth/2,displayHeight*0.875,36, startMenu[4])
        blitMessage("F1 for Instructions",white,magenta,displayWidth*0.2,displayHeight*0.965,36,False)
        blitMessage("V0.9.9", white,magenta,displayWidth*0.96,displayHeight*0.975,18,False)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    infoBool = True
                    gameDisplay.fill(black)
                    blitMessage("You are a diamond.",cyan,blue,displayWidth/2,displayHeight*0.15,72,False)
                    blitMessage("You see a green flash.",white,magenta,displayWidth/2,displayHeight*0.3,48,False)
                    blitMessage("You think 'yes'.",white,magenta,displayWidth/2,displayHeight*0.375,48,False)
                    blitMessage("You run towards the green flash.",white,magenta,displayWidth/2,displayHeight*0.45,48,False)
                    blitMessage("You see a red flash.",white,magenta,displayWidth/2,displayHeight*0.6,48,False)
                    blitMessage("You think 'no'.",white,magenta,displayWidth/2,displayHeight*0.675,48,False)
                    blitMessage("You run away from the red flash.",white,magenta,displayWidth/2,displayHeight*0.75,48,False)
                    blitMessage("F1 TO CLOSE",white,magenta,displayWidth/2,displayHeight*0.9,36,False)
                    pygame.display.update()
                    while infoBool:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_F1:
                                    infoBool = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    startMenu[pointer] = 0
                    pointer+=1
                    if pointer == len(startMenu):
                        pointer = 0
                    startMenu[pointer]= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    startMenu[pointer] = 0
                    pointer-=1
                    if pointer == -1:
                        pointer = len(startMenu)-1
                    startMenu[pointer] = 1
                if event.key == pygame.K_RETURN:
                    if startMenu[0]:
                        titleMusic.stop()
                        gameLoop("normal",name)
                        titleMusic.play(-1)
                    elif startMenu[1]:
                        titleMusic.stop()
                        gameLoop("special",name)
                        titleMusic.play(-1)
                    elif startMenu[2]:
                        leaderboardFunc("normal",name,-1,False)
                    elif startMenu[3]:
                        signInBool = True
                    elif startMenu[4]:
                        startBool = False
						
def gameLoop(mode,name):
    gameDisplay.fill(black)
    blitMessage("L O A D I N G . . .",green,magenta,displayWidth/2,displayHeight*0.5,72, False)
    pygame.display.update()
    board = pygame.image.load("board.png")
    diamond = pygame.image.load("diamond.png")
    flashGreen = pygame.image.load("flashGreen.png")
    flashRed = pygame.image.load("flashRed.png")
    flashHeight = flashGreen.get_height()
    flashWidth = flashGreen.get_width()
    section_pass = pygame.mixer.Sound("speedIncreaseSound.ogg")
    passat90 = pygame.mixer.Sound("90sSound.ogg")
    music = pygame.mixer.Sound("EDM Detection Mode.ogg")
    sound = pygame.mixer.Sound("hitSound.ogg")
    diamondSize = diamond.get_height()
    gameOver = False
    gameLoopBool = True
    reset = True
    lifeWidth = 20
    while gameLoopBool:
        if reset:
            flashNum = createFlashNum(0,mode)
            lifePosChange=0
            score = 0
            message = "Score = %s" %score
            xPos, yPos, xPosChange, yPosChange, lifePos = resetPos(diamondSize,lifeWidth)
            speed = (displayHeight/2-diamondSize/2)/4
            reset = False
            victory = red
            victory_shadow = cyan
            gameOverMsg = "GAME OVER"
            gameOverFont = 128
            gameOverFontChange = -3
            gameOver_options = [1,0,0]
            pointer = 0
            written = False
            playingMusic = False
            gameOverMessage ="You didn't make the leaderboard :("
            music.play(-1)
        if xPosChange == 0 and yPosChange == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameLoopBool = False
                    startBool = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        xPosChange = -speed
                        yPosChange = 0
                        sound.play()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        xPosChange = speed
                        yPosChange = 0
                        sound.play()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        yPosChange = speed
                        xPosChange = 0
                        sound.play()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        yPosChange = -speed
                        xPosChange = 0
                        sound.play()
        xPos += xPosChange
        yPos += yPosChange
        lifePos -= lifePosChange       
        flash, flashCoords, pointCoords, deathCoords = makeCoords(flashNum,flashGreen,flashRed,diamondSize,lifeWidth,flashHeight,flashWidth) 
        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [0,0,lifeWidth,(displayHeight)])
        pygame.draw.rect(gameDisplay, green, [0,displayHeight,lifeWidth,-lifePos])
        gameDisplay.blit(board,(lifeWidth,0))
        blitMessage("V E R T E X",green,magenta,displayWidth*0.225,displayHeight*0.05,48, False)
        gameDisplay.blit(flash,(flashCoords[0],flashCoords[1]))
        gameDisplay.blit(diamond,(xPos,yPos))
        blitMessage(message,cyan,blue,(displayWidth*0.85),displayHeight*0.05,36, False)
        pygame.display.update()
        if xPos == pointCoords[0] and yPos == pointCoords[1]:
            flashNum = createFlashNum(flashNum,mode)
            score = score + 1
            message = "Score = %s" %score
            if lifePosChange == 0:
                lifePosChange = 6
            elif lifePosChange < 24 and lifePosChange > 0 and score%10 == 0:
                if score == 90:
                    passat90.play()
                else:
                    section_pass.play()
                lifePosChange += 1.8
            xPos, yPos, xPosChange, yPosChange, lifePos = resetPos(diamondSize,lifeWidth)
        elif lifePos <= 0:
            gameOver = True
            music.stop()
        else:
            for i in deathCoords:
                if xPos == i[0] and yPos ==i[1]:
                    gameOver = True
                    music.stop()
        while gameOver == True:
            if written == False:
                written, place, gameOverMessage = writeToFile(name,score,written,mode,gameOverMessage)
            gameDisplay.fill(black)    
            blitMessage("{1} points".format(name,score),cyan,blue,displayWidth/2,displayHeight*0.375,72, False)
            if place <10:
                if place == 0:
                    blitMessage("You are the champion, {0}!".format(name),cyan,blue,displayWidth/2,displayHeight*0.4475,36, False)
                    if not playingMusic:
                        gameOverMusic = pygame.mixer.Sound("highscore.ogg")
                    if victory == red:
                        victory = cyan
                        victory_shadow = red
                    elif victory == cyan:
                        victory = red
                        victory_shadow = cyan
                    gameOverFont+=gameOverFontChange
                    if gameOverFont>= 200:
                        gameOverFontChange=-4
                    elif gameOverFont<=2:
                        gameOverFontChange=9
                    gameOverMsg = "HIGHSCORE"
                elif place == 1:
                    blitMessage("2nd Place! Runner up!",cyan,blue,displayWidth/2,displayHeight*0.4475,36, False)
                    if not playingMusic:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
                elif place == 2:
                    blitMessage("3rd Place! Bronze is still a medal!",cyan,blue,displayWidth/2,displayHeight*0.4475,36, False)
                    if not playingMusic:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
                else:
                    blitMessage("{0}th place on the leaderboard!".format(place+1),cyan,blue,displayWidth/2,displayHeight*0.4475,36, False)
                    if not playingMusic:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
            else:
                blitMessage(gameOverMessage,cyan,blue,displayWidth/2,displayHeight*0.4475,36, False)
                if not playingMusic:
                    gameOverMusic = pygame.mixer.Sound("gameOverMusic.ogg")
            if not playingMusic:
                gameOverMusic.play(-1)
                playingMusic = True
            blitMessage(gameOverMsg,victory,victory_shadow,displayWidth/2,displayHeight*0.15,gameOverFont, False)
            blitMessage("PLAY AGAIN",green,magenta,displayWidth/2,displayHeight*0.6,48, gameOver_options[0])
            blitMessage("LEADERBOARD",green,magenta,displayWidth/2,displayHeight*0.7,48, gameOver_options[1])
            blitMessage("MAIN MENU",green,magenta,displayWidth/2,displayHeight*0.8,48, gameOver_options[2])
            blitMessage("Thank you for playing!",white,magenta,displayWidth/2,displayHeight*0.95,36, False)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        gameOver_options[pointer] = 0
                        pointer+=1
                        if pointer == len(gameOver_options):
                            pointer = 0
                        gameOver_options[pointer]= 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        gameOver_options[pointer] = 0
                        pointer-=1
                        if pointer == -1:
                            pointer = len(gameOver_options)-1
                        gameOver_options[pointer] = 1
                    if event.key == pygame.K_RETURN:
                        if gameOver_options[0]:
                            gameOver = False
                            reset = True
                            pygame.mixer.stop()
                        elif gameOver_options[1]:
                            leaderboardFunc(mode,name,place,True)
                        elif gameOver_options[2]:
                            gameOver = False
                            gameLoopBool = False
                            pygame.mixer.stop()
        clock.tick(FPS)

def leaderboardFunc(mode,name,place,playing):
    arrow = pygame.image.load("arrow.png")
    file = open("leaderboardNormal.txt","r")
    leaderboardNormal = []
    leaderboardspecial = []
    leaderboardCurrent = []
    for line in file:
        temp = line.split(",")
        temp[1]=temp[1][0:-1]
        leaderboardNormal.append(temp)
    file.close()
    file = open("leaderboardSpecial.txt","r")
    for line in file:
        temp = line.split(",")
        temp[1]=temp[1][0:-1]
        leaderboardspecial.append(temp)
    file.close()
    keepLeaderboarding = True
    leaderboardMode = mode
    printed = False
    while keepLeaderboarding:
        if leaderboardMode == "normal":
            leaderboardCurrent = leaderboardNormal
        elif leaderboardMode == "special":
            leaderboardCurrent = leaderboardspecial
        gameDisplay.fill(black)
        blitMessage("L E A D E R B O A R D",green,magenta,displayWidth/2,displayHeight*0.1,72, False)
        blitMessage("PRESS BACKSPACE OR ESCAPE TO CLOSE",green,magenta,displayWidth/2,displayHeight*0.935,36, False)
        y_pos=displayHeight*0.25
        count=1
        while not printed:
            blitMessage("of {0} mode".format(leaderboardMode),green,magenta,displayWidth/2,displayHeight/6,36, False)
            if leaderboardMode == "normal":
                gameDisplay.blit(pygame.transform.rotate(arrow,180),(550,displayHeight/2))
            elif leaderboardMode == "special":
                gameDisplay.blit(arrow,(10,displayHeight/2))
            for i in range(0,10):
                if leaderboardCurrent[i][0] == name:
                    col = cyan
                    shad = blue
                else:
                    col = white
                    shad = magenta
                blitMessage(str(count)+".",col,shad,120,y_pos,36, False)
                blitMessage(str(leaderboardCurrent[i][0]),col,shad,displayWidth*0.4,y_pos,36, False)
                blitMessage(str(leaderboardCurrent[i][1]),col,shad,(displayWidth/3)*2,y_pos,36, False)
                y_pos+=40
                count+=1
            printed = True
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                     if leaderboardMode == "special":
                         leaderboardMode = "normal"
                         printed = False
                 elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                     if leaderboardMode == "normal":
                         leaderboardMode = "special"
                         printed = False
                 elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                     keepLeaderboarding = False

start()
pygame.quit()
quit()
