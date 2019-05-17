import pygame 
from pygame.locals import *
import json

COLOR_MAP = [
        pygame.Color(255, 0, 0),
        pygame.Color(0, 255, 0),
        pygame.Color(0, 0, 255),
        pygame.Color(255, 255, 0),
        pygame.Color(255, 0, 255),
        pygame.Color(0, 255, 255),
        pygame.Color(255, 140, 0)
    ]
SHADOW_COLOR_MAP = [
        pygame.Color(100, 255, 0, 0),
        pygame.Color(100, 0, 255, 0),
        pygame.Color(100, 0, 0, 255),
        pygame.Color(100, 255, 255, 0),
        pygame.Color(100, 255, 0, 255),
        pygame.Color(100, 0, 255, 255),
        pygame.Color(100, 255, 140, 0)
        ]
G_WAIT = 0 
G_READY = 1
G_PLAYING = 2
G_GAMEOVER = 3
    
#필요 상수
        
def gameinitializer(self, title, board, start_x = 0, start_y = 0):
    self.FRAME_TIME = 1/30
    self.gamever_msg = "GAMEOVER"
    self.transparent = pygame.Color(255, 255, 255)
    self.color_map = COLOR_MAP
    self.shadow_color_map = SHADOW_COLOR_MAP

    self.KEY_LEFT = pygame.K_LEFT
    self.KEY_RIGHT = pygame.K_RIGHT
    self.KEY_DOWN = pygame.K_DOWN
    self.KEY_UP = pygame.K_UP
    self.KEY_SPACE = pygame.K_SPACE


    #화면 사이즈 정의
    import ctypes
    self.user32 = ctypes.windll.user32
    self.screen_width = self.user32.GetSystemMetrics(0)
    self.screen_height = self.user32.GetSystemMetrics(1)
    self.block_size = self.screen_height/len(board)/2
    print("block size", self.block_size)
    self.gameboard_start_x, self.gameboard_start_y = start_x, start_y 
    self.clock = pygame.time.Clock()
    print("screen size {}X{}".format(self.screen_width, self.screen_height))

    #초기화
    pygame.init()
    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    self.myfont = pygame.font.SysFont('Comic Sans MS', self.screen_width//70)
    self.screen = pygame.display.set_mode((int(self.screen_width/2), int(self.screen_height/2)))
    pygame.display.set_caption(title)
    self.screen.fill(self.color_map[1])
    print("[sys] : pygame now be initialized.")


def set_color():
    import random
    return random.randint(0, 6)
    



def add_socket(self):
    import socket
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect('', 9292)



######socket 통신용#########
def serialize(self):
    msg = dict()
    msg['score'] = self.score
    msg['block'] = self.current_block
    msg['color'] = self.current_block_color
    msg['map'] = self.board
    msg['x'] = self.X
    msg['y'] = self.y
    msg['y'] = self.rotate
    msg = json.dumps(msg)
    self.s.send(msg)
    

def deserialize(self, msg):
    msg = self.s.recv(1024)
    msg = json.loads(msg)
    self.score = msg['score']
    self.current_block = msg['block'] 
    self.current_block =msg['state'] 
    msg['color'] = self.current_block_color
    msg['map'] = self.board
    msg['x'] = self.X
    msg['y'] = self.y
    msg['rotate'] = self.rotate
    
###############


def draw(self):
    
    #맵그리기
    self.screen.fill((255,255,255))
    temp_y = self.gameboard_start_y
    
    for row in self.board:
        temp_x = self.gameboard_start_x
        for item in row:
            if item == 0 :
                pygame.draw.rect(self.screen, self.transparent, [temp_x, temp_y, self.block_size, self.block_size])
            elif item == 2 : 
               pygame.draw.rect(self.screen, self.color_map[2], [temp_x, temp_y, self.block_size, self.block_size])
            elif item == 3 :
               pygame.draw.rect(self.screen, (0,0,0), [temp_x, temp_y, self.block_size, self.block_size])
            temp_x += self.block_size
        temp_y += self.block_size
        score_map = temp_x

    #블록그리기
    temp_y = self.gameboard_start_y + self.y * self.block_size
    for row in self.current_block :
        temp_x = self.gameboard_start_x + self.x*self.block_size
        for item in row :
            if item == 1 : 
                pygame.draw.rect(self.screen, self.color_map[  self.current_block_color ], [temp_x, temp_y, self.block_size, self.block_size])
            temp_x += self.block_size
        temp_y += self.block_size
    
        
    pygame.draw.rect(self.screen, (255,0,100,150), [score_map+10, 0, self.screen_width/8, self.screen_height/8], 10)
    pygame.draw.rect(self.screen, (255,0,100,150), [score_map+10, self.screen_height/8+10, self.screen_width/8, self.screen_height/6], 10)
    textsurface = self.myfont.render("score : "+str(self.score), False, (0, 0, 0))
    self.screen.blit(textsurface,(score_map+self.screen_width/32-10, 0+self.screen_height/32))
    
    temp_y = self.screen_height/8+3 + self.screen_width/64
    for row in self.next_block :
        temp_x = score_map+10 + self.screen_width/64
        for item in row :
            if item == 1 : 
                pygame.draw.rect(self.screen, self.color_map[  self.next_block_color ], [temp_x, temp_y, self.screen_width/64, self.screen_width/64])
            temp_x += self.screen_width/64
        temp_y += self.screen_width/64


    pygame.display.flip()
            

def update(self):
    #키 값을 받았을때 행위 지정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        keys=pygame.key.get_pressed()
        self.key_handler(keys)

    #루프가 몇번 돌았을 경우 한칸씩 내려간다.
    if self.loop_checker == 60/(1+self.level*1.5) :
        self.loop_checker = 0
        newblock_checker = self.move(0,1)
        if newblock_checker == False : 
            self.current_block, self.current_block_color = self.next_block, self.next_block_color
            self.next_block, self.next_block_color = self.new_block()
            self.x = self.start_point_x
            self.y = self.start_point_y
            if self.collision_detect(self.current_block, self.x, self.y) :
                self.game_state = False
      
