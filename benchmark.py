import shutil, os


from time import sleep, perf_counter
from threading import Thread
import random

n= int(input("How many?"))
f = open("commands.txt", "w")
f.write("7"+"\n5")
f.close()
for i in range(1,n):
    oldmask=os.umask(000)
    os.makedirs('client'+str(i+1),0o777)
    print('cp ' +'client.py ' + 'client'+str(i+1)+"/" )
    os.system('cp ' +'client.py ' + 'client'+str(i+1)+"/" )
    # os.system('mkdir '+'client'+str(i+1)+"/files")
    print('cp ' +'commands.txt ' + 'client'+str(i+1)+"/")
    os.system('cp ' +'commands.txt ' + 'client'+str(i+1)+"/" )    
    os.umask(oldmask)



def random_task():
    for i in range(5):
        k=random.randint(2,n)
        print("Transfering to this client",k)
        os.chdir(os.getcwd()+'/client'+str(k))
        os.system('python3 client.py < commands.txt')
        os.chdir("..")





def syncronous_task(n):
    for i in range(1,n):
        print("Transfering to this client",(i+1))
        os.chdir(os.getcwd()+'/client'+str(i+1))
        os.system('python3 client.py < commands.txt')
        os.chdir("..")




def task():
    
    k=random.randint(1,n)
    print("Transfering to this client",(k+1))
    os.chdir(os.getcwd()+'/client'+str(k+1))
    os.system('python3 client.py < commands.txt')
    os.chdir("..")


def async_task():
    start_time = perf_counter()


    # create two new threads
    t1 = Thread(target=task)
    t2 = Thread(target=task)
    t3 = Thread(target=task)

    # start the threads
    t1.start()
    t2.start()
    t3.start()

    # wait for the threads to complete
    t1.join()
    t2.join()
    t3.join()

    end_time = perf_counter()

    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')


syncronous_task(n)