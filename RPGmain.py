import pygame
import math

pygame.init()
running = True

screen = pygame.display
display = screen.set_mode((800, 600))
screen.set_caption('RPG Game')
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
menutxt = font.render('Press P to start the Game', False, (0, 0, 0))
gameovertxt = font.render('GAME OVER', False, (0, 0, 0,))
wintxt = font.render('YOU WIN', False, (0, 0, 0,))

flagimg = pygame.image.load('image/flags.png')
portalimg = pygame.image.load('image/portal.png')

playerimgr = pygame.image.load('image/knightv2 right.png')
playerimgl = pygame.image.load('image/knightv2 left.png')
healthimg = pygame.image.load('image/heart.png')
playerx = 0
playerleftx = playerx + 10
playerrightx = playerx + 36
middlex = (playerrightx + playerleftx) / 2
playery = 523
playermove = 0
gravity = 0
playerhlth = 3

swordr_img = pygame.image.load('image/sword right.png')

swordl_img = pygame.image.load('image/sword left.png')

bullet_img = pygame.image.load('image/dot.PNG')

enemyplatform = []


class enemy:
    list = []

    def __init__(self, enemy_img, enemyx, enemyy, enemymove, ablshoot):
        self.img = pygame.image.load(enemy_img)
        self.x = enemyx
        self.y = enemyy
        self.leftx = self.x
        self.rightx = self.x + 64
        self.midpx = (self.rightx + self.leftx) / 2
        self.movm = enemymove
        self.ablshoot = ablshoot
        if self.ablshoot is True:
            self.cooldown = False
            self.shoot = False
        enemy.list.append(self)

    def enemymovm(self, block):
        global playery, playermove, takedamage, takedamageleft, takedamageright
        if self.leftx < block.leftx or self.rightx > block.rightx:
            self.movm *= -1

        py = playery + 63
        if (playerrightx // 1 == self.leftx // 1 and playery <= self.y <= playery + 64) or (
                py // 1 == self.y // 1 and self.leftx <= middlex <= self.rightx - 32):
            takedamage = True
            takedamageleft = True

        elif (playerleftx // 1 == self.rightx // 1 and playery <= self.y <= playery + 64) or (
                py // 1 == self.y // 1 and self.leftx + 32 <= middlex <= self.rightx):
            takedamage = True
            takedamageright = True

        self.x += self.movm
        self.leftx = self.x
        self.rightx = self.x + 64
        self.midpx = (self.rightx + self.leftx) / 2

    def enemyshoot(self):
        global bullety, bulletx, rangex, shootleft, shootright, ncol, takedamage, takedamageleft, takedamageright
        # Coordinate of bullet before shoot
        if self.shoot == False and self.cooldown == False:
            if playery // 1 == self.y // 1 and (self.midpx // 1 - 250 < middlex // 1 < self.midpx // 1 + 250):
                self.shoot = True
                if middlex > self.midpx:
                    shootright = True
                    bulletx = self.rightx
                    rangex = 0
                    bullety = self.y + 24

                elif middlex < self.midpx:
                    shootleft = True
                    bulletx = self.leftx
                    rangex = 0
                    bullety = self.y + 24

        if self.cooldown is True:
            ncol += 1
            if ncol == 800:
                self.cooldown = False
                ncol = 0

        # Enemy shoot the bullet
        if self.shoot is True:
            display.blit(bullet_img, (bulletx, bullety))
            distance = math.sqrt(((bulletx - playerx) ** 2 + (bullety - (playery + 20)) ** 2))
            if shootleft is True:
                bulletx -= 0.4

            elif shootright is True:
                bulletx += 0.4

            rangex += 0.4

            if rangex >= 250 or distance < 32:
                if shootleft is True and distance < 32:
                    takedamage = True
                    takedamageleft = True

                elif shootright is True and distance < 32:
                    takedamage = True
                    takedamageright = True

                shootleft, shootright = False, False
                self.shoot = False
                self.cooldown = True

    def damage_enemy(self, x, y):
        distance = math.sqrt(((x - self.midpx) ** 2 + (y - self.y) ** 2))
        if distance < 27:
            enemy.delete_enemy(self)

    def delete_enemy(self):
        enemy.list.remove(self)
        for x in range(0, len(enemyplatform)):
            for y in enemyplatform[x]:
                if y == self:
                    enemyplatform[x].remove(self)


class specialenemy(enemy):
    list = []

    def __init__(self, enemy_img, enemyx, enemyy, enemymove, ablshoot, special_ability):
        super().__init__(enemy_img, enemyx, enemyy, enemymove, ablshoot)
        self.special = special_ability
        specialenemy.list.append(self)

    def activate_ability(self):
        if self.special == 'Fast':
            if playery <= self.y and 400 <= playerx <= 800:
                if self.movm > 0:
                    self.movm = 0.5

                elif self.movm < 0:
                    self.movm = -0.5

            else:
                if self.movm > 0:
                    self.movm = 0.1

                elif self.movm < 0:
                    self.movm = -0.1


# enemy_img, enemyx, enemyy, enemymove, ablshoot
enemy('image/skull.png', 310, 433, 0.1, True)
enemy('image/skull.png', 100, 383, 0.1, False)
enemy('image/skull.png', 160, 283, 0.1, True)
enemy('image/skull.png', 692, 203, 0, True)
specialenemy('image/skull.png', 400, 23, 0.1, False, 'Fast')
enemy('image/skull.png', 700, 23, 0, True)


class block:
    list = []
    listenemy = []

    def __init__(self, img, pixel, value, topy, leftx, numberofenemy):
        self.img = pygame.image.load(img)
        self.pixel = pixel
        self.value = value
        self.topy = topy
        self.boty = self.topy + 29
        self.stand = topy - 47
        self.leftx = leftx
        self.rightx = 0
        self.nthenemy = numberofenemy
        if self.nthenemy > 0:
            for x in range(0, self.nthenemy):
                block.listenemy.append(self)
        block.list.append(self)

    def constructblock(self):
        templeftx = self.leftx
        for construct in range(0, self.value):
            display.blit(self.img, (templeftx, self.topy))
            templeftx += self.pixel
        self.rightx = templeftx

    def blockp(self):
        global gravity, n_gravity, inair, jump, playermove, playery
        if jump is False:
            if self.stand // 1 == playery // 1 and (
                    self.leftx <= playerleftx <= self.rightx or self.leftx <= playerrightx <= self.rightx):
                playery //= 1
                gravity = 0
                inair = False

        if self.boty // 1 == playery // 1 and (
                self.leftx <= playerleftx <= self.rightx or self.leftx <= playerrightx <= self.rightx):
            jump = False
            gravity = 0
            n_gravity = 0

        if self.stand < playery < self.boty and (
                self.leftx <= playerleftx <= self.rightx or self.leftx <= playerrightx <= self.rightx):
            playermove = 0


# img, pixel, value, topy, leftx, nthenemy
block('image/grass 32 pixel.png', 32, 25, 570, 0, 0)
block('image/grass 32 pixel.png', 32, 10, 480, 300, 1)
block('image/grass 32 pixel.png', 32, 5, 430, 80, 1)
block('image/grass 32 pixel.png', 32, 8, 330, 140, 1)
block('image/grass 32 pixel.png', 32, 2, 250, 400, 0)
block('image/grass 32 pixel.png', 32, 2, 250, 530, 0)
block('image/grass 32 pixel.png', 32, 5, 250, 660, 1)
block('image/grass 32 pixel.png', 32, 8, 150, 0, 0)
block('image/grass 32 pixel.png', 32, 2, 100, 280, 0)
block('image/grass 32 pixel.png', 32, 13, 70, 400, 2)

for x in range(0, len(block.listenemy)):
    enemyplatform.append([])
    enemyplatform[x].append(enemy.list[x])


def playertakedamage():
    global playermove, takedamage, takedamagemove, takedamageleft, takedamageright, playerhlth
    if takedamagemove == 0:
        playerhlth -= 1

    if takedamagemove != 0:
        if takedamageleft is True:
            playermove = -0.5
        elif takedamageright is True:
            playermove = 0.5

    takedamagemove += 1
    if takedamagemove == 200:
        takedamage = False
        takedamageleft = False
        takedamageright = False
        takedamagemove = 0
        playermove = 0


def winorgameover(txt):
    global timestop, running, gamestart
    while True:
        display.fill((0, 255, 255))
        display.blit(txt, (275, 200))

        for x in block.list:
            block.constructblock(x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        timestop += 1
        if timestop == 3000:
            timestop = 0
            gamestart = False
            reset()
            break

        screen.update()


def reset():
    global playerx, playery, playermove, playerhlth, n_gravity, takedamage, takedamageleft, takedamageright, takedamagemove, jump, left, right, inair
    playerx = 0
    playery = 523
    playermove = 0
    playerhlth = 3
    n_gravity = 0
    takedamagemove = 0
    jump = False
    left, right = False, True
    inair = False
    takedamage = False
    takedamageleft, takedamageright = False, False
    enemy.list.clear()
    enemy('image/skull.png', 310, 433, 0.1, True)
    enemy('image/skull.png', 100, 383, 0.1, False)
    enemy('image/skull.png', 160, 283, 0.1, True)
    enemy('image/skull.png', 692, 203, 0, True)
    specialenemy('image/skull.png', 400, 23, 0.1, False, 'Fast')
    enemy('image/skull.png', 700, 23, 0, True)
    enemyplatform.clear()
    for x in range(0, len(block.listenemy)):
        enemyplatform.append([])
        enemyplatform[x].append(enemy.list[x])


n_gravity = 0
takedamagemove = 0
sn = 0
jump = False
left, right = False, True
inair = False
takedamage = False
takedamageleft, takedamageright = False, False
sword = False
bulletx, bullety, rangex = None, None, None
shootleft, shootright = False, False
ncol = 0
gamestart = False
timestop = 0

while running:
    display.fill((0, 255, 255))

    block.constructblock(block.list[0])

    display.blit(menutxt, (200, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_p:
                gamestart = True

    screen.update()

    while gamestart:
        display.fill((0, 255, 255))
        for x in block.list:
            block.constructblock(x)

        display.blit(flagimg, (740, 23))
        display.blit(portalimg, (734, 203))
        display.blit(portalimg, (-10, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gamestart = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    gamestart = False

                if event.key == pygame.K_a and takedamage is False:
                    playermove = -0.25
                    left = True
                    right = False

                if event.key == pygame.K_d and takedamage is False:
                    playermove = 0.25
                    left = False
                    right = True

                if event.key == pygame.K_w and inair is False and takedamage is False:
                    jump = True
                    gravity = -0.3

                if event.key == pygame.K_SPACE and sword is False:
                    sword = True

            if event.type == pygame.KEYUP and takedamage is False:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    playermove = 0

        inair = True
        for x in block.list:
            block.blockp(x)

        if jump is True:
            n_gravity += 1
            if n_gravity == 400:
                jump = False
                gravity = 0
                n_gravity = 0

        elif inair is True:
            gravity = 0.3

        for s in specialenemy.list:
            specialenemy.activate_ability(s)

        for x in range(0, len(block.listenemy)):
            for z in enemyplatform[x]:
                if not z:
                    break

                else:
                    enemy.enemymovm(z, block.listenemy[x])

        if takedamage is True:
            playertakedamage()

        if sword is True:
            sn += 1
            if left is True:
                swordl_lx = playerx - 27
                swordl_y = playery + 20
                display.blit(swordl_img, (swordl_lx, swordl_y))
                for x in enemy.list:
                    enemy.damage_enemy(x, swordl_lx, swordl_y)

            elif right is True:
                swordr_lx = playerx + 48
                swordr_y = playery + 20
                display.blit(swordr_img, (swordr_lx, swordr_y))
                for x in enemy.list:
                    enemy.damage_enemy(x, swordr_lx + 32, swordr_y)

            if sn == 100:
                sn = 0
                sword = False

        for n, x in enumerate(enemy.list):
            display.blit(x.img, (x.x, x.y))
            if x.ablshoot is True:
                enemy.enemyshoot(enemy.list[n])

        hlthx = 10
        for h in range(0, playerhlth):
            display.blit(healthimg, (hlthx, 10))
            hlthx += 40

        if playerhlth == 0:
            winorgameover(gameovertxt)

        if playery // 1 == 203 and playerx // 1 == 734:
            playerx = 0
            playery = 50

        if playery // 1 == 23 and playerx // 1 == 740:
            winorgameover(wintxt)

        playerx += playermove
        playerleftx = playerx + 10
        playerrightx = playerx + 36
        middlex = (playerrightx + playerleftx) / 2
        playery += gravity

        if left is True:
            display.blit(playerimgl, (playerx, playery))

        elif right is True:
            display.blit(playerimgr, (playerx, playery))

        screen.update()
