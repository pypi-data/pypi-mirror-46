from apscheduler.schedulers.tornado import TornadoScheduler
import logging

tornado_scheduler = TornadoScheduler()


def start():
    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    tornado_scheduler.start()


def shutdown():
    tornado_scheduler.shutdown()


def add_interval(job, interval, job_id=None):
    return tornado_scheduler.add_job(job, 'interval', seconds=interval, id=job_id)


def remove(job_id):
    tornado_scheduler.remove_job(job_id)
