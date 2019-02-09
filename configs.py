from pygame import USEREVENT

# screen params
SCR_W_COEFF = 30
SCR_H_COEFF = 16
PLATFORM_SIZE = 30
SCR_SIZE = (PLATFORM_SIZE*SCR_W_COEFF, PLATFORM_SIZE*SCR_H_COEFF)

# connection params 
SERV_IP = '127.0.0.1'
SERV_PORT = 31337

# game params
PLAYER_SIZE = [20,20]
SPEED = 4
JUMP_SPEED = 7
GRAVITY = 0.3
FRICTION = GRAVITY*1.5

# events
E_PICKED = USEREVENT + 1