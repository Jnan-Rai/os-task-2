"""Dining Philosophers: four philosophers, monitor-style condition-variable solution.
The monitor grants both forks atomically only when both neighbors are not eating.
Run: python dining_philosophers/monitor_solution.py
"""
import sys, threading, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_html, record_factory
random.seed(31)
events=[]; log_lock=threading.Lock(); record=record_factory(events,log_lock)
N=4; names=[f'Philosopher {i+1}' for i in range(N)]
class DiningMonitor:
 def __init__(self):self.cv=threading.Condition();self.state=['Thinking']*N
 def test(self,i):return self.state[i]=='Hungry' and self.state[(i-1)%N]!='Eating' and self.state[(i+1)%N]!='Eating'
 def take_forks(self,i):
  with self.cv:
   self.state[i]='Hungry';record(f'{names[i]} becomes hungry and asks the monitor for both forks',names[i],'Hungry')
   while not self.test(i):
    record(f'{names[i]} waits: at least one neighbor is eating',names[i],'Waiting');self.cv.wait()
   self.state[i]='Eating';record(f'Monitor grants both adjacent forks to {names[i]} atomically',names[i],'Eating',resource=f'Fork {i+1}',owner=names[i]);record(f'{names[i]} also holds Fork {(i+1)%N+1}',names[i],'Eating',resource=f'Fork {(i+1)%N+1}',owner=names[i])
 def put_forks(self,i):
  with self.cv:
   self.state[i]='Thinking';record(f'{names[i]} finishes and releases both adjacent forks',names[i],'Thinking',resource=f'Fork {i+1}',owner='Free');record(f'Fork {(i+1)%N+1} is released',names[i],'Thinking',resource=f'Fork {(i+1)%N+1}',owner='Free');self.cv.notify_all()
mon=DiningMonitor()
def philosopher(i):
 for meal in range(2):
  record(f'{names[i]} is thinking (meal {meal+1}/2)',names[i],'Thinking');time.sleep(random.uniform(.04,.11));mon.take_forks(i);time.sleep(random.uniform(.06,.12));mon.put_forks(i)
ts=[threading.Thread(target=philosopher,args=(i,)) for i in range(N)]
for t in ts:t.start()
for t in ts:t.join()
record('Run complete: all four philosophers have finished two meals each')
make_html('dining_philosophers_monitor.html','Dining Philosophers · Monitor','dining',events,names,'Exactly four philosophers share four forks. A condition-variable monitor checks both neighbors and changes a philosopher to Eating while holding the monitor lock, so adjacent philosophers cannot eat together. Deadlock is prevented; starvation is possible without a fairness policy.')
