#problem 2
from itertools import cycle
from time import sleep
from threading import Thread,Semaphore
from queue import Queue

FollowerNum = int(input("How many Followers are dancing?"))
LeaderNum = int(input("How many Leaders are dancing?"))

Danceflag = 0
On_Floorflag = 0
inlineflag = 0

LeaderQue = Queue(LeaderNum)
FollowQue = Queue(FollowerNum)

Followsema = Semaphore(0)
Leadsema = Semaphore(0)
mutex = Semaphore(1)

counter = 0

def start_music(music):
    global Danceflag, On_Floorflag, inlineflag, counter
    Danceflag = 1
    print("The Band Leader is now playing",music)
    sleep(7)
    #forced leave
    print("Music is ending, current dancers:", counter)
    Danceflag = 0
    On_Floorflag = 0
    inlineflag = 0
    while(LeaderQue.empty() == False):
        i = LeaderQue.get()
        print("Leader",i,"has went back in line")
        counter -= 1
    while(FollowQue.empty() == False):
        i = FollowQue.get()
        print("Follower",i,"has went back in line")
        counter -= 1

def end_music(music):
    print("The Band leader has ended the",music)

def enter_floor(type,id):
    global Danceflag, On_Floorflag, counter, d, d1
    if(Danceflag == 1):
        if(type == 2 and counter <= (FollowerNum+LeaderNum)):
            mutex.acquire()
            print("Follower",id,"has entered the dance floor")
            FollowQue.put(id)
            counter += 1
            #print(counter)
            mutex.release()
            sleep(1)
        if(type == 1 and counter <= (FollowerNum+LeaderNum)):
            mutex.acquire()
            print("Leader",id,"has entered the dance floor")
            LeaderQue.put(id)
            counter += 1
            #print(counter)
            mutex.release()
            sleep(1)
        On_Floorflag = 1
        sleep(1)

def dance(type,id):
    global Danceflag, On_Floorflag, inlineflag, d, d1
    a = None
    if(Danceflag == 1 and On_Floorflag == 1):
        if(type == 2):
            while(LeaderQue.empty() == True):
                sleep(2)
            a = LeaderQue.get()
            Followsema.release()
        if(type == 1):
            while(FollowQue.empty() == True):
                sleep(2)
            a = FollowQue.get()
            Leadsema.release()
            print("Follower",a,"and Leader",id,"are dancing")
        inlineflag = 1

def line_up(type,id):
    global Danceflag, On_Floorflag, inlineflag, counter, FollowerNum, LeaderNum
    if(inlineflag == 1 and counter > 0):
        if(type == 2):
            print("Follower",id,"has went back to the line")
            counter -= 1
            #print(counter)
            sleep(1)
            Followsema.acquire()
        if(type == 1 and counter > 0):
            print("Leader",id,"has went back to the line")
            counter -= 1
            #print(counter)
            sleep(1)
            Leadsema.acquire()
        sleep(1)

def Leader(id):
    type = 1
    while True:
        enter_floor(type,id)
        dance(type,id)
        line_up(type,id)

for i in range(0, LeaderNum):
    Lead = Thread(target=Leader, args=[i])
    Lead.start()

def Follower(id):
    type = 2
    while True:
        enter_floor(type,id)
        dance(type,id)
        line_up(type,id)

for i in range(0, FollowerNum):
    Follo = Thread(target=Follower, args=[i])
    Follo.start()

for music in cycle(['waltz', 'tango', 'foxtrot']):
     start_music(music)
     end_music(music)
