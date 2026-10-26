"""Dining Philosophers: four philosophers, semaphore-based deadlock prevention.
A room semaphore allows at most three philosophers to compete for four forks, breaking circular wait.
Run: python dining_philosophers/semaphore_solution.py
"""
import sys, threading, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import make_html, record_factory
random.seed(21)
events=[]; log_lock=threading.Lock(); record=record_factory(events,log_lock)
N=4; names=[f'Philosopher {i+1}' for i in range(N)]; forks=[threading.Semaphore(1) for _ in range(N)]; room=threading.Semaphore(N-1)
def philosopher(i):
 name=names[i]; left=i; right=(i+1)%N
 for meal in range(2):
  record(f'{name} is thinking (meal {meal+1}/2)',name,'Thinking');time.sleep(random.uniform(.04,.11))
  record(f'{name} is hungry and waits for a seat at the table',name,'Hungry')
  room.acquire(); record(f'{name} enters the room (at most three may compete for forks)',name,'Waiting')
  # Consistent left-then-right acquisition is safe here because room limits contenders to N-1.
  forks[left].acquire();record(f'{name} picks up Fork {left+1}',name,'Acquiring Forks',resource=f'Fork {left+1}',owner=name)
  forks[right].acquire();record(f'{name} picks up Fork {right+1} and can eat',name,'Eating',resource=f'Fork {right+1}',owner=name)
  time.sleep(random.uniform(.06,.12))
  record(f'{name} finishes eating and puts down Fork {right+1}',name,'Releasing Forks',resource=f'Fork {right+1}',owner='Free');forks[right].release()
  record(f'{name} puts down Fork {left+1}',name,'Thinking',resource=f'Fork {left+1}',owner='Free');forks[left].release();room.release()
ts=[threading.Thread(target=philosopher,args=(i,)) for i in range(N)]
for t in ts:t.start()
for t in ts:t.join()
record('Run complete: all four philosophers have finished two meals each')
make_html('dining_philosophers_semaphore.html','Dining Philosophers · Semaphores','dining',events,names,'Exactly four philosophers share four forks. A room semaphore limits fork contenders to three, preventing the circular-wait condition required for deadlock. Random delays make the real thread interleaving visible; fairness is not guaranteed by Python semaphores.')
