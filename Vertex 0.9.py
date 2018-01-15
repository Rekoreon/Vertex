import pygame
import time
import random
pygame.init()
display_size = 600
gameDisplay = pygame.display.set_mode((display_size+20,display_size))
pygame.display.set_caption('Vertex')
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
purple = (255,0,255)
green = (63,255,45)
cyan = (0,255,255)
blue = (0,0,255)
liquid_clear = (0,0,0,0)
clock = pygame.time.Clock()
FPS = 60

def start():
    pygame.mixer.init()
    startBool = True
    signInBool = True
    name = ""
    width = 600
    height = 600
    while startBool:
        while signInBool:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    try:
                        key = chr(event.key)
                        if name == "" or name[-1]==" ":
                            key = key.upper()
                    except ValueError:
                        key = ""
                    if key =="\r":
                        signInBool=False
                        key = ""
                    elif key =="\x08":
                        name = name[0:-1]
                        key = ""
                    if len(name) <10:
                        name+=key
            gameDisplay.fill(black)
            blitMessage("Please enter a username (Max 10 Characters):",green,purple,display_size/2,display_size*0.45,36)
            blitMessage(name,white,purple,display_size/2,display_size/2,36)
            pygame.display.update()
        gameDisplay.fill(black)
        blitMessage("V E R T E X".format(name),green,purple,display_size/2,display_size*0.1,144)
        blitMessage("Welcome, {0}!".format(name),white,purple,display_size/2,display_size*0.32,54)
        blitMessage("PRESS 1 TO PLAY NORMAL MODE",green,purple,display_size/2,display_size*0.45,48)
        blitMessage("PRESS 2 TO PLAY MIXED MODE ",green,purple,display_size/2,display_size*0.55,48)
        blitMessage("PRESS L TO VIEW LEADERBOARD",green,purple,display_size/2,display_size*0.65,48)
        blitMessage("PRESS S TO SIGN OUT",green,purple,display_size/2,display_size*0.775,36)
        blitMessage("PRESS Q TO QUIT",green,purple,display_size/2,display_size*0.85,36)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameLoop("normal",name)
                elif event.key == pygame.K_2:
                    gameLoop("mixed",name)
                elif event.key == pygame.K_q:
                    startBool= False
                elif event.key == pygame.K_l:
                    leaderboardFunc("normal",name)
                elif event.key == pygame.K_s:
                    signInBool = True
                    
def gameLoop(mode,name):
    board = pygame.image.load("board.png")
    diamond = pygame.image.load("diamond.png")
    flash_left = pygame.image.load("flash_left.png")
    flash_left_red = pygame.image.load("flash_left_red.png")
    sound = pygame.mixer.Sound("soft-hitnormalhh.wav")
    sound.set_volume(0.1)
    section_pass = pygame.mixer.Sound("sectionpass.mp3")
    section_pass.set_volume(0.1)
    music = pygame.mixer.Sound("EDM Detection Mode.wav")
    music.set_volume(0.1)
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
            written = False
            music.play()
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
        flash, flash_coords, point_coords, death_coords = coord_maker(flash_num,flash_left,flash_left_red,block_size) 
        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [0,0,20,(display_size)])
        pygame.draw.rect(gameDisplay, green, [0,display_size,20,-lead_x_life])
        gameDisplay.blit(board,(20,0))
        blitMessage("V E R T E X".format(name),green,purple,display_size*0.225,display_size*0.025,48)
        gameDisplay.blit(flash,(flash_coords[0],flash_coords[1]))
        gameDisplay.blit(diamond,(lead_x,lead_y))
        blitMessage(msg,white,purple,(display_size-(display_size/5)),10,36)
        pygame.display.update()
        if lead_x == point_coords[0] and lead_y == point_coords[1]:

            flash_num = flash_num_creator(flash_num,mode)
            score = score + 1
            msg = "Score = %s" %score
            if life_drain == 0:
                life_drain = 6
            elif life_drain < 24 and life_drain > 0 and score%10 == 0:
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
                written, place = writeToFile(name,score,written,mode)
            gameDisplay.fill(black)
            blitMessage("GAME OVER",red,cyan,display_size/2,display_size*0.1,108)
            blitMessage("Well done {0}, you got {1} points!".format(name,score),white,purple,display_size/2,display_size*0.29,36)
            if place <10:
                if place == 0:
                    blitMessage("1st Place! You are the champion!",green,purple,display_size/2,display_size*0.34,36)
                elif place == 1:
                    blitMessage("2nd Place! Runner up!",green,purple,display_size/2,display_size*0.34,36)
                elif place == 2:
                    blitMessage("3rd Place! Bronze is still a medal!",green,purple,display_size/2,display_size*0.34,36)
                else:
                    blitMessage("{0}th Place!".format(place+1),green,purple,display_size/2,display_size*0.34,36)
            else:
                blitMessage("You didn't make the leaderboard :(",white,purple,display_size/2,display_size*0.34,36)
            blitMessage("PRESS P TO PLAY AGAIN",red,cyan,display_size/2,display_size*0.45,48)
            blitMessage("PRESS M TO FOR MAIN MENU",red,cyan,display_size/2,display_size*0.55,48)
            blitMessage("PRESS L TO VIEW LEADERBOARD",red,cyan,display_size/2,display_size*0.65,48)
            blitMessage("Thank you for playing!",white,purple,display_size/2,display_size*0.8125,36)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gameOver = False
                        reset = True
                    elif event.key == pygame.K_m:
                        gameOver = False
                        gameLoopBool = False
                    elif event.key == pygame.K_l:
                        leaderboardFunc(mode,name)
        clock.tick(FPS)

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
    elif mode == "mixed":
        flash_nums_min=0
        flash_nums_lim=9
    for i in range(flash_nums_lim):
        if i != flash_num and i > flash_nums_min:
            flash_nums.append(i)
    flash_num = random.choice(flash_nums)
    return flash_num

def coord_maker(flash_num,flash_left,flash_left_red,block_size):
    left_coords = [20, display_size/2-block_size/2]
    top_coords = [display_size/2-block_size/2+20, 0]
    right_coords = [display_size-block_size+20, display_size/2-block_size/2]
    bottom_coords = [display_size/2-block_size/2+20, display_size-block_size]
    flash_left_coords = [20, display_size/2-150]
    flash_top_coords = [display_size/2-130, 0]
    flash_right_coords = [display_size-130, display_size/2-150]
    flash_bottom_coords = [display_size/2-130, display_size-150]
    death_coords = []
    if flash_num == 1:
        flash = flash_left
        point_coords = left_coords
        flash_coords = flash_left_coords
        death_coords.extend([top_coords,right_coords,bottom_coords])
    elif flash_num == 2:
        flash = pygame.transform.rotate(flash_left,270)
        point_coords = top_coords
        flash_coords = flash_top_coords
        death_coords.extend([left_coords,right_coords,bottom_coords])
    elif flash_num == 3:
        flash = pygame.transform.rotate(flash_left,180)
        point_coords = right_coords
        flash_coords = flash_right_coords
        death_coords.extend([left_coords,top_coords,bottom_coords])
    elif flash_num == 4:
        flash = pygame.transform.rotate(flash_left,90)
        point_coords = bottom_coords
        flash_coords = flash_bottom_coords
        death_coords.extend([left_coords,top_coords,right_coords])
    elif flash_num == 5:
        flash = flash_left_red
        flash_coords = flash_left_coords
        point_coords = right_coords
        death_coords.extend([left_coords,top_coords,bottom_coords])         
    elif flash_num == 6:
        flash = pygame.transform.rotate(flash_left_red,270)
        flash_coords = flash_top_coords
        point_coords = bottom_coords
        death_coords.extend([left_coords,top_coords,right_coords])
    elif flash_num == 7:
        flash = pygame.transform.rotate(flash_left_red,180)
        flash_coords = flash_right_coords
        point_coords = left_coords
        death_coords.extend([top_coords,right_coords,bottom_coords])
    elif flash_num == 8:
        flash = pygame.transform.rotate(flash_left_red,90)
        flash_coords = flash_bottom_coords
        point_coords = top_coords
        death_coords.extend([left_coords,right_coords,bottom_coords])    
    return flash, flash_coords, point_coords, death_coords

def blitMessage(msg,colour,shadow_colour,position,y,font_size):
    font = pygame.font.SysFont(None, font_size)
    screen_text = font.render(msg, True, colour)
    shadow = font.render(msg,True,shadow_colour)
    width = screen_text.get_width()
    gameDisplay.blit(shadow, [(position-width/2)+1,y+1])
    gameDisplay.blit(screen_text, [(position-width/2),y])
    
    
def writeToFile(name,score,written,mode):
    if mode == "normal":
        file = open("leaderboardNormal.txt","r")
    elif mode == "mixed":
        file = open("leaderboardMixed.txt","r")
    leaderboard = []
    for line in file:
        temp = line.split(",")
        temp[1]=int(temp[1][0:-1])
        leaderboard.append(temp)
    file.close()
    count = 0
    place = 0
    for i in leaderboard:
        if score > int(i[1]) and not written:
            leaderboard.insert(count,[name,score])
            written = True
            leaderboard = leaderboard[0:-1]
            place = count
        count+=1
    if not written:
        place = 10
        written = True
    if mode == "normal":
        file = open("leaderboardNormal.txt","w")
    elif mode == "mixed":
        file = open("leaderboardMixed.txt","w")
    for i in leaderboard:
        file.write("{0},{1}\n".format(i[0],i[1]))
    file.close()
    return written, place

def leaderboardFunc(mode,name):
    arrow = pygame.image.load("arrow.png")
    file = open("leaderboardNormal.txt","r")
    leaderboardNormal = []
    leaderboardMixed = []
    for line in file:
        temp = line.split(",")
        temp[1]=temp[1][0:-1]
        leaderboardNormal.append(temp)
    file.close()
    file = open("leaderboardMixed.txt","r")
    for line in file:
        temp = line.split(",")
        temp[1]=temp[1][0:-1]
        leaderboardMixed.append(temp)
    file.close()
    keepLeaderboarding = True
    leaderboardMode = mode
    printed = False
    while keepLeaderboarding:
        gameDisplay.fill(black)
        blitMessage("L E A D E R B O A R D",green,purple,display_size/2,display_size*0.05,72)
        blitMessage("PRESS L AGAIN TO CLOSE",green,purple,display_size/2,display_size*0.935,36)
        y_pos=display_size*0.25
        count=1
        while not printed:
            if leaderboardMode == "normal":
                blitMessage("of Normal Mode",green,purple,display_size/2,100,36)
                gameDisplay.blit(pygame.transform.rotate(arrow,180),(550,display_size/2))
                for i in range(0,10):
                    if leaderboardNormal[i][0] == name:
                        blitMessage(str(count)+".",green,purple,120,y_pos,36)
                        blitMessage(str(leaderboardNormal[i][0]),green,purple,display_size/3,y_pos,36)
                        blitMessage(str(leaderboardNormal[i][1]),green,purple,(display_size/3)*2,y_pos,36)
                        y_pos+=40
                        count+=1
                    else:
                        blitMessage(str(count)+".",white,purple,120,y_pos,36)
                        blitMessage(str(leaderboardNormal[i][0]),white,purple,display_size/3,y_pos,36)
                        blitMessage(str(leaderboardNormal[i][1]),white,purple,(display_size/3)*2,y_pos,36)
                        y_pos+=40
                        count+=1
                printed = True
                pygame.display.update()
            elif leaderboardMode == "mixed":
                blitMessage("of Mixed Mode",green,purple,display_size/2,100,36)
                gameDisplay.blit(arrow,(10,display_size/2))
                for i in range(0,10):
                    if leaderboardMixed[i][0] == name:
                        blitMessage(str(count)+".",green,purple,120,y_pos,36)
                        blitMessage(str(leaderboardMixed[i][0]),green,purple,display_size/3,y_pos,36)
                        blitMessage(str(leaderboardMixed[i][1]),green,purple,(display_size/3)*2,y_pos,36)
                        y_pos+=40
                        count+=1
                    else:
                        blitMessage(str(count)+".",white,purple,120,y_pos,36)
                        blitMessage(str(leaderboardMixed[i][0]),white,purple,display_size/3,y_pos,36)
                        blitMessage(str(leaderboardMixed[i][1]),white,purple,(display_size/3)*2,y_pos,36)
                        y_pos+=40
                        count+=1
                printed = True
                pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                     if leaderboardMode == "mixed":
                         leaderboardMode = "normal"
                         printed = False
                 elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                     if leaderboardMode == "normal":
                         leaderboardMode = "mixed"
                         printed = False
                 elif event.key == pygame.K_l:
                     keepLeaderboarding = False



start()
pygame.quit()
quit()
