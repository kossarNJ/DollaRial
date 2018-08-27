from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

sched = BlockingScheduler()


@sched.scheduled_job('cron', day='1st mon')
def timed_job():

    call(["python", "manage.py", "worker"])
    print("salary paid")


@sched.scheduled_job('interval', minutes=60)
def timed_job2():

    call(["python", "manage.py", "autofail"])
    print('transactions are checked')


sched.start()
