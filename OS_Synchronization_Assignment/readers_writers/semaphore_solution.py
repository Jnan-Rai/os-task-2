"""Readers-Writers: semaphore-based, reader-preference solution.
Run: python readers_writers/semaphore_solution.py
This is reader-preference: concurrent readers share access; writers get exclusive access.
"""
import sys, threading, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_html, record_factory
random.seed(7)
events=[]; log_lock=threading.Lock(); record=record_factory(events,log_lock)
read_count=0; count_lock=threading.Semaphore(1); resource=threading.Semaphore(1)
actors=[f'Reader {i}' for i in range(1,4)]+[f'Writer {i}' for i in range(1,3)]
def reader(name):
 global read_count
 record(f'{name} is ready',name,'Waiting')
 time.sleep(random.uniform(.01,.06))
 count_lock.acquire()
 read_count+=1
 if read_count==1:
  resource.acquire(); record(f'{name} blocks writers by acquiring the resource semaphore',name,'Reading',resource='Shared resource',owner='Readers')
 else: record(f'{name} joins the active reader group',name,'Reading',resource='Shared resource',owner='Readers')
 count_lock.release()
 record(f'{name} enters the read critical section',name,'Reading')
 time.sleep(random.uniform(.08,.16))
 count_lock.acquire(); read_count-=1
 record(f'{name} leaves; active reader count is {read_count}',name,'Idle')
 if read_count==0:
  resource.release(); record('Last reader releases the shared resource',name,'Idle',resource='Shared resource',owner='Available')
 count_lock.release()
def writer(name):
 record(f'{name} is ready and requests exclusive access',name,'Waiting')
 time.sleep(random.uniform(.02,.09)); resource.acquire()
 record(f'{name} acquires the resource semaphore',name,'Writing',resource='Shared resource',owner=name)
 record(f'{name} enters the write critical section',name,'Writing')
 time.sleep(random.uniform(.09,.15))
 record(f'{name} exits the write critical section',name,'Idle',resource='Shared resource',owner='Available')
 resource.release()
threads=[threading.Thread(target=reader,args=(a,)) for a in actors[:3]]+[threading.Thread(target=writer,args=(a,)) for a in actors[3:]]
for t in threads:t.start()
for t in threads:t.join()
record('Run complete: all threads have finished')
make_html('readers_writers_semaphore.html','Readers-Writers · Semaphore','rw',events,actors,'A semaphore solution using a reader counter. Multiple readers may read together; a writer holds exclusive access. This classic reader-preference design can starve writers under a continuous stream of readers.')
