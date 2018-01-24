#Vertex
#24/01/2018
#Joe Casci
import pygame
import time
import random
import string
pygame.init()
display_size = 600
display_width = 620
gameDisplay = pygame.display.set_mode((display_width,display_size))
pygame.display.set_caption('Vertex')
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
purple = (255,0,255)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
yellow = (255,255,0)
liquid_clear = (0,0,0,0)
clock = pygame.time.Clock()
FPS = 60

def start():
    blitMessage("L O A D I N G . . .",green,purple,display_width/2,display_size*0.5,72, False)
    pygame.display.update()
    pygame.mixer.init()
    titleMusic = pygame.mixer.Sound("Jerry Five.ogg")
    startBool = True
    signInBool = True
    name = ""
    width = 600
    height = 600
    menu_options = [1,0,0,0,0]
    pointer = 0
    caps = False
    musicing = False
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
            blitMessage("Please enter a username (Max 15 Characters):",green,purple,display_width/2,display_size*0.45,36, False)        
            blitMessage(name,cyan,blue,display_width/2,display_size*0.5,36, False)
            pygame.display.update()
        if musicing == False:
            titleMusic.play(-1)
            musicing = True
        gameDisplay.fill(black)
        blitMessage("V E R T E X",green,purple,display_width/2,display_size*0.15,144, False)
        blitMessage("Welcome, {0}!".format(name),cyan,blue,display_width/2,display_size*0.37,54, False)
        blitMessage("PLAY NORMAL MODE",green,purple,display_width/2,display_size*0.5,48, menu_options[0])
        blitMessage("PLAY SPECIAL MODE",green,purple,display_width/2,display_size*0.6,48, menu_options[1])
        blitMessage("VIEW LEADERBOARD",green,purple,display_width/2,display_size*0.7,48, menu_options[2])
        blitMessage("SIGN OUT",green,purple,display_width/2,display_size*0.825,36, menu_options[3])
        blitMessage("QUIT",green,purple,display_width/2,display_size*0.9,36, menu_options[4])
        blitMessage("V1.0.1", white,purple,display_width*0.96,display_size*0.975,18,False)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu_options[pointer] = 0
                    pointer+=1
                    if pointer == len(menu_options):
                        pointer = 0
                    menu_options[pointer]= 1
                elif event.key == pygame.K_UP:
                    menu_options[pointer] = 0
                    pointer-=1
                    if pointer == -1:
                        pointer = len(menu_options)-1
                    menu_options[pointer] = 1
                if event.key == pygame.K_RETURN:
                    if menu_options[0]:
                        titleMusic.stop()
                        gameLoop("normal",name)
                        titleMusic.play(-1)
                    elif menu_options[1]:
                        titleMusic.stop()
                        gameLoop("special",name)
                        titleMusic.play(-1)
                    elif menu_options[2]:
                        leaderboardFunc("normal",name,-1,False)
                    elif menu_options[3]:
                        signInBool = True
                    elif menu_options[4]:
                        startBool = False
                        
def gameLoop(mode,name):
    gameDisplay.fill(black)
    blitMessage("L O A D I N G . . .",green,purple,display_width/2,display_size*0.5,72, False)
    pygame.display.update()
    board = pygame.image.load("board.png")
    diamond = pygame.image.load("diamond.png")
    flashGreen = pygame.image.load("flashGreen.png")
    flashRed = pygame.image.load("flashRed.png")
    section_pass = pygame.mixer.Sound("speedIncreaseSound.ogg")
    passat90 = pygame.mixer.Sound("90sSound.ogg")
    music = pygame.mixer.Sound("EDM Detection Mode.ogg")
    sound = pygame.mixer.Sound("hitSound.ogg")
    block_size = diamond.get_height()
    gameOver = False
    gameLoopBool = True
    reset = True
    while gameLoopBool:
        if reset:
            flash_num = flash_num_creator(0,mode)
            life_drain=0
            score = 0
            msg = "Score = %s" %score
            lead_x = ((display_size/2)-(block_size/2))+20
            lead_y = ((display_size/2)-(block_size/2))
            lead_x_life = display_size
            speed = (display_size/2-block_size/2)/4
            lead_x_change=0
            lead_y_change=0
            reset = False
            victory = red
            victory_shadow = cyan
            gameOverMsg = "GAME OVER"
            gameOverFont = 152
            gameOverFontChange = -3
            gameOver_options = [1,0,0]
            pointer = 0
            written = False
            musicing = False
            messuj ="You didn't make the leaderboard :("
            music.play(-1)
        if lead_x_change == 0 and lead_y_change == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameLoopBool = False
                    startBool = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        lead_x_change = -speed
                        lead_y_change = 0
                        sound.play()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        lead_x_change = speed
                        lead_y_change = 0
                        sound.play()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        lead_y_change = speed
                        lead_x_change = 0
                        sound.play()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        lead_y_change = -speed
                        lead_x_change = 0
                        sound.play()
        lead_x += lead_x_change
        lead_y += lead_y_change
        lead_x_life -= life_drain       
        flash, flash_coords, point_coords, death_coords = coord_maker(flash_num,flashGreen,flashRed,block_size) 
        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [0,0,20,(display_size)])
        pygame.draw.rect(gameDisplay, green, [0,display_size,20,-lead_x_life])
        gameDisplay.blit(board,(20,0))
        blitMessage("V E R T E X",green,purple,display_width*0.225,display_size*0.05,48, False)
        gameDisplay.blit(flash,(flash_coords[0],flash_coords[1]))
        gameDisplay.blit(diamond,(lead_x,lead_y))
        blitMessage(msg,cyan,blue,(display_width*0.85),display_size*0.05,36, False)
        pygame.display.update()
        if lead_x == point_coords[0] and lead_y == point_coords[1]:
            flash_num = flash_num_creator(flash_num,mode)
            score = score + 1
            msg = "Score = %s" %score
            if life_drain == 0:
                life_drain = 6
            elif life_drain < 24 and life_drain > 0 and score%10 == 0:
                if score == 90:
                    passat90.play()
                else:
                    section_pass.play()
                life_drain += 1.8
            lead_x, lead_y, lead_x_change, lead_y_change, lead_x_life = resetPos(block_size)
        elif lead_x_life <= 0:
            gameOver = True
            music.stop()
        else:
            for i in death_coords:
                if lead_x == i[0] and lead_y ==i[1]:
                    gameOver = True
                    music.stop()
        while gameOver == True:
            if written == False:
                written, place, messuj = writeToFile(name,score,written,mode,messuj)
            gameDisplay.fill(black)    
            blitMessage("{1} points".format(name,score),cyan,blue,display_width/2,display_size*0.375,72, False)
            if place <10:
                if place == 0:
                    blitMessage("You are the champion, {0}!".format(name),cyan,blue,display_width/2,display_size*0.4475,36, False)
                    if not musicing:
                        gameOverMusic = pygame.mixer.Sound("highscore.ogg")
                    if victory == red:
                        victory = cyan
                        victory_shadow = red
                    elif victory == cyan:
                        victory = red
                        victory_shadow = cyan
                    gameOverFont+=gameOverFontChange
                    if gameOverFont>= 198:
                        gameOverFontChange=-3
                    elif gameOverFont<=0:
                        gameOverFontChange=9
                    gameOverMsg = "HIGHSCORE"
                elif place == 1:
                    blitMessage("2nd Place! Runner up!",cyan,blue,display_width/2,display_size*0.4475,36, False)
                    if not musicing:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
                elif place == 2:
                    blitMessage("3rd Place! Bronze is still a medal!",cyan,blue,display_width/2,display_size*0.4475,36, False)
                    if not musicing:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
                else:
                    blitMessage("{0}th place on the leaderboard!".format(place+1),cyan,blue,display_width/2,display_size*0.4475,36, False)
                    if not musicing:
                        gameOverMusic = pygame.mixer.Sound("Who Likes to Party.ogg")
            else:
                blitMessage(messuj,cyan,blue,display_width/2,display_size*0.4475,36, False)
                if not musicing:
                    gameOverMusic = pygame.mixer.Sound("gameOverMusic.ogg")
            if not musicing:
                gameOverMusic.play(-1)
                musicing = True
            blitMessage(gameOverMsg,victory,victory_shadow,display_width/2,display_size*0.15,gameOverFont, False)
            blitMessage("PLAY AGAIN",green,purple,display_width/2,display_size*0.6,48, gameOver_options[0])
            blitMessage("LEADERBOARD",green,purple,display_width/2,display_size*0.7,48, gameOver_options[1])
            blitMessage("MAIN MENU",green,purple,display_width/2,display_size*0.8,48, gameOver_options[2])
            blitMessage("Thank you for playing!",white,purple,display_width/2,display_size*0.95,36, False)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        gameOver_options[pointer] = 0
                        pointer+=1
                        if pointer == len(gameOver_options):
                            pointer = 0
                        gameOver_options[pointer]= 1
                    elif event.key == pygame.K_UP:
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
        blitMessage("L E A D E R B O A R D",green,purple,display_width/2,display_size*0.1,72, False)
        blitMessage("PRESS BACKSPACE OR ESCAPE TO CLOSE",green,purple,display_width/2,display_size*0.935,36, False)
        y_pos=display_size*0.25
        count=1
        while not printed:
            blitMessage("of {0} mode".format(leaderboardMode),green,purple,display_width/2,display_size/6,36, False)
            if leaderboardMode == "normal":
                gameDisplay.blit(pygame.transform.rotate(arrow,180),(550,display_size/2))
            elif leaderboardMode == "special":
                gameDisplay.blit(arrow,(10,display_size/2))
            for i in range(0,10):
                if leaderboardCurrent[i][0] == name:
                    col = cyan
                    shad = blue
                else:
                    col = white
                    shad = purple
                blitMessage(str(count)+".",col,shad,120,y_pos,36, False)
                blitMessage(str(leaderboardCurrent[i][0]),col,shad,display_width*0.4,y_pos,36, False)
                blitMessage(str(leaderboardCurrent[i][1]),col,shad,(display_width/3)*2,y_pos,36, False)
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

def resetPos(block_size):
    lead_x = ((display_size/2)-(block_size/2))+20
    lead_y = ((display_size/2)-(block_size/2))
    lead_x_change = 0
    lead_y_change = 0
    lead_x_life = display_size
    return lead_x,lead_y,lead_x_change,lead_y_change,lead_x_life

def flash_num_creator(flash_num,mode):
    flash_nums = []
    if mode == "normal":
        flash_nums_min=0
        flash_nums_lim=5
    elif mode == "special":
        flash_nums_min=0
        flash_nums_lim=9
    for i in range(flash_nums_lim):
        if i != flash_num and i > flash_nums_min:
            flash_nums.append(i)
    flash_num = random.choice(flash_nums)
    return flash_num

def coord_maker(flash_num,flashGreen,flashRed,block_size):
    left_coords = [20, display_size/2-block_size/2]
    top_coords = [display_size/2-block_size/2+20, 0]
    right_coords = [display_size-block_size+20, display_size/2-block_size/2]
    bottom_coords = [display_size/2-block_size/2+20, display_size-block_size]
    flashGreen_coords = [20, display_size/2-150]
    flash_top_coords = [display_size/2-130, 0]
    flash_right_coords = [display_size-130, display_size/2-150]
    flash_bottom_coords = [display_size/2-130, display_size-150]
    death_coords = []
    if flash_num == 1:
        flash = flashGreen
        point_coords = left_coords
        flash_coords = flashGreen_coords
        death_coords.extend([top_coords,right_coords,bottom_coords])
    elif flash_num == 2:
        flash = pygame.transform.rotate(flashGreen,270)
        point_coords = top_coords
        flash_coords = flash_top_coords
        death_coords.extend([left_coords,right_coords,bottom_coords])
    elif flash_num == 3:
        flash = pygame.transform.rotate(flashGreen,180)
        point_coords = right_coords
        flash_coords = flash_right_coords
        death_coords.extend([left_coords,top_coords,bottom_coords])
    elif flash_num == 4:
        flash = pygame.transform.rotate(flashGreen,90)
        point_coords = bottom_coords
        flash_coords = flash_bottom_coords
        death_coords.extend([left_coords,top_coords,right_coords])
    elif flash_num == 5:
        flash = flashRed
        flash_coords = flashGreen_coords
        point_coords = right_coords
        death_coords.extend([left_coords,top_coords,bottom_coords])         
    elif flash_num == 6:
        flash = pygame.transform.rotate(flashRed,270)
        flash_coords = flash_top_coords
        point_coords = bottom_coords
        death_coords.extend([left_coords,top_coords,right_coords])
    elif flash_num == 7:
        flash = pygame.transform.rotate(flashRed,180)
        flash_coords = flash_right_coords
        point_coords = left_coords
        death_coords.extend([top_coords,right_coords,bottom_coords])
    elif flash_num == 8:
        flash = pygame.transform.rotate(flashRed,90)
        flash_coords = flash_bottom_coords
        point_coords = top_coords
        death_coords.extend([left_coords,right_coords,bottom_coords])    
    return flash, flash_coords, point_coords, death_coords

def blitMessage(msg,colour,shadow_colour,position,y,font_size,menuArrow):
    font = pygame.font.SysFont(None, font_size)
    screen_text = font.render(msg, True, colour)
    shadow = font.render(msg,True,shadow_colour)
    width = screen_text.get_width()
    height = screen_text.get_height()
    if menuArrow:
        menuArrow_arrow = pygame.image.load("menuArrow.png")
        arrow_width = menuArrow_arrow.get_width()
        arrow_height = menuArrow_arrow.get_height()
        gameDisplay.blit(menuArrow_arrow, [(position-width/2-arrow_width)-16,y-arrow_height/2])
        screen_text = font.render(msg,True,yellow)
        shadow = font.render(msg,True,red)
    gameDisplay.blit(shadow, [(position-width/2)+1,(y-height/2)+1])
    gameDisplay.blit(screen_text, [(position-width/2),(y-height/2)])
    
def writeToFile(name,score,written,mode,messuj):
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
        if score < int(i[1]) and name == i[0]:
            written = True
            if count+1 == 1:
                position = "1st"
            elif count+1 ==2:
                position = "2nd"
            elif count+1 ==3:
                position = "3rd"
            else:
                position = "{0}th".format(count+1)
            messuj = "Your old score is higher, you're still {0} place".format(position)
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
    return written, place, messuj

start()
pygame.quit()
quit()
