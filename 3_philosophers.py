#problem 3
from time import sleep
from threading import Thread,Semaphore
from random import random
from timeit import Timer

mutex = Semaphore(1)
PhilNum = int(input("How Many Philosophers are dining?"))
MealNum = int(input("How many meals are they having?"))
savestate = MealNum
savestate2 = MealNum
savestate3 = MealNum
Phillist = []
Phillist2 = []
Phillist3 = []
forks = [Semaphore(1) for i in range (PhilNum)]
footmeals = 0

for i in range (PhilNum):
    Phillist.append(savestate)
    Phillist2.append(savestate2)
    Phillist3.append(savestate3)
#Phil states
#(0 = thinking, 1 = eating)
#forks
Forknum = PhilNum

def LeftFork(id):
    return id

def RightFork(id):
    return (id+1) % PhilNum

#footman
footman_mutex = Semaphore(PhilNum-1)

def get_forks(id):
    global footman_mutex
    footman_mutex.acquire()
    forks[RightFork(id)].acquire()
    forks[LeftFork(id)].acquire()

def put_forks(id):
    global footman_mutex
    forks[RightFork(id)].release()
    forks[LeftFork(id)].release()
    footman_mutex.release()

def footman(id):
    global savestate, Phillist
    while(Phillist[id] > 0):
        mutex.acquire()
        if(savestate > 0):
#            print("Philosopher",id,"is thinking")
            get_forks(id)
#            print("Philosopher",id,"is eating")
            put_forks(id)
            Phillist[id] -= 1
#            print(Phillist, Phillist[id])
            mutex.release()
            sleep(random())
        else:
            mutex.release()

#left-handed
left_hand_mutex = Semaphore(PhilNum-1)

def get_forks_left(id):
    global left_hand_mutex
    if(id == 0):
        left_hand_mutex.acquire()
        forks[LeftFork(id)].acquire()
        forks[RightFork(id)].acquire()
    else:
        left_hand_mutex.acquire()
        forks[RightFork(id)].acquire()
        forks[LeftFork(id)].acquire()

def put_forks_left(id):
    global left_hand_mutex
    if(id == 0):
        forks[LeftFork(id)].release()
        forks[RightFork(id)].release()
        left_hand_mutex.release()
    else:
        forks[RightFork(id)].release()
        forks[LeftFork(id)].release()
        left_hand_mutex.release()

def left_handed(id):
    global savestate2, Phillist2
    while(Phillist2[id] > 0):
        mutex.acquire()
        if(savestate2 > 0):
#            print("Philosopher",id,"is thinking")
            get_forks(id)
#            print("Philosopher",id,"is eating")
            put_forks(id)
            Phillist2[id] -= 1
#            print(Phillist2, Phillist2[id])
            mutex.release()
            sleep(random())
        else:
            mutex.release()



#Tanenbaum
tanen_mutex = Semaphore(PhilNum-1)

def tanenbaum(id):
    global savestate3, Phillist3
    State = 0
    while(Phillist3[id] > 0):
        if(State == 0):
#            print("Philosopher",id,"is thinking")
            forks[RightFork(id)].acquire()
            forks[LeftFork(id)].acquire()
            State = 1
            sleep(random())
        else:
#            print("Philosopher",id,"is eating")
            forks[RightFork(id)].release()
            forks[LeftFork(id)].release()
            Phillist3[id] -= 1
#            print(Phillist3, Phillist3[id])
            State = 0
            sleep(random())

def FootTimer():
    foot = [Thread(target=footman, args=[i]) for i in range (PhilNum)]
    for t in foot: t.start()
    for t in foot: t.join()

timer = Timer(FootTimer)
print("Time:{:0.3f}s".format(timer.timeit(100)/100))

def LeftTimer():
    LHand = [Thread(target=left_handed, args=[i]) for i in range (PhilNum)]
    for t in LHand: t.start()
    for t in LHand: t.join()

timer2 = Timer(LeftTimer)
print("Time:{:0.3f}s".format(timer2.timeit(100)/100))

def TanTimer():
    TBaum = [Thread(target=tanenbaum, args=[i]) for i in range (PhilNum)]
    for t in TBaum: t.start()
    for t in TBaum: t.join()

timer3 = Timer(TanTimer)
print("Time:{:0.3f}s".format(timer3.timeit(100)/100))
