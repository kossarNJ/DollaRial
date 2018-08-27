from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():

    print("Saaalaaaary ^##############################")
    call(["python", "manage.py", "worker"])
    print('salary paid')


@sched.scheduled_job('interval', minutes=2)
def timed_job2():

    print("Trans ^##############################")
    call(["python", "manage.py", "autofail"])
    print('trans')


sched.start()
