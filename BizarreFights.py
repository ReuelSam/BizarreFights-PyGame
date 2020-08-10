import pygame
pygame.init()

screen_width = 500
screen_height = 480
 

global win


#color definitions
BLACK=(0,0,0)
GREEN=(0,255,0)
BRIGHT_GREEN=(0,200,0)
RED=(255,0,0)
BRIGHT_RED=(200,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
BRIGHT_BLUE=(0,0,200)

# Loading required images

global score,score1,score2,win,background,player1,player2,players,bullets1,bullets2,man,goblin,bullets,no_bullets

no_bullets = 3
bullets = []
bullets1 = []
bullets2 = []

bulletSound = pygame.mixer.Sound('Music/bullet.wav')
hitSound = pygame.mixer.Sound('Music/hit.wav')


## Frame Rate variables
clock = pygame.time.Clock()

score = 0
score1 = 0
score2 = 0

class Player(object):
    def __init__(self,x,y,width,height,character,frames,health):
        self.x = x                          # x position on screen from top left
        self.y = y                          # y position on screen from top left
        self.width = width                  # width of character
        self.height = height                # height of character
        self.vel = 5                        # speed with which the character moves
        self.isJump = False                 # jump motion attribute
        self.jumpCount = 10                 # height of jump
        self.left = False                   # Left character motion tracker to load required image
        self.right = False                  # Right character motion tracker to load required image
        self.walkCount = 0                  # Index in walkLeft and  walkRight lists
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = health
        self.initial_health = health
        self.visible = True
        self.frames = frames
        self.shoot = False
        self.attack = False
        self.block = False
        self.direction = "R"
        self.walkRight = [pygame.image.load('Images/Characters/%s/R%s.png' %( character, frame)) for frame in range(1, frames+1)]
        self.walkLeft = [pygame.image.load('Images/Characters/%s/L%s.png' % ( character, frame)) for frame in range(1, frames+1)]

        #if character == "Fighter" or character == "Archer" or character == "Gargoyle":
        #    print("Fighter  chosen")
        self.Rattack_frame = pygame.image.load('Images/Characters/%s/Rattack.png' % character)
        self.Rblock_frame = pygame.image.load('Images/Characters/%s/Rblock.png' % character)
        self.Rshoot_frame = pygame.image.load('Images/Characters/%s/Rshoot.png' % character)
        self.Lattack_frame = pygame.image.load('Images/Characters/%s/Lattack.png' % character)
        self.Lblock_frame = pygame.image.load('Images/Characters/%s/Lblock.png' % character)
        self.Lshoot_frame = pygame.image.load('Images/Characters/%s/Lshoot.png' % character)
##        else:
##            self.Rattack_frame = pygame.image.load('Images/Characters/%s/R1.png' % character)
##            self.Rblock_frame = pygame.image.load('Images/Characters/%s/R1.png' % character)
##            self.Rshoot_frame = pygame.image.load('Images/Characters/%s/R1.png' % character)
##            self.Lattack_frame = pygame.image.load('Images/Characters/%s/L1.png' % character)
##            self.Lblock_frame = pygame.image.load('Images/Characters/%s/L1.png' % character)
##            self.Lshoot_frame = pygame.image.load('Images/Characters/%s/L1.png' % character)
####        self.char = pygame.image.load('Images/Characters/%s/standing.png' % playerno)

        
    def draw(self,win):
        if self.walkCount + 1 >= 3*self.frames:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1

        elif self.block == True or self.shoot==True or self.attack == True:
            
            if self.block == True:
                #print("Player is blocking ",self.direction)
                if self.direction == "R":
                    win.blit(self.Rblock_frame,(self.x,self.y))
                if self.direction == "L":
                    win.blit(self.Lblock_frame,(self.x,self.y))
                    
            if self.shoot == True:
                #print("Player is shooting ",self.direction)
                if self.direction == "R":                
                    win.blit(self.Rshoot_frame,(self.x,self.y))
                if self.direction == "L":
                    win.blit(self.Lshoot_frame,(self.x,self.y))

            if self.attack == True:
                #print("Player is attacking ",self.direction)
                if self.direction == "R":
                    win.blit(self.Rattack_frame,(self.x,self.y))
                if self.direction == "L":
                    win.blit(self.Lattack_frame,(self.x,self.y))

        else:
            #win.blit(char,(self.x,self.y))
            if self.right:
                win.blit(self.walkRight[0],(self.x,self.y))
                
            else:
                win.blit(self.walkLeft[0],(self.x,self.y))


        
        

        

        

        pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1]-20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0],self.hitbox[1]-20, round(50 - ((50/self.initial_health) * (self.initial_health - self.health))), 10))
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)


    def hit(self,win):
        hitSound.play()
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
##
##        if self.visible == True:    
##            win.blit(char,(self.x,self.y))
        
        pygame.display.update()

    def punched(self,win):
        hitSound.play()
        if self.health > 1:
            self.health -= 0.1
        else:
            self.visible = False
##
##        if self.visible == True:    
##            win.blit(char,(self.x,self.y))
        
        pygame.display.update()


class Enemy(object):
##    walkRight = [pygame.image.load('Images/Characters/Enemy1/R%sE.png' % frame) for frame in range(1, 12)]
##    walkLeft = [pygame.image.load('Images/Characters/Enemy1/L%sE.png' % frame) for frame in range(1, 12)]

    def __init__(self, x, y, width, height, end, playerno, frames, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end                              # end of path of enemy
        self.path = [self.x, self.end]          
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = health
        self.initial_health = health
        self.visible = True
        self.frames = frames
        self.walkRight = [pygame.image.load('Images/Characters/%s/R%s.png' %( playerno, frame)) for frame in range(1, frames+1)]
        self.walkLeft = [pygame.image.load('Images/Characters/%s/L%s.png' % ( playerno, frame)) for frame in range(1, frames+1)]
    
    def draw(self,win):
        #print("Drawing Enemy")
        self.move()                                 # we need to move enemy before drawing

        if self.walkCount + 1 >= 3*self.frames:
            self.walkCount = 0

        if self.vel > 0:                                 # moving right
            win.blit(self.walkRight[self.walkCount // 3], (self.x,self.y))
            self.walkCount += 1
        else:                                       # moving left
            win.blit(self.walkLeft[self.walkCount // 3], (self.x,self.y))
            self.walkCount += 1

        pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1]-20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0],self.hitbox[1]-20, round(50 - ((50/self.initial_health) * (self.initial_health - self.health))), 10))

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


    def move(self):
        #print("Enemy Moving")
        if man.visible:
            if self.vel > 0:                            # if moving right
                if self.x  + self.vel < self.path[1]:   # if before end point
                    if man.hitbox[0] >= self.hitbox[0] + self.hitbox[2] or man.hitbox[0] + man.hitbox[2] <= self.hitbox[0]:
                        self.x += self.vel
                    elif man.hitbox[1]-man.hitbox[3] > goblin.hitbox[3] and man.isJump == True:
                        self.x += self.vel
                    else:
                        if man.visible == True:
                            man.hit(win)
                else:                                   # if past end point
                    self.vel *= -1                      # change direction by negating velocity
                    self.walkCount = 0                  # set walkCount to zero
                    
            else:                                       # if moving left
                
                if self.x  - self.vel > self.path[0]:   # if reached start point
                    if man.hitbox[0] >= self.hitbox[0] + self.hitbox[2] or man.hitbox[0] + man.hitbox[2] <= self.hitbox[0]:    
                        self.x += self.vel                  # not minus because vel is -ve
                    elif man.hitbox[1]-man.hitbox[3] > goblin.hitbox[3] and man.isJump == True:
                        self.x += self.vel
                    else:
                        if man.visible == True:
                            man.hit(win)
                        
                            
                else:                                   # if past end point
                    self.vel *= -1                      # change direction by negating velocity
                    self.walkCount = 0                  # set walkCount to zero

##        else:
##            print("Entered")
##            if self.vel > 0:
##                print("Right")
##                win.blit(self.walkRight[0], (self.x,self.y))
##            else:
##                print("Left")
##                win.blit(self.walkLeft[0], (self.x,self.y))
##            pygame.display.update()
##            gameOver(win)
                
        

    def hit(self,win): 
        global score
        hitSound.play()
        #score += 1
        #print("Projectile hit Enemy")
        
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        pygame.draw.rect(win,(0,0,0),self.hitbox)
        pygame.display.update()

    
        



        

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius) # (...., 1)to not have circle filled in
        

def redrawGameWindow(gamemode):
    global walkCount
    global man,goblin,bullets

    if gamemode == "gamemode2":
        win.blit(background,(0,0))                      # fill the window with a picture defined above^^^^^^^^^^^^^^    
        for man in players:
            if man.visible == True:
                man.draw(win)
            else:
                gameOver(win,gamemode)
                

        text=medium_font.render("Player1 Score: " + str(score1), 1, (0,0,0))
        win.blit(text,(30, 10))

        text=medium_font.render("Player2 Score: " + str(score2), 1, (0,0,0))
        win.blit(text,(300, 10))
        
        for bullet in bullets1:
            bullet.draw(win)
            
        for bullet in bullets2:
            bullet.draw(win)
            
        pygame.display.update()                 # refresh display to show character

    else:
        
        
        win.blit(background,(0,0))                      # fill the window with a picture defined above^^^^^^^^^^^^^^    

        if man.visible == True:
            #print("Man Visible")
            man.draw(win)
        else:
            gameOver(win,gamemode)
            
        if goblin.visible == True:
            #print("Goblin Visible")
            goblin.draw(win)
        else:
            gameOver(win,gamemode)
            
        text=medium_font.render("Score: " + str(score), 1, (0,0,0))
        win.blit(text,(390, 10))
        
        for bullet in bullets:
            bullet.draw(win)
            
        pygame.display.update()                 # refresh display to show character


def gameOver(win,gamemode):
    global score1,score2,score


    if gamemode == "gamemode2":
        if player1.visible==True:
            text=large_font.render("GAME OVER. Player1 Wins!", 1, (0,0,0))
            win.blit(text,(100, 250))
        else:
            text=large_font.render("GAME OVER. Player2 Wins!", 1, (0,0,0))
            win.blit(text,(100, 250))

        score1 = 0
        score2 = 0
        
    else:
        if man.visible==False:
            text=large_font.render("GAME OVER. You Lost", 1, (0,0,0))
            win.blit(text,(100, 250))
        else:
            text=large_font.render("GAME OVER. You Win!", 1, (0,0,0))
            win.blit(text,(100, 250))

        score = 0

    button(win,"BACK TO MENU",BLACK,280,400,200,50,RED,BRIGHT_RED,main_menu,None,None,None,None,None)


# main loop
def main_pvp(gamemode,bg,character1,frames1,character2,frames2):

    
    global score1,score2,win,background,player1,player2,players,bullets1,bullets2


    background = pygame.image.load('Images/Backgrounds/'+bg)
    player1 = Player(100, 410, 64, 64,character1,frames1,10)
    player2 = Player(300, 410, 64, 64,character2,frames2,10)
    players = [player1, player2]
    bullets1 = []
    bullets2 = []
    
    win = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("First Game")    # Title of screen

    shootLoop = 0
    run = True
    while (run):
        
        clock.tick(27)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
            
        for event in pygame.event.get():        # list of all events that take place
                                                # event=whatever key is being hit/pressed
            if event.type == pygame.QUIT:       # if user hits the 'X' on top right; to close game
                main_menu(None,None,None,None,None,None)
                run=False
                
    ###     (0,0) position would describe top left of screen. not center. x and y change correspondingly

        for bullet in bullets1:
            if player2.visible == True:
                if bullet.y - bullet.radius < player2.hitbox[1] + player2.hitbox[3] and bullet.y + bullet.radius > player2.hitbox[1]:     # if the bullet is within the height of the goblin hitbox. Correct y position
                    if bullet.x + bullet.radius > player2.hitbox[0] and bullet.x - bullet.radius < player2.hitbox[0] + player2.hitbox[2]:     # if the bullet is within the width of the goblin hitbox. Correct x position
                        if player2.block == False:
                            score1+=1
                            player2.hit(win)
                            #print("Player1 shot Player2")
                        bullets1.pop(bullets1.index(bullet))
            
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets1.pop(bullets1.index(bullet))


        for bullet in bullets1:
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets1.pop(bullets1.index(bullet))
        

        keys = pygame.key.get_pressed()

        #print(pygame.K_RCTRL)
        
        ## projectile/bullets

        if player2.visible == True:
            if keys[pygame.K_RCTRL] and shootLoop == 0:
                player2.shoot = True
##                player2.attack = False
##                player2.block = False
##                if player2.direction == "R":
##                    win.blit(player2.Rshoot_frame,(player2.x,player2.y))
##                if player2.direction == "L":
##                    win.blit(player2.Lshoot_frame,(player2.x,player2.y))
                bulletSound.play()
                if player2.left:
                    facing = -1
                else:
                    facing = 1
                if len(bullets2) < no_bullets:
                    bullets2.append(projectile(round(player2.x+player2.width//2),round(player2.y+player2.height//2),6,(0,0,0), facing))
                shootLoop = 1
            else:
                player2.shoot=False

                
            # for character motion
            if keys[pygame.K_LEFT] and player2.x > player2.vel:
                player2.x -= player2.vel
                player2.left = True
                player2.right = False
                player2.standing=False
                player2.direction="L"
            elif keys[pygame.K_RIGHT] and player2.x < (screen_width - player2.width): # because coordinate is top left of character
                player2.x += player2.vel
                player2.right = True
                player2.left = False
                player2.standing=False
                player2.direction="R"
            else:
                player2.standing=True            
                player2.walkCount = 0
                
            if player2.isJump == False:              # you cannot move up or down when jumping. or jump again


            ###     UP AND DOWN MOTION REMOVED DUE TO PLATFORM GAME MOTION
            ###     check out basic_motions.py

                if keys[pygame.K_UP]:    # for jump physics. Jump acts as parabola motion. up and down at different velocity due to acceleration
                    player2.isJump = True
                    player2.right = False
                    player2.left = False
                    player2.walkCount = 0
                        
            else:
                if player2.jumpCount >= -10:
                    neg = 1                 # for upward motion
                    if player2.jumpCount < 0:
                        neg = -1            # for downward motion
                    player2.y -= (((player2.jumpCount ** 2) // 2) * neg)    # **2 for parabola path
                                                            # //2 for shorter jump
                                                            # *neg to shift from upward to downward motion
                    player2.jumpCount -= 1
                else:                       # end of jump
                    player2.isJump = False
                    player2.jumpCount = 10

        if keys[pygame.K_RSHIFT]:
            player2.attack = True
##            player2.shoot = False
##            player2.block = False
##            if player2.direction == "R":
##                win.blit(player2.Rattack_frame,(player2.x,player2.y))
##            if player2.direction == "L":
##                win.blit(player2.Lattack_frame,(player2.x,player2.y))
            
        else:
            player2.attack = False
##            player2.shoot = False
##            player2.block = False

        if keys[pygame.K_KP0]:
##            player2.attack = False
##            player2.shoot = False
            player2.block = True
##            if player2.direction == "R":
##                win.blit(player2.Rblock_frame,(player2.x,player2.y))
##            if player2.direction == "L":
##                win.blit(player2.Lblock_frame,(player2.x,player2.y))
                
        else:
##            player2.attack = False
##            player2.shoot = False
            player2.block = False
            

        if player2.attack == True:
            if player1.hitbox[0] >= player2.hitbox[0] + player2.hitbox[2] or player1.hitbox[0] + player1.hitbox[2] <= player2.hitbox[0]:
                pass
            elif player1.hitbox[1]-player1.hitbox[3] > player2.hitbox[3] and player2.isJump == True:
                pass
            else:
                if player1.visible == True and player1.block == False:
                    player1.punched(win)    


####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PLAYER1


        for bullet in bullets2:
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets2.pop(bullets2.index(bullet))



        for bullet in bullets2:
            if player1.visible == True:
                if bullet.y - bullet.radius < player1.hitbox[1] + player1.hitbox[3] and bullet.y + bullet.radius > player1.hitbox[1]:     # if the bullet is within the height of the goblin hitbox. Correct y position
                    if bullet.x + bullet.radius > player1.hitbox[0] and bullet.x - bullet.radius < player1.hitbox[0] + player1.hitbox[2]:     # if the bullet is within the width of the goblin hitbox. Correct x position
                        if player1.block == False:
                            score2+=1
                            player1.hit(win)
                            #print("Player2 shot Player1")
                        bullets2.pop(bullets2.index(bullet))
            
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets2.pop(bullets2.index(bullet))


        if player1.visible == True:
                    ## projectile/bullets
            if keys[pygame.K_LSHIFT] and shootLoop == 0:
##                player1.attack = False
                player1.shoot = True
##                player1.block = False
                

                bulletSound.play()
                if player1.left:
                    facing = -1
                else:
                    facing = 1
                if len(bullets1) < no_bullets:
                    bullets1.append(projectile(round(player1.x+player1.width//2),round(player1.y+player1.height//2),6,(0,0,0), facing))
                shootLoop = 1
            else:
                player1.shoot = False
                
            # for character motion
            if keys[pygame.K_a] and player1.x > player1.vel:
                player1.x -= player1.vel
                player1.left = True
                player1.right = False
                player1.standing=False
                player1.direction="L"
                #print("Player1 is facing ",player1.direction)
            elif keys[pygame.K_d] and player1.x < (screen_width - player1.width): # because coordinate is top left of character
                player1.x += player1.vel
                player1.right = True
                player1.left = False
                player1.standing=False
                player1.direction="R"
                #print("Player1 is facing ",player1.direction)
            else:
                player1.standing=True            
                player1.walkCount = 0
                
            if player1.isJump == False:              # you cannot move up or down when jumping. or jump again


            ###     UP AND DOWN MOTION REMOVED DUE TO PLATFORM GAME MOTION
            ###     check out basic_motions.py

                if keys[pygame.K_w]:    # for jump physics. Jump acts as parabola motion. up and down at different velocity due to acceleration
                    player1.isJump = True
                    player1.right = False
                    player1.left = False
                    player1.walkCount = 0
                        
            else:
                if player1.jumpCount >= -10:
                    neg = 1                 # for upward motion
                    if player1.jumpCount < 0:
                        neg = -1            # for downward motion
                    player1.y -= (((player1.jumpCount ** 2) // 2) * neg)    # **2 for parabola path
                                                            # //2 for shorter jump
                                                            # *neg to shift from upward to downward motion
                    player1.jumpCount -= 1
                else:                       # end of jump
                    player1.isJump = False
                    player1.jumpCount = 10        


        if keys[pygame.K_q]:
            player1.attack = True
##            player1.shoot = False
##            player1.block = False

##            if player1.direction == "R":
##                print("Player1 is attacking ",player1.direction)
##                win.blit(player1.Rattack_frame,(player1.x,player1.y))
##            if player1.direction == "L":
##                print("Player1 is attacking ",player1.direction)
##                win.blit(player1.Lattack_frame,(player1.x,player1.y))
        else:
            player1.attack = False
##            player1.shoot = False
##            player1.block = False

        if keys[pygame.K_e]:
##            player1.attack = False
##            player1.shoot = False
            player1.block = True
##            print("Player1 is blocking ",player1.direction)
##            if player1.direction == "R":
##                win.blit(player1.Rblock_frame,(player1.x,player1.y))
##            if player1.direction == "L":
##                win.blit(player1.Lblock_frame,(player1.x,player1.y))
        else:
##            player1.attack = False
##            player1.shoot = False
            player1.block = False
            

        if player1.attack == True:
            if player2.hitbox[0] >= player1.hitbox[0] + player1.hitbox[2] or player2.hitbox[0] + player2.hitbox[2] <= player1.hitbox[0]:
                pass
            elif player2.hitbox[1]-player2.hitbox[3] > player1.hitbox[3] and player1.isJump == True:
                pass
            else:
                if player2.visible == True and player2.block == False:
                    player2.punched(win)    




        redrawGameWindow(gamemode)

                

    pygame.quit()


def main_pvc(gamemode,bg,character1,frames1,character2,frames2):

    global score1,score2,win,background,man,goblin,bullet,score,bullets


    background = pygame.image.load('Images/Backgrounds/'+bg)
    man = Player(300, 410, 64, 64,character1,frames1,50)
    #goblin = Player(300, 410, 64, 64,character2,frames2)
    goblin = Enemy(50, 410, 64, 64, 400, character2,frames2,10)
    #players = [player1, player2]
    bullets = []
    #bullets2 = []
    
    win = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("First Game")    # Title of screen

    
    shootLoop = 0                           # bullet cooldown
    
    run = True
    while (run):

        clock.tick(27)

        if shootLoop > 0:                   # after first shot, shootLoop = 1
            shootLoop += 1
        if shootLoop > 3:                   # once it reaches 4, reset and we are able to shoot
            shootLoop = 0
            
        for event in pygame.event.get():        # list of all events that take place
                                                # event=whatever key is being hit/pressed
            if event.type == pygame.QUIT:       # if user hits the 'X' on top right; to close game
                main_menu(None,None,None,None,None,None)
                run=False

        ##  FOR LOOP: BULLETS
                
        for bullet in bullets:
            if goblin.visible == True:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:     # if the bullet is within the height of the goblin hitbox. Correct y position
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:     # if the bullet is within the width of the goblin hitbox. Correct x position
                        score += 1
                        goblin.hit(win)
                        bullets.pop(bullets.index(bullet))
            
            if bullet.x < screen_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        #print(pygame.K_RCTRL)
        
        ## projectile/bullets
        if keys[pygame.K_LSHIFT] and shootLoop == 0:     # cooldown shootloop value must be 0. Basic delay
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < no_bullets:
                bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0), facing))
            shootLoop = 1                       # set shootLoop to 1 on first shot

            
        # for character motion




        
        if keys[pygame.K_a] and man.x > man.vel:
            if goblin.visible == False:
                man.x -= man.vel
                man.left = True
                man.right = False
                man.standing=False
            elif man.hitbox[0] > goblin.hitbox[0] + goblin.hitbox[2] or man.hitbox[0] + man.hitbox[2] < goblin.hitbox[0]:
                man.x -= man.vel
                man.left = True
                man.right = False
                man.standing=False
            elif man.hitbox[1]-man.hitbox[3] > goblin.hitbox[3] and man.isJump == True:
                man.x -= man.vel
                man.left = True
                man.right = False
                man.standing=False
            
                
        elif keys[pygame.K_d] and man.x < (screen_width - man.width): # because coordinate is top left of character
            if goblin.visible == False:
                man.x += man.vel
                man.right = True
                man.left = False
                man.standing=False
            elif man.hitbox[0] > goblin.hitbox[0] + goblin.hitbox[2] or man.hitbox[0] + man.hitbox[2] < goblin.hitbox[0]:
                man.x += man.vel
                man.right = True
                man.left = False
                man.standing=False
            elif man.hitbox[1]-man.hitbox[3] > goblin.hitbox[3] and man.isJump == True:
                man.x += man.vel
                man.right = True
                man.left = False
                man.standing=False
            
                
        else:
            man.standing=True            
            man.walkCount = 0
            
        if man.isJump == False:              # you cannot move up or down when jumping. or jump again


        ###     UP AND DOWN MOTION REMOVED DUE TO PLATFORM GAME MOTION
        ###     check out basic_motions.py

            if keys[pygame.K_w]:    # for jump physics. Jump acts as parabola motion. up and down at different velocity due to acceleration
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
                    
        else:
            if man.jumpCount >= -10:
                neg = 1                 # for upward motion
                if man.jumpCount < 0:
                    neg = -1            # for downward motion
                man.y -= (((man.jumpCount ** 2) // 2) * neg)    # **2 for parabola path
                                                        # //2 for shorter jump
                                                        # *neg to shift from upward to downward motion
                man.jumpCount -= 1
            else:                       # end of jump
                man.isJump = False
                man.jumpCount = 10

        redrawGameWindow(gamemode)






def message_display(screen,text,x,y,size,color):
    largeText = pygame.font.SysFont("calibri",size)
    TextSurf, TextRect = text_objects(text, largeText,color)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


def text_objects(text, font,color):
    textSurface = font.render(text, 1, color)
    return textSurface, textSurface.get_rect()

def button(screen,msg,color,x,y,w,h,ic,ac,action=None,gamemode=None,bg_name=None,character1=None,frames1=None,character2=None,frames2=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            screen.fill(BLACK)

            action(gamemode,bg_name,character1,frames1,character2,frames2)
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    #smallText = pygame.font.SysFont("comicsans",20)
    textSurf, textRect = text_objects(msg, medium_font,color)
    textRect.center = ( (x+(w//2)), (y+(h//2)) )
    screen.blit(textSurf, textRect)
    
def quitgame(dummy1,dummy2,dummy3,dummy4,dummy5,dummy6): #PUT LINK TO GAME MENU HERE
    pygame.quit()

def main_menu(dummy1,dummy2,dummy3,dummy4,dummy5,dummy6):

    menu_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("Bizarre Fights")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        message_display(menu_screen,'Bizarre Fights',250,100,50,RED)

        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
        button(menu_screen,"PLAY",BLACK,150,200,200,60,BLUE,BRIGHT_BLUE,choose_gamemode,None,None,None,None,None)
        button(menu_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)


def choose_gamemode(dummy1,dummy2,dummy3,dummy4,dummy5,dummy6):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("Choose Gamemode")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        message_display(bg_screen,'Choose Background',250,100,50,RED)

        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
        button(bg_screen,"P1 vs Com",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,choose_background,"gamemode1",None,None,None,None,None)
        button(bg_screen,"P1 vs P2",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,choose_background,"gamemode2",None,None,None,None,None)

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,main_menu,None,None,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)
        

def choose_background(gamemode,dummy1,dummy2,dummy3,dummy4,dummy5):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("Choose Background")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        message_display(bg_screen,'Choose Background',250,100,50,RED)

        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
        button(bg_screen,"Forest",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,choose_player1,gamemode,"forest.jpg",None,None,None,None)
        button(bg_screen,"Meadow",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,choose_player1,gamemode,"meadow.jpg",None,None,None,None)
        button(bg_screen,"Night",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,choose_player1,gamemode,"night.jpg",None,None,None,None)
        button(bg_screen,"Colloseum",BLACK,250,260,200,60,BLUE,BRIGHT_BLUE,choose_player1,gamemode,"colloseum.jpg",None,None,None,None)

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,choose_gamemode,None,None,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)
        



        pygame.display.update()

        clock.tick(60)

def choose_player1(gamemode,bg,dummy1,dummy2,dummy3,dummy4):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("Character Selection")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        message_display(bg_screen,'Choose Player1',250,100,50,RED)

        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
        button(bg_screen,"Archer",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,choose_player2,gamemode,bg,"Archer",6,None,None)
        button(bg_screen,"Gargoyle",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,choose_player2,gamemode,bg,"Gargoyle",7,None,None)
        #button(bg_screen,"Soldier",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,choose_player2,gamemode,bg,"Soldier",3,None,None)
        button(bg_screen,"Warrior",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,choose_player2,gamemode,bg,"Warrior",9,None,None)
        button(bg_screen,"Fighter",BLACK,250,260,200,60,BLUE,BRIGHT_BLUE,choose_player2,gamemode,bg,"Fighter",4,None,None)

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,choose_background,gamemode,None,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)

def choose_player2(gamemode,bg,character1,frames1,dummy2,dummy3):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("Character Selection")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        if gamemode == "gamemode1":
            message_display(bg_screen,'Choose Enemy',250,100,50,RED)
            func = pvc_controls
            #func = main_pvc
        else:
            message_display(bg_screen,'Choose Player2',250,100,50,RED)
            func = pvp_controls
            #func = main_pvp
            
        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
        button(bg_screen,"Archer",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Archer",6)
        button(bg_screen,"Gargoyle",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Gargoyle",7)
        #button(bg_screen,"Soldier",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Soldier",3)
        button(bg_screen,"Warrior",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Warrior",9)
        button(bg_screen,"Fighter",BLACK,250,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Fighter",4)

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,choose_player1,gamemode,bg,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)   
    


def pvp_controls(gamemode,bg,character1,frames1,character2,frames2):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("PvP Controls")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        message_display(bg_screen,'Controls',250,100,50,RED)


        p1_controls = pygame.image.load('Images/Controls/player1_controls.png')
        p2_controls = pygame.image.load('Images/Controls/player2_controls.png')
        
        bg_screen.blit(p1_controls,(50,150))
        bg_screen.blit(p2_controls,(250,150))

        
        button(bg_screen,"Continue",BLACK,190,330,120,50,BLUE,BRIGHT_BLUE,main_pvp,gamemode,bg,character1,frames1,character2, frames2)
        
##        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
##        button(bg_screen,"Archer",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Archer",6)
##        button(bg_screen,"Gargoyle",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Gargoyle",7)
##        #button(bg_screen,"Soldier",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Soldier",3)
##        button(bg_screen,"Warrior",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Warrior",9)
        

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,choose_player2,gamemode,bg,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)

def pvc_controls(gamemode,bg,character1,frames1,character2,frames2):
    bg_screen = pygame.display.set_mode((screen_width, screen_height))   # setting window of size 500x500

    pygame.display.set_caption("PvP Controls")    # Title of screen
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True

        message_display(bg_screen,'Controls',250,100,50,RED)



        p1_controls = pygame.image.load('Images/Controls/player1_controls.png')
        #p2_controls = pygame.image.load('Images/Controls/player2_controls')
        
        bg_screen.blit(p1_controls,(150,150))
        #bg_screen.blit(p2_controls,(250,200))

        
        button(bg_screen,"Continue",BLACK,190,330,120,50,BLUE,BRIGHT_BLUE,main_pvc,gamemode,bg,character1,frames1,character2, frames2)
        
##        #button("vs COMP",BLACK,350,250,200,60,GREEN,BRIGHT_GREEN,vsComp)
##        button(bg_screen,"Archer",BLACK,50,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Archer",6)
##        button(bg_screen,"Gargoyle",BLACK,250,200,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Gargoyle",7)
##        #button(bg_screen,"Soldier",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Soldier",3)
##        button(bg_screen,"Warrior",BLACK,50,260,200,60,BLUE,BRIGHT_BLUE,func,gamemode,bg,character1,frames1,"Warrior",9)
        

        button(bg_screen,"BACK",BLACK,280,400,100,50,RED,BRIGHT_RED,choose_player2,gamemode,bg,None,None,None,None)
        button(bg_screen,"QUIT",BLACK,380,400,100,50,RED,BRIGHT_RED,quitgame,None,None,None,None,None,None)



        pygame.display.update()

        clock.tick(60)   



medium_font = pygame.font.SysFont('comicsans', 30)
large_font = pygame.font.SysFont('comicsans', 30)
##player1 = Player(100, 410, 64, 64,"Archer",6)
##player2 = Player(300, 410, 64, 64,"Goblin",9)
##players = [player1, player2]
##bullets1 = []
##bullets2 = []
main_menu(None,None,None,None,None,None)
