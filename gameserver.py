from threading import Thread, Lock, Event
import time
import os, sys
import gametools
import queue 
import socket
import json
from collections import deque


WAIT = 0
PLAYING = 1
GAME_END = 3

class GameServer() :
    def __init__(self, room_size):
        self.player = dict()
        self.port = 9292
        self.room_size = room_size
        print("server init")
    
    def run(self):
        host = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #입장용 소켓
        s.bind((host, self.port))
        s.listen(30)
        room = GameRoom(self.room_size)
        room.start()
        #방 입장
        while 1:
            print("tset1")
            if len(self.player) < self.room_size : 
                conn, addr = self.wait_client(s)
                room.add_player(conn, addr)
                print("test ")


    def wait_client(self, s):

        conn, addr = s.accept()
        print("connection :{} - connected player : {}".format(conn, addr))
        return conn, addr

    def close_connection(self, player=None):
        for key in player.keys:
            player[key].close()
    
class GameRoom(Thread):
    def __init__(self, size):
        super(GameRoom, self).__init__()
        
        
        self.game_buf =queue.deque([],100)
        self.player_statelist = dict()
        self.player = dict()
        self.lock = Lock()
        self.game_state = WAIT
        self.daemon = True
        

    def run(self):
        self.wait_start()
        self.playing_func()
        

    #{addr : }
    def wait_start(self):
        
        while  self.game_state == WAIT: 
            ready_checker = 0
            players = list(self.player)
            print("wait")
            with self.lock:
                if len(self.game_buf) : 
                    msg = self.game_buf.popleft()
                    temp_name = msg['addr']
                    temp_state = msg['state']
                    self.player_statelist[temp_name]=temp_state

                    for m in players:
                        if self.player_statelist[m] == gametools.G_READY : 
                            ready_checker += 1
            
            if ready_checker == len(self.player_statelist) : 
                import copy
                player_statelist =copy.deepcopy(self.player_statelist)
                player_statelist['state'] = gametools.G_PLAYING
                for m in players:
                    self.player[m].send_message(json.dumps(self.player_statelist))
                break
        
        self.game_state = PLAYING
        msg= {'addr' : 'server', 'state' : gametools.G_PLAYING}
        for m in players:
            self.player[m].send_message(json.dumps(msg))


    def playing_func(self):
        while  self.game_state == PLAYING: 
            
            with self.lock:
                if len(self.game_buf) : 
                    msg = self.game_buf.popleft()
                    temp_addr = msg['addr']
                    players = list(self.player)
                    if msg['state'] == gametools.G_GAMEOVER:
                        self.player_statelist[temp_addr] = gametools.G_GAMEOVER
                        gameend_checker= 0
                        for m in players:
                            if self.player_statelist[m] == gametools.G_GAMEOVER:
                                gameend_checker += 1
                        if gameend_checker == len(self.player_statelist):
                            self.game_state = GAME_END
                            
                    
                    for m in players:
                        if m != temp_addr : 
                            self.player[m].send_message(json.dumps(msg))
                
        print("shutdown room...")
    def add_player(self, conn, addr):
        self.player[addr] = GamePlayer(conn, addr, self.game_buf, self.lock)
        self.player[addr].start()
        self.player_statelist[addr] = gametools.G_WAIT
        
            

                

class GamePlayer(Thread):
    def __init__(self, conn, addr, shared_queue, lock):
        super(GamePlayer, self).__init__()
        self.conn = conn
        self.daemon = True
        self.addr = addr
        self.lock = lock
        self.to_serverbuf = deque(shared_queue, 50)

    def run(self):
        import time 
        while 1:
            start_time = time.time()
            msg = self.conn.recv(1024)
            msg= json.loads(msg)
            with self.lock:
                if msg == None:
                    msg['addr'] = self.addr
                    self.to_serverbuf.append(msg)

            delta = time.time()-start_time
            if 1/60 > delta:
                time.sleep(1/60 - delta)
        
    def close(self):
        self.conn.close()

    def send_message(self, msg):
        self.conn.send(msg.encode())

    def change_state(self, state):
        self.state = state





if __name__ == "__main__":
    print("TestT")
    server = GameServer(20)
    server.run()
    