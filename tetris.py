import copy
import sys
import random
import gametools
block_group = [
            [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
            ],
            [
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
            ],
            [
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
            [
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 1, 1],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
        ]

board = [
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
        ]

class tetris():

    def __init__(self, block_group, list: board):
        
        self.block_group = copy.deepcopy(block_group)
        self.empty_line = copy.deepcopy(board[1])
        self.FRAME_TIME = 1/45
        gametools.gameinitializer(self,"tetirs",board)
        self.game_init(board)
        
    #게임 시작 준비
    def game_init(self, board):
        self.board = copy.deepcopy(board)
        self.score = 0
        self.level = 1
        self.start_point_x = int(len(board[0])/2-1)
        self.start_point_y = 1
        self.x = self.start_point_x
        self.y = self.start_point_y

        self.game_state = True

        self.next_block, self.next_block_color = self.new_block()
        self.current_block, self.current_block_color = self.new_block()

    #키보드 입력값 처리 함수
    def key_handler(self, key):
        if key == self.KEY_LEFT: #왼쪽으로 움직이기
            self.move(-1, 0)
        elif key == self.KEY_RIGHT: # 오른쪽으로 움직이기
            self.move(1, 0)
        elif key == self.KEY_DOWN: #아래로 한칸 내리기
            self.move(0, 1)
        elif key == self.KEY_UP: #회전
            self.current_block=self.rotate(self.current_block, self.x, self.y)
        elif key == self.KEY_SPACE: #아래로 내리기
            while move(0, 1) :
                pass
        

        
    #블록 이동
    def move(self, move_x, move_y):
        
        if self.collision_detect(block, self.x+move_x, self.y+move_y):
            if move_y :
                self.adapt_block()
                return False
        else :
            self.x += move_x
            self.y += move_y
            return True
    
    #블록 고정시키기
    def adapt_block(self):
        for row in range(len(self.current_block)):
            for col in range(len(self.current_block[0])):
                if current_block[row][col] == 1 : 
                    self.board[ self.y + row ][ self.x + col ] = 2
        self.clear_line()

    #블록생성 함수
    def new_block(self):
        block = self.block_group[ random.randint(0, 6) ]
        color = gametools.set_color()
        for _ in range(random.randint(0,3)) : 
            self.rotate( block, self.start_point_x, self.start_point_y)
        return block, color
        



    
    #블록 회전시키기
    def rotate(self, block, x, y):
        
        #블록회전 구현
        rotate_block = copy.deepcopy(block)
        for row in range(len(block)):
            for col in range(len(block[0])):
                rotate_block[row][col] = block[col][row]
        
        
        #회전했는데 충돌이 일어나면 블록을 못돌리게 한다.
        if self.collision_detect(rotate_block, x, y):
            return block
        else:
            return rotate_block



    #블록 충돌 감지
    def collision_detect(self, block, x, y):
        for row in range(len(block)):
            for col in range(len(block[0])):
                if (self.board[y+row][x+col] == 2 or self.board[y+row][x+col] == 3) and block[row][col] == 1 : #3이나 2가 블록 1번과 겹친다면 충돌 감지 됨.
                    return True
        return False

    #블록이 바닥에 도달되면 줄을 지울 때 사용하는 함수
    def clear_line(self):
        count = 0
        remove_list=[]
        #한 줄마다 체크합니다.
        for row in range(self.y, self.y+len(self.block_group[0][0])):
            
            for col in range(len(self.board[0])) :
                if self.board[row][col] == 2 :
                    count += 1
            #보드가 꽉 차면 지울 행을 리스트에 저장합니다.
            if len(self.board)-2 == count :
                remove_list.append(row)
        
        #리스트를 지우고 추가합니다.
        for row in remove_list:
            self.board.remove(row)
            self.board.insert(1, copy.deepcopy(self.empty_line))
            add_score(len(remove_list))

    #점수 올리는 함수
    def add_score(self, stack):
        self.score += 50 + (stack-1)*20 + self.level*20 #기본 점수 + 한번에 처리한 스택 점수 + 레벨 점수

    #게임이 실제 실행되는 함수 
    def loop(self):

        import time
        self.loop_checker = 1
        while self.game_state == True : 
            start_time=time.time()
            gametools.draw(self)
            gametools.update(self)
            print("test")
            end_time = time.time()
            delta_time = end_time - start_time
            if delta_time < self.FRAME_TIME:
                time.sleep(self.FRAME_TIME - delta_time)
            self.loop_checker += 1
        



            

a=tetris(block_group,board)
a.loop()



    

    

        