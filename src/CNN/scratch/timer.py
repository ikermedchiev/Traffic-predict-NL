import sched
import time


def repeat_every_minute(sc, t):
    next_call_time = t + 60
    sc.enterabs(next_call_time, 1, repeat_every_minute, (sc, next_call_time))
    print(time.gmtime())


s = sched.scheduler(time.time, time.sleep)
current_time = time.time()
dtime = current_time % 60
next_call_time = current_time + 60 - dtime

s.enterabs(next_call_time, 1, repeat_every_minute, (s, next_call_time))
s.run()
