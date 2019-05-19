import pygame 
from pygame.locals import *
import json
from threading import Thread, Lock, Event
from collections import deque

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
G_GAMEOVER = 0
G_WAIT = 1
G_READY = 2
G_PLAYING = 3
    
#필요 상수
        
def gameinitializer(self, title, board, start_x = 0, start_y = 0):
    self.FRAME_TIME = 1/30
    self.gamever_msg = "GAMEOVER"
    self.transparent = pygame.Color(255, 255, 255)
    self.color_map = COLOR_MAP
    self.shadow_color_map = SHADOW_COLOR_MAP

    self.key = 0
    self.key_pushed = False

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
    self.block_size = self.screen_height/(len(board))/2
    print("block size", self.block_size)
    self.gameboard_start_x, self.gameboard_start_y = start_x, start_y 
    self.clock = pygame.time.Clock()
    print("screen size {}X{}".format(self.screen_width//2, self.screen_height//2))

    #초기화
    pygame.init()
    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    self.myfont = pygame.font.SysFont('Comic Sans MS', self.screen_width//70)
    self.screen = pygame.display.set_mode((int(self.screen_width//3.5), int(self.screen_height//2)))
    pygame.display.set_caption(title)
    self.screen.fill(self.color_map[1])
    print("[sys] : pygame now be initialized.")


def set_color():
    import random
    return random.randint(0, 6)
    


###############


def draw(self):
    
    #맵그리기
    self.screen.fill((100,100,150))
    temp_y = self.gameboard_start_y

    for row in [self.board[0]]+self.board[5:]:
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
    
    temp_y = self.y
    cordinate_y = self.gameboard_start_y + (temp_y-4) * self.block_size
    for row in self.current_block :
        if temp_y <5:
            temp_y += 1
            cordinate_y=self.gameboard_start_y + (temp_y-4) * self.block_size
            continue
        else : 
            temp_x = self.gameboard_start_x + self.x*self.block_size
            for item in row :
                if item == 1 : 
                    pygame.draw.rect(self.screen, self.color_map[  self.current_block_color ], [temp_x, cordinate_y, self.block_size, self.block_size])
                temp_x += self.block_size
            temp_y += 1
            cordinate_y=self.gameboard_start_y + (temp_y-4) * self.block_size

    
        
    pygame.draw.rect(self.screen, (255,0,100,150), [score_map+10, 0, self.screen_width/8, self.screen_height/8], 10)
    pygame.draw.rect(self.screen, (255,0,100,150), [score_map+10, self.screen_height/8+10, self.screen_width/8, self.screen_height/6], 10)
    pygame.draw.rect(self.screen, (255,0,100,150), [score_map+10, self.screen_height/3.3, self.screen_width/8, self.screen_height/6], 10)
    levelsurface = self.myfont.render("level : " + str(self.level), False, (0, 0, 0))
    textsurface = self.myfont.render("score : " + str(self.score), False, (0, 0, 0))
    self.screen.blit(textsurface,(score_map+self.screen_width/32-10, 0+self.screen_height/32))
    self.screen.blit(levelsurface,(score_map+self.screen_width/32-10, 0+self.screen_height/3.5+40))
    
    
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
        print(keys)
        self.key_handler(keys)
    

    #루프가 몇번 돌았을 경우 한칸씩 내려간다.
    if self.loop_checker == 60//(1+self.level*1.6) :
        self.loop_checker = 0
        self.move(0,1)
    
    if (self.score - self.level*500) > 0 and self.score != 0 :
        self.level += 1
    
def lazy_waiting(self):
    while 1: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

# class GameBuilder():

#     def __init__(self, tetris_client):
#         import socket
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.s.connect('192.168.0.2', 9292)
#         self.addr = s.getsocketname()
#         self.tetris_client = tetris_client
#         self.player=dict()
#         self.lock = Lock()
#         self.recv_queue = queue.deque([],100)
#         import gameserver
#         self.game_state = gameserver.WAIT


#     def single_call(self):
#         self.tetris_client.loop()
#     def multi_call(self):
#         self.multi = Thread(target = self.multi_loop , args=())
#         self.multi.daemon=True
#         while game_state != gameserver.GAME_END:
            


#     def recv(self):
#         msg = self.s.recv(1024)
#         msg= self.deserialize(msg)
#         with self.lock:
#             self.recv_queue.append(msg)

    
#     ######socket 통신용#########
#     def serialize(self):
#         msg = tetris_client.serialize()
#         self.s.send(msg)
        

#     def deserialize(self, msg):
#         msg = self.s.recv(1024)
#         msg=msg.decode()
#         msg = json.loads(msg)
#         for m in msg:
#             player[m].deserialize(msg[m])
    
#     def multi_loop(self):
#         while self.game_state != gameserver.GAME_END:
#             self.recv()


            

#     def draw(self):

    