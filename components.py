import random
import pygame

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('images/scoreboard.png')
        self.rect = self.image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #super().__init__()
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = 1
        self.speed = 3
        self.moveX = 2
        self.moveY = 2
        self.slope = self.y // self.x
        self.image = pygame.image.load('images/ball.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.xy = (self.x, self.y)

    def set_moveX(self, platform1, platform2):
        """set the change in X based on number of rings left and
        how fast the ball is moving
        """
        rings = len(platform1.rings) + len(platform2.rings)

        if self.speed > 8:
            if rings < 2:
                self.moveX = self.speed + 3
            if rings < 4:
                self.moveX = self.speed - 1
            else:
                self.moveX = self.speed // rings + 3
        elif self.speed > 6:
            if rings < 4:
                self.moveX = self.speed - 1
            else:
                self.moveX = self.speed // rings + random.randint(2,4)
        else:
            if rings < 4:
                self.moveX = self.speed - 1
            else:
                self.moveX = self.speed // 2 + 1

    def set_move(self, x, y):
        if y - self.rect.y < 0:
            self.moveY = self.speed * -1
        else:
            self.moveY = self.speed

    def setX(self, x):
        self.x = x
        self.setXY(self.x, self.y)

    def setY(self, y):
        self.y = y
        self.setXY(self.x, self.y)

    def setXY(self, x, y):
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self, x, y):
        self.setXY(x, y)
        self.speed = 3
        self.moveX = 2
        self.moveY = 2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.xy = (x, y)
        #self.ring0 = pygame.image.load('images/ring0.png')
        self.ring1 = pygame.image.load('images/ring1a.png')
        self.ring2 = pygame.image.load('images/ring2.png')
        self.ring3 = pygame.image.load('images/ring3.png')
        self.rings = [self.ring1, self.ring2, self.ring3]
        self.rect = self.rings[-1].get_bounding_rect()
        self.image = self.rings[-1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y
        self.removed = False

    def remove_ring(self, player):
        if len(self.rings) > 0:
            self.removed = True
            ring_rect = self.ring1.get_rect()
            player.setX(ring_rect.centerx + self.x)
            del self.rings[-1]
            if len(self.rings) == 0:
                player.state = 'killed'

    def setX(self, x):
        self.x = x
        self.setXY(self.x, self.y)

    def setY(self, y):
        self.y = y
        self.setXY(self.x, self.y)

    def setXY(self, x, y):
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.rect.x = self.x
        self.rect.y = self.y

    def scalebypercent(self, percent):
        '''Rescale ring platform by percentage'''
        ring1rect = self.ring1.get_rect()
        new_x = ring1rect.width * percent // 100
        new_y = ring1rect.height * percent // 100
        #self.ring0 = pygame.transform.scale(self.ring0, (new_x, new_y))
        self.ring1 = pygame.transform.scale(self.ring1, (new_x, new_y))
        self.ring2 = pygame.transform.scale(self.ring2, (new_x, new_y))
        self.ring3 = pygame.transform.scale(self.ring3, (new_x, new_y))
        #self.rings = [self.ring0, self.ring1, self.ring2, self.ring3]
        self.rings = [self.ring1, self.ring2, self.ring3]
        self.rect = self.ring3.get_bounding_rect()
        self.image = self.ring3
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y

    def scalebyheight(self, newheight):
        '''Rescale platform by height'''
        ring1rect = self.ring1.get_rect()
        percent = int(newheight / ring1rect.height * 100)
        self.scalebypercent(percent)

    def scalebywidth(self, newwidth):
        '''Rescale platform by width'''
        ring1rect = self.ring1.get_rect()
        percent = int(newwidth / ring1rect.width * 100)
        self.scalebypercent(percent)

    def reset(self):
        self.rings = [self.ring1, self.ring2, self.ring3]


class Program(pygame.sprite.Sprite):
    ''' Class that defines the details of the Program (players) in the game.
        Player 1 is Tron, and Player 2 is Sark
    '''

    def __init__(self, facing, x, y, lives):
        self.facing = facing
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.state = 'stand'
        self.standImg = None
        self.crouchImg = None
        self.swingImg = None
        self.standOrig = None
        self.lives = lives

    def setX(self, x):
        self.x = x
        self.setXY(self.x, self.y)

    def setY(self, y):
        self.y = y
        self.setXY(self.x, self.y)

    def setXY(self, x, y):
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.rect.x = self.x
        self.rect.y = self.y

    def moveleft(self, platform):
        if len(platform.rings) > 0:
            ring_boundary = platform.rings[-1].get_bounding_rect()
            if self.x < ring_boundary.left + platform.x:
                self.x = ring_boundary.left + platform.x
            else:
                self.setX(self.x - 5)

    def moveright(self, platform):
        player_boundary = self.standImg.get_bounding_rect()
        if len(platform.rings) > 0:
            ring_boundary = platform.rings[-1].get_bounding_rect()
            if not self.x + player_boundary.width > ring_boundary.right + platform.x:
                self.setX(self.x + 5)

    def scalebypercent(self, percent):
        '''Rescale player by percentage'''
        standrect = self.standImg.get_rect()
        crouchrect = self.crouchImg.get_rect()
        swingrect = self.swingImg.get_rect()
        stand_x = standrect.width * percent // 100
        crouch_x = crouchrect.width * percent // 100
        swing_x = swingrect.width * percent // 100
        stand_y = standrect.height * percent // 100
        crouch_y = crouchrect.height * percent // 100
        swing_y = swingrect.height * percent // 100
        self.standOrig = pygame.transform.scale(self.standOrig, (stand_x, stand_y))
        self.standImg = pygame.transform.scale(self.standImg, (stand_x, stand_y))
        self.crouchImg = pygame.transform.scale(self.crouchImg, (crouch_x, crouch_y))
        self.swingImg = pygame.transform.scale(self.swingImg, (swing_x, swing_y))
        self.rect = self.standImg.get_bounding_rect()
        self.image = self.standImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y

    def scalebyheight(self, newheight):
        '''Rescale player by height'''
        standrect = self.standImg.get_rect()
        percent = int(newheight / standrect.height * 100)
        self.scalebypercent(percent)

    def scalebywidth(self, newwidth):
        '''Rescale player by width'''
        standrect = self.standImg.get_rect()
        percent = int(newwidth / standrect.width * 100)
        self.scalebypercent(percent)

    def rotate(self, angle):
        self.standImg = pygame.transform.rotate(self.standOrig, angle)

    def reset(self, x, y):
        self.state = 'stand'
        self.setXY(x, y)
        self.standImg = self.standOrig
        self.scalebyheight(100)


class Tron(Program):
    def __init__(self, facing, x, y, lives):
        super().__init__(facing, x, y, lives)
        self.name = 'Tron'
        self.standOrig = pygame.image.load('images/tron_stand.png')
        self.standImg = pygame.image.load('images/tron_stand.png')
        self.crouchImg = pygame.image.load('images/tron_crouch.png')
        self.swingImg = pygame.image.load('images/tron_swing.png')
        self.rect = self.standImg.get_bounding_rect()
        self.image = self.standImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y


class Sark(Program):
    def __init__(self, facing, x, y, lives):
        super().__init__(facing, x, y, lives)
        self.name = 'Sark'
        self.standOrig = pygame.image.load('images/sark_stand.png')
        self.standImg = pygame.image.load('images/sark_stand.png')
        self.crouchImg = pygame.image.load('images/sark_crouch.png')
        self.swingImg = pygame.image.load('images/sark_swing.png')
        self.rect = self.standImg.get_bounding_rect()
        self.image = self.standImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y
