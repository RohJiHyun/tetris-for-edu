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
class NetworkConnect(Thread):
    def __init__(self, game, socket):
        Thread.__init__(self)
        self.game = game        
        self.other = []
        self.socket = socket
        self.stopped = Event()

    #thread run!
    def run(self):
        while 1 :
            if self.stopped.is_set():
                break

        msg = self.socket.recv(500)
        if msg.startswitch("ready") :
            with self.other.lock:


class GameServer() :
    def __init__(self, room_size):
        self.player = dict()
        
        self.room_size = room_size
    def run(self):
        host = ''
        s = socket(socket.AF_INET, socket.SOCK_STREAM) #입장용 소켓
        s.bind((host, port))
        s.listen(30)
        #방 입장
        while not self.is_playing[0]:
            
            if len(player) < self.size : 
                conn, addr = self.wait_client(port_number)


    def wait_client(self, port = 9192):

        conn, addr = s.accept()
        print("connection :{} - connected player : {}".format(conn, addr))
        return conn, addr

    def close_connection(self, player=None):
        for key in player.keys:
            player[key].close()
    
class GameRoom(Thread):
    def __init__(self, size):
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

            with self.lock():
                if len(self.game_buf) : 
                    msg = self.game_buf.popleft()
                    temp_name = msg['addr']
                    temp_state = msg['state']
                    self.player_statelist[temp_name]=temp_state

                    players = list(self.player)
                    for m in players:
                        if self.player_statelist[addr] == gametools.G_READY
                            ready_checker += 1

                        if m != temp_addr : 
                            
            if ready_checker == len(self.player_statelist)
                self.player_statelist['state'] = gametools.G_PLAYING
                self.player[m].send_message(json.dumps(self.player_statelist))
                break
        
        self.game_state = PLAYING
        msg= {'state' : 'playing'}
        for m in players:
            self.player[m].send_message(json.dumps(msg))


    def playing_func(self):
        while  self.game_state == PLAYING: 
            
            with self.lock():
                if len(self.game_buf) : 
                    msg = self.game_buf.popleft()
                    temp_addr = msg['addr']
                    players = list(self.player)
                    for m in players
                        if m != temp_addr : 
                            self.player[m].send_message(json.dumps(self.player_statelist))
        self.game_state = PLAYING            
    
    def add_player(self, conn, addr):
        self.player[addr] = GamePlayer(conn, gametools.G_WAIT, self.game_buf, self.lock)
        self.player[addr].start()
        self.player_statelist[addr] = gametools.G_WAIT
        
            

                

class GamePlayer(Thread):
    def __init__(self, conn, state, shared_queue,Lock: lock):
        self.conn = conn
        self.daemon = True
        self.state = state
        self.lock = lock
        self.to_serverbuf = deque(shared_queue, 50)

    def run(self):
        import time 
        while 1:
            start_time = time.time()
            msg = self.conn.recv(1024)
            msg= json.loads(msg)
            with self.lock():
                if msg == None:
                    self.msg[self.addr] = self.addr
                    self.to_serverbuf.append(msg)

            delta = time.time()-start_time
            if 1/60 > delta:
                time.sleep(1/60 - delta)
        
    def close(self)
        self.conn.close()

    def send_message(self, msg):
        self.conn.send(msg.encode())

    def change_state(self, state):
        self.state = state