from threading import Thread, Lock, Event
import time
import os, sys
import gametools
import queue 
import socket

from collections import deque


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



class GameRoom() :
    def __init__(self, room_size):
        self.player = dict()
        self.join_scoket = socket(socket.AF_INET, socket.SOCK_STREAM) #입장용 소켓
        self.room_size = room_size
        self.lock = Lock()
        self.is_playing = [False]
        self.init_port = 9192
    def run(self):
        port_number = self.init_port
        #방 입장
        while not self.is_playing[0]:
            
            if len(player) < self.size : 
                conn, addr = self.wait_client(port_number)

                if self.is_playing :
                    conn.close()
                else:
                    try :
                        self.player[addr] == self.player[addr]
                        print("존재하는 ip addr")
                    except KeyError :
                        self.player[addr] = GamePlay(conn, gametools.G_WAIT, self.shared_queue, Lock)
                        self.player[addr].start()
                        port_number += 1
                        print("add new player...")
        
        #게임 진행
        while is_playing[0] :
            pass
            
        self.close_connection(self.player)


    def wait_client(self, port = 9192):
        host = ''
        s.bind((host, port))
        s.listen(self.size)
        conn, addr = s.accept()
        print("connection :{} - connected player : {}".format(conn, addr))
        return conn, addr

    def close_connection(self, player=None):
        for key in player.keys:
            player[key].close()
    
class GameWork(Thread):
    def __init__(self, size):
        self.main_buffer =queue.deque([],50)
        self.statelist = [0]*size
        self.daemon = True
    def run(self):
        while True : 
            

                

class GamePlay(Thread):
    def __init__(self, conn, state, shared_queue,Lock: lock):
        self.conn = conn
        self.daemon = True
        self.state = state
        self.lock = lock
        self.buffer = []
        self.to_serverbuf = deque(shared_queue, 50)
        self.to_clientbuf = deque(buffer,50)

    def run(self):
        import time 
        while 1:
            start_time = time.time()
            msg = self.conn.recv(1024)
            
            if msg.startswith("reday"):


            delta = time.time()-start_time
            if 1/60 > delta:
                time.sleep(1/60 - delta)
        
    def close()
        self.conn.close()