import pygame as pg
from pygame import display
from pygame.constants import RLEACCEL
from gameFuntion import *
pg.mixer.init()


from pygame.locals import(
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)


class Element(pg.sprite.Sprite):
    # pos is a tuple includs the initial position of this object
    # shapeList is a list that contains the coordinates of the pixs of this object, assuming the initial position is (0,0)
    # color is a tuple represents the color of the object
    def __init__(self, pos, image):
        super(Element, self).__init__()
        self.initpos = pos
        self.surf = pg.image.load(image).convert()
        self.surf.set_colorkey((0, 0, 0),RLEACCEL)
        self.rect = self.surf.get_rect(center = (self.initpos))
    def update(self):
        pass

    def collision(self, sprotesGroup):
        return pg.sprite.spritecollideany(self, sprotesGroup)

class Tank(Element):
    def __init__(self, pos, image = 'Tank.png'):
        Element.__init__(self, pos, image)

    # The move of a tank
    def move(self, speed, pressed_key):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 900:
            self.rect.right = 900
        else:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-speed, 0)
            elif pressed_key[K_RIGHT]:
                self.rect.move_ip(speed, 0)
        
        
        
    def get_bullet_pos(self):
        #return a tuple which represents the coordinate of the bullet
        return ((self.rect.topleft[0]+self.rect.topright[0])/2, self.rect.topleft[1])
        
    

class Bullet(Element):
    def __init__(self, pos, image = 'bullet.png'):
        Element.__init__(self, pos, image)
    

    def update(self, speed, bricks,screen):
        #when a bullet is fired, it will mive upside 
        if self.collision(bricks):
            for i in bricks:
                if pg.sprite.collide_rect(self, i): # if the bullet hits on the brick
                    self.kill()
                    i.effect(bricks, screen)
        elif self.rect.top > 0:
            self.rect.top -= speed
        else:
            #actuall the top now is -4
            self.kill()
            

class Brick(Element):
    def __init__(self, pos, image = 'normal.png'):
        Element.__init__(self, pos, image)
    

    def update(self, speed,screen):
        if self.rect.top < 600:
            self.rect.top += speed
        else:
            self.kill()
            self.sound('lose.wav')
            crash(screen)
            
    def effect(self, bricks, screen):
        self.kill()
        self.sound('shootAlien.wav')
    
    def sound(self, file):
        pg.mixer.music.load(file)
        pg.mixer.music.play()

class BombBrick(Brick):
    def __init__(self, pos, image = 'boom.png'):
        Element.__init__(self, pos, image)

    def update(self, speed, screen):
        if self.rect.top < 600:
            self.rect.top += speed
        else:
            self.kill()
            
    def effect(self,bricks, screen):
        Brick.effect(self, bricks, screen)
        self.sound('explosion.wav')
        crash(screen)
    

class MagicBrick(Brick):
    def __init__(self, pos, image = 'coin.png'):
        Element.__init__(self, pos, image)

    #eliminate all the bricks that are in the same row
    def effect(self, bricks,screen):
        self.sound('shootCoins.wav')
        for i in bricks:
            if self.rect.centery == i.rect.centery:
                i.kill()
                
   


        
        
            
            
    


    

