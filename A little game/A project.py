import pygame                                       #import and initiate pygame
pygame.init()

display_width = 900                 #display height
display_height = 506                #display width

display = pygame.display.set_mode((display_width, display_height))    #create screen
pygame.display.set_caption("Mini project game")           #name screen
clock = pygame.time.Clock()

char_walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]     #character animation images
char_walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
background = pygame.image.load('Mountains_background.png')       #background image
char = pygame.image.load('standing.png')

BulletSound = pygame.mixer.Sound('projectile.wav')
HitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self, x, y, width, height):            #character attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump = False
        self.jump_height = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, display):                #drawing everything causes everything to be seen
        if self.walk_count +1 >= 27:
            self.walk_count = 0

        if not (self.standing):
            if self.left:
                display.blit(char_walkLeft[self.walk_count//3], (self.x, self.y))               #one picture per 3 frames
                self.walk_count += 1
            elif self.right:
                display.blit(char_walkRight[self.walk_count//3], (self.x, self.y))              #animating the character
                self.walk_count += 1
        else:
            if self.right:
                display.blit(char_walkRight[0], (self.x, self.y))
            else:
                display.blit(char_walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(display, blue, self.hitbox, 2)

    def hit(self):
        self.x = 300
        self.y = 350
        self.walk_count = 0
        self.jump = False
        self.jump_height = 10

        lose_font = pygame.font.SysFont('arial', 100)
        text = lose_font.render('You lost', 1, red)
        display.blit(text, (display_width/2 - (text.get_width()/2), display_height/2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, colour, direction):            #the projectiles different attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self. direction = direction
        self.velocity = 10 * direction

    def draw(self, display):
        pygame.draw.circle(display, self.colour, (self.x, self.y), self.radius)         #drawing the projectile

class enemy(object):
    walk_right = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walk_left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__ (self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.velocity = 3
        self.hitbox = self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self, display):
        self.move()
        if self.visible:
            if self.walk_count +1 >= 33:
               self.walk_count = 0

            if self.velocity > 0:
                display.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                display.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1

            pygame.draw.rect(display, red, (self.hitbox[0], self.hitbox[1]-20, 45, 10))
            pygame.draw.rect(display, green, (self.hitbox[0], self.hitbox[1]-20, 50 - ((4.75)*(10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(display, red, self.hitbox, 2)

    def move(self):
        if self.velocity > 0:
            if self.x  + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1  
                self.walk_count = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walk_count = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

black = (0, 0, 0)                   #defining Colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

programIcon = pygame.image.load('icon.png')                 #set display Icon
pygame.display.set_icon(programIcon)

def UpdateDisplay():
    display.blit(background, (0, 0))     #creates a background
    text = font.render("Score " + str(score), 1, black)
    display.blit(text, (750, 10))
    character.draw(display)             #draw character
    Enemy.draw(display)
    for bullet in bullets:
        bullet.draw(display)
    pygame.display.update()                         #updating the display

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)

        display.fill(white)
        intro_font = pygame.font.SysFont('arial', 100)
        text = intro_font.render('My inferior game', 1, black)
        display.blit(text, (display_width/2 - (text.get_width()/2), display_height/2 - text.get_height()))          #shadow for the blue text

        intro_font = pygame.font.SysFont('arial', 100)
        text = intro_font.render('My inferior game', 1, (0, 0, 200))
        display.blit(text, (display_width/2 - (text.get_width()/2) - 4, display_height/2 - text.get_height() - 4))  #blue text


        if display_width/2 - 300 < mouse [0] and display_width/2 - 100 > mouse [0] and display_height/2 + 50 < mouse [1] and display_height/2 + 150 > mouse [1]:
            pygame.draw.rect(display, green, (display_width/2 - 296, display_height/2 + 54, 200, 100))

            green_button_text = pygame.font.SysFont('arial', 48)
            text = green_button_text.render('Start game', 1, black)
            display.blit(text, (display_width/2 - 291, display_height/2 + 74))
            if click[0] == 1:
                run = True
                intro = False
                   
        else:
            pygame.draw.rect(display, (0, 150, 0), (display_width/2 - 296, display_height/2 + 54, 200, 100))        #green button
            pygame.draw.rect(display, (0, 150, 0), (display_width/2 - 297, display_height/2 + 53, 200, 100))
            pygame.draw.rect(display, (0, 150, 0), (display_width/2 - 298, display_height/2 + 52, 200, 100))
            pygame.draw.rect(display, (0, 150, 0), (display_width/2 - 299, display_height/2 + 51, 200, 100))
            pygame.draw.rect(display, green, (display_width/2 - 300, display_height/2 + 50, 200, 100))

            green_button_text = pygame.font.SysFont('arial', 48)
            text = green_button_text.render('Start game', 1, black)
            display.blit(text, (display_width/2 - 295, display_height/2 + 70))

        if display_width/2 + 100 < mouse [0] and display_width/2 + 300 > mouse [0] and display_height/2 + 50 < mouse [1] and display_height/2 + 150 > mouse [1]:
            pygame.draw.rect(display, red, (display_width/2 + 96, display_height/2 + 54, 200, 100))

            red_button_text = pygame.font.SysFont('arial', 50)
            text = red_button_text.render('Exit game', 1, black)
            display.blit(text, (display_width/2 + 106, display_height/2 + 74))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(display, (150, 0, 0), (display_width/2 + 96, display_height/2 + 54, 200, 100))        # red button
            pygame.draw.rect(display, (150, 0, 0), (display_width/2 + 97, display_height/2 + 53, 200, 100))
            pygame.draw.rect(display, (150, 0, 0), (display_width/2 + 98, display_height/2 + 52, 200, 100))
            pygame.draw.rect(display, (150, 0, 0), (display_width/2 + 99, display_height/2 + 51, 200, 100))
            pygame.draw.rect(display, red, (display_width/2 + 100, display_height/2 + 50, 200, 100))

            red_button_text = pygame.font.SysFont('arial', 50)
            text = red_button_text.render('Exit game', 1, black)
            display.blit(text, (display_width/2 + 110, display_height/2 + 70))

        pygame.display.update()
        clock.tick(15)

#mainloop
font = pygame.font.SysFont("arial", 30, True, True)
character = player(300, 350, 64, 64)            #character size and starter position
Enemy = enemy(0, 350, 64, 64, 836)         #enemy path, size and starter position
fire_rate = 0
bullets = []            
intro = True

if intro == True:
    game_intro()

run = True

while run:
    clock.tick(27)              #framerate

    if Enemy.visible == True:
        if character.hitbox[1] < Enemy.hitbox[1] + Enemy.hitbox[3] and character.hitbox[1] + character.hitbox[3] > Enemy.hitbox[1]:
            if character.hitbox[0] + character.hitbox[2] > Enemy.hitbox[0] and character.hitbox[0] < Enemy.hitbox[0] + Enemy.hitbox[2]:
                character.hit()
                score = 0

    if fire_rate > 0:
        fire_rate += 1
    if fire_rate > 13:
        fire_rate = 0

    for event in pygame.event.get():    #exit game
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if Enemy.visible == True:
            if bullet.y - bullet.radius < Enemy.hitbox[1] + Enemy.hitbox[3] and bullet.y + bullet.radius > Enemy.hitbox[1]:
                if bullet.x + bullet.radius > Enemy.hitbox[0] and bullet.x - bullet.radius < Enemy.hitbox[0] + Enemy.hitbox[2]:
                    Enemy.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    HitSound.play()

        if bullet.x < 900 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))      #destroys bullets going outside the screen

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and fire_rate == 0 or keys[pygame.K_UP] and fire_rate == 0:           #buttons which fire a projectile
        if character.left:
            direction = -1
        else:
            direction = 1
        if len(bullets) < 3:           #number of projectiles/bullets there can be on the screen at the same time
            bullets.append(projectile(round(character.x + character.width//2), round(character.y + character.height//2), 6, red, direction))    
            BulletSound.play()
        fire_rate = 1

    if keys[pygame.K_LSHIFT]:        #sprint
        character.speed = 10
    else:
        character.speed = 5
    if keys[pygame.K_a] and character.x > 0 or keys[pygame.K_LEFT] and character.x > 0:                              #set controls to move
        character.x -= character.speed
        character.left = True
        character.right = False                                            #creating borders within you can move
        character.standing = False
    elif keys[pygame.K_d] and character.x < display_width-character.width or keys[pygame.K_RIGHT] and character.x < display_width-character.width:
        character.x += character.speed
        character.right = True
        character.left = False
        character.standing = False
    else:
        character.standing = True
        character.walk_count = 0

    if not (character.jump):
        if keys[pygame.K_SPACE]:
            character.jump = True               #Jumping
            character.walk_count = 0
    else:
        if character.jump_height >= -10:
            negative = 1
            if character.jump_height < 0:
                negative = -1
            character.y -= (character.jump_height ** 2)/3 * negative           #how jumping is done so it is more accurate with reality
            character.jump_height -= 1
        else:
            character.jump = False
            character.jump_height = 10
    
    UpdateDisplay()

pygame.quit()    #exit pygame
quit()
