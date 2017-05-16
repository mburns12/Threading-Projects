#Problem 1: At IIT's Disc Golf Range
from threading import Thread,Semaphore
from time import sleep
#makes it so each process doesn't interupt the other
Mutex_Sema = Semaphore(1)
#prevents simultaneous "extractions" from stash
Turnstile_Sema = Semaphore(1)

cartflag = 0
discs_on_field = 0
frolfnum = int(input("how many frolfers are throwing?"))
stash = int(input("how big is the stash?"))
N = int(input("how many discs fit a bucket?"))
i = 0

def frol(id):
    global cartflag, N, stash, frolfnum, discs_on_field, Mutex_Sema, Turnstile_Sema
    # frolfer
    while True:
        if(cartflag == 0):
            Turnstile_Sema.acquire()
            if(stash >= N):
                Mutex_Sema.acquire()
                print("frolfer",id,"calling for bucket")
                stash -= N                # call for bucket
                print("froler",id,"assigned",N,"discs,",stash,"discs available")
                Mutex_Sema.release()
                Turnstile_Sema.release()
                for i in range(0,N):      # for each disc in bucket,
                    Mutex_Sema.acquire()
                    discs_on_field += 1   # throw (maybe simulate with a random sleep)
                    print("frolfer",id,"threw disc",i)
                    Mutex_Sema.release()
                    sleep(1)
            else:
                cartflag = 1
                Turnstile_Sema.release()
        else:
            sleep(1)

def cart():
    global cartflag, N, stash, frolfnum, discs_on_field, Mutex_Sema, Turnstile_Sema
    # cart
    while True:
        if(cartflag == 1):
            Mutex_Sema.acquire()
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("Not enough discs in stash, sending out cart")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            stash += discs_on_field   # collect discs and deposit in stash
            print("cart has collected",discs_on_field,"discs and returned them to stash")
            print("current stash:",stash)
            discs_on_field = 0
            cartflag = 0
            Mutex_Sema.release()
            sleep(1)
car = Thread(target=cart)
car.start()

for i in range(0,frolfnum):
    fro = Thread(target=frol, args=[i])
    fro.start()
