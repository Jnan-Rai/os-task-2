"""Readers-Writers: monitor-style solution with a lock and condition variable.
Run: python readers_writers/monitor_solution.py
"""
import sys, threading, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_html, record_factory
random.seed(12)
events=[]; log_lock=threading.Lock(); record=record_factory(events,log_lock)
class ReadersWritersMonitor:
 def __init__(self):
  self.cv=threading.Condition(); self.readers=0; self.writer_active=False; self.waiting_writers=0
 def start_read(self,name):
  with self.cv:
   while self.writer_active or self.waiting_writers>0:
    record(f'{name} waits because a writer is active or queued',name,'Waiting'); self.cv.wait()
   self.readers+=1; record(f'{name} enters; active readers={self.readers}',name,'Reading',resource='Shared resource',owner='Readers')
 def end_read(self,name):
  with self.cv:
   self.readers-=1; record(f'{name} leaves; active readers={self.readers}',name,'Idle')
   if self.readers==0:self.cv.notify_all(); record('Last reader notifies waiting threads',name,'Idle',resource='Shared resource',owner='Available')
 def start_write(self,name):
  with self.cv:
   self.waiting_writers+=1
   while self.writer_active or self.readers>0:
    record(f'{name} waits for all readers/writers to leave',name,'Waiting'); self.cv.wait()
   self.waiting_writers-=1; self.writer_active=True; record(f'{name} obtains exclusive monitor access',name,'Writing',resource='Shared resource',owner=name)
 def end_write(self,name):
  with self.cv:
   self.writer_active=False; record(f'{name} releases exclusive access',name,'Idle',resource='Shared resource',owner='Available'); self.cv.notify_all()
mon=ReadersWritersMonitor(); actors=[f'Reader {i}' for i in range(1,4)]+[f'Writer {i}' for i in range(1,3)]
def reader(n):
 record(f'{n} is ready',n,'Waiting');time.sleep(random.uniform(.01,.07));mon.start_read(n);time.sleep(random.uniform(.08,.15));mon.end_read(n)
def writer(n):
 record(f'{n} is ready',n,'Waiting');time.sleep(random.uniform(.02,.08));mon.start_write(n);time.sleep(random.uniform(.09,.14));mon.end_write(n)
ts=[threading.Thread(target=reader,args=(a,)) for a in actors[:3]]+[threading.Thread(target=writer,args=(a,)) for a in actors[3:]]
for t in ts:t.start()
for t in ts:t.join()
record('Run complete: all threads have finished')
make_html('readers_writers_monitor.html','Readers-Writers · Monitor','rw',events,actors,'A monitor abstraction built with a Python Condition. The condition protects the reader count and writer flag, and waiting threads sleep until the predicate permits entry. Waiting writers are given preference over new readers.')
