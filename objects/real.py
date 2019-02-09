from objects.abstract import TWObject, Pickable
from configs import PLAYER_SIZE, JUMP_SPEED, GRAVITY, FRICTION, SPEED, PLATFORM_SIZE, E_PICKED
import pygame
import utils

OBJECTS_POOL = utils.get_objects_pool()

class DefaultBlock(TWObject):
    
    def __init__(self, point, size=[PLATFORM_SIZE]*2):
        super().__init__(point+size, )

    def update(self):
        pass
    
    def _postInit(self):
        self.image = pygame.Surface(self.sizes[2:])
        self.image.fill(pygame.Color('#ff6262'))
        
    
class JumperBlock(DefaultBlock):
    
    def _postInit(self):
        self.image = pygame.Surface(self.sizes[2:])
        self.image.fill(pygame.Color('#5faa0a'))
        
    def modifier(self, obj):
        obj.yvel -= 10
    
    

class Player(TWObject):
    
    def __init__(self, spawnpoint, uid=None):
        super().__init__(spawnpoint+PLAYER_SIZE, uid=uid)
        
    def _postInit(self):
        self.image = pygame.image.load("img/gg.png")
        self.xvel = 0
        self.yvel = 0
        self.dir = 0
        self.keydir = [0,0]
        self.onGround = False
        self.collideable = False
        self.is_player = True
        #self.rope = Rope(self)        

    def update(self):
        if self.keydir[0] != 0: 
            self.xvel = self.keydir[0]*SPEED
        if self.keydir[1] == -1 and self.onGround:
            self.yvel -= JUMP_SPEED
            self.onGround = False
        
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        self.onGround = False

        for obj in OBJECTS_POOL:
            if self != obj and pygame.sprite.collide_rect(self, obj):
                if obj.collideable:
                    self.onGround, self.xvel, self.yvel = self.collide(obj)
                    obj.modifier(self)
                if obj.pickable:
                    obj.picked_by(self)
        
        if not self.onGround:
            self.yvel += GRAVITY
        
        if abs(self.xvel) <= FRICTION:
            self.xvel = 0
        else:
            if self.xvel > 0:
                self.xvel -= FRICTION
            elif self.xvel < 0:
                self.xvel += FRICTION

    def collide(self, block):
        axis_rot = 45
        rot_coef = -3
        rot_offset_vert = axis_rot + rot_coef
        rot_offset_hrz = axis_rot - rot_coef
        f_up = 90
        f_left = 180
        f_down = 270
        entrSide = utils.u_degrees(utils.angleTo(block.rect.center, self.rect.center))
        if (f_up-rot_offset_vert) <= entrSide < (f_up+rot_offset_vert): #сверху
            self.rect.bottom = block.rect.top+1
            return (True, self.xvel, 0)
        elif (f_left-rot_offset_hrz) <= entrSide < (f_left+rot_offset_hrz): #слева
            self.rect.right = block.rect.left
            return (False, 0, self.yvel)
        elif (f_down-rot_offset_vert) <= entrSide < (f_down+rot_offset_vert): #снизу
            self.rect.top = block.rect.bottom
            if self.yvel < 0:
                return (False, self.xvel, 0)
            return (False, self.xvel, self.yvel)
        elif (360-rot_offset_hrz) <= entrSide or entrSide < rot_offset_hrz: #справа
            self.rect.left = block.rect.right
            return (False, 0, self.yvel)

###################################just becoz
    def moveAfterMouse(self, mouse_pos):
        self.angle = utils.angleTo(self.rect.center, mouse_pos)
        self.xvel, self.yvel = utils.toRectCoords(10, self.angle)

    def lookOnMouse(self, m_pos):
        self.dir = -1 if self.rect.centerx > m_pos[0] else 1


class Heart(Pickable):
    
    def _postInit(self):
        self.image = pygame.Surface(self.sizes[2:])
        self.image.fill(pygame.Color('#ff33b8'))

    def picked_by(self, entity):
        print(f'{entity} picked a heart: {self}, {self.uid}')
        pygame.event.post(pygame.event.Event(E_PICKED, author=entity, target=self))    
        
    
class GrapplingHook(TWObject):
    
    def __init__(self, owner):
        super().__init__((owner.rect.center))
        self.size = [40, 20]
        self.owner = owner
        self.image = pygame.image.load("img/rope.png")
        
    def update(self):
        self.rect.center = self.owner.rect.center
        
    def shoot(self):
        pass
    