import pygame                                       #import and initiate pygame
pygame.init()

display_width = 900                 #display height
display_height = 506                #display width

char_walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]     #character animation images
char_walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
background = pygame.image.load('Mountains_background.png')       #background image
char = pygame.image.load('standing.png')

class player(object):
    def __init__(self, x, y, width, height):            #character attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump = False
        self.jump_height = 9
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True

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

    def draw(self, display):
        self.move()
        if self.walk_count +1 >= 33:
            self.walk_count = 0

        if self.velocity > 0:
            display.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            display.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1

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

black = (0, 0, 0)                   #defining Colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

display = pygame.display.set_mode((display_width, display_height))    #create screen
pygame.display.set_caption("Test")           #name screen
clock = pygame.time.Clock()

programIcon = pygame.image.load('icon.png')                 #set display Icon
pygame.display.set_icon(programIcon)

def UpdateDisplay():
    display.blit(background, (0, 0))     #creates a background
    character.draw(display)             #draw character
    Enemy.draw(display)
    for bullet in bullets:
        bullet.draw(display)
    pygame.display.update()                         #updating the display

#mainloop
character = player(300, 310, 64, 64)            #character size and starter position
Enemy = enemy(0, 350, 64, 64, 836)
bullets = []            
run = True

while run:
    pygame.time.delay(27)                       #framerate
    clock.tick(27)

    for event in pygame.event.get():    #exit game
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 900 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))      #destroys bullets going outside the screen

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:           #buttons which fire a projectile
        if character.left:
            direction = -1
        else:
            direction = 1
        if len(bullets) < 10:           #number of projectiles/bullets there can be on the screen at the same time
            bullets.append(projectile(round(character.x + character.width//2), round(character.y + character.height//2), 6, red, direction))    
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
            character.right = False
            character.left = False
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
