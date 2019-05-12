import pygame 
from pygame.locals import *


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
        
    
#필요 상수
        
def gameinitializer(self, title, board):
    self.FRAME_TIME = 1/30
    self.gamever_msg = "GAMEOVER"
    self.transparent = pygame.Color(255, 255, 255)
    self.color_map = COLOR_MAP
    self.shadow_color_map = SHADOW_COLOR_MAP

    self.KEY_LEFT = K_LEFT
    self.KEY_RIGHT = K_RIGHT
    self.KEY_DOWN = K_DOWN
    self.KEY_UP = K_UP
    self.KEY_SPACE = K_SPACE


    #화면 사이즈 정의
    import ctypes
    self.user32 = ctypes.windll.user32
    self.screen_width = self.user32.GetSystemMetrics(0)
    self.screen_height = self.user32.GetSystemMetrics(1)
    self.block_size = self.screen_height/2*len(board)+20
    self.gameboard_start_x, self.gameboard_start_y = 0, 0 
    self.clock = pygame.time.Clock()
    print("screen size {}X{}".format(self.screen_width, self.screen_height))

    #초기화
    pygame.init()
    self.screen = pygame.display.set_mode((int(self.screen_width/2), int(self.screen_height/2)))
    pygame.display.set_caption(title)
    self.screen.fill(self.color_map[1])
    print("[sys] : pygame now be initialized.")


def set_color():
    import random
    return random.randint(0, 6)
    

######socket 통신용#########
def serialize():
    pass

def deserialize(msg):
    pass
###############


def draw(self):
    temp_x, temp_y = self.gameboard_start_x, self.gameboard_start_y
    #맵그리기
    self.screen.fill((255,255,255))
    for row in self.board:
        for item in row:
            if item == 0 :
                pygame.draw.rect(self.screen, self.transparent, [temp_x, temp_y, self.block_size, self.block_size])
            elif item == 2 : 
               pygame.draw.rect(self.screen, self.color_map[2], [temp_x, temp_y, self.block_size, self.block_size])
            elif item == 3 :
               pygame.draw.rect(self.screen, self.color_map[1], [temp_x, temp_y, self.block_size, self.block_size])
            temp_x += self.block_size
        temp_y += self.block_size

    #블록그리기
    temp_x, temp_y = self.gameboard_start_x + self.x*self.block_size, self.gameboard_start_y + self.y * self.block_size
    for row in self.current_block :
        for item in row :
            if item == 1 : 
                pygame.draw.rect(self.screen, self.current_block_color, [temp_x, temp_y, self.block_size, self.block_size])
    pygame.display.flip()
            

def update(self):
    #키 값을 받았을때 행위 지정
    for event in pygame.event.get():
        self.key_handler(event)
        if event == pygame.QUIT:
            pygame.quit()

    #루프가 몇번 돌았을 경우 한칸씩 내려간다.
    if self.loop_checker == 60/1+self.level*1.5 :
        newblock_checker = self.move(0,1)
        if newblock_checker == False : 
            self.current_block, self.current_block_color = self.next_block, self.next_block_color
            self.next_block, self.next_block_color = self.new_block()
                
# def loop(self):
#     self.clock.tick(40)

#     for event in pygame.event.get()
#         if event.type == pygame.QUIT:
#             import sys
#             sys.exit()
    
    
