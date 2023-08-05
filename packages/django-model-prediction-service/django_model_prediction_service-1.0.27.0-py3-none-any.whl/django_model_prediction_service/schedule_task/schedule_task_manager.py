import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler

from django_model_prediction_service.common.logger import get_logger


class ScheduleTaskManager:
    logger = get_logger()

    def __init__(self, scheduler=None):
        if scheduler:
            self.scheduler = scheduler
        else:
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()

        scheduler_log_level = 'DEBUG'
        if not self.is_debug():
            scheduler_log_level = 'INFO'
        logging.getLogger('apscheduler').setLevel(scheduler_log_level)

        self.tasks = {}

    @staticmethod
    def is_debug():
        return os.environ.get('CONFIG_SERVICE_SETTINGS_DEBUG', 'true').lower() != 'false'

    def __del__(self):
        self.scheduler.shutdown(wait=False)

    def add_task(self, name, interval, func, next_run_time=None):
        if name in self.tasks:
            self.logger.error('task <{}> already exist'.format(name))
            return False

        if next_run_time:
            self.tasks[name] = self.scheduler.add_job(func, 'interval', seconds=interval, next_run_time=next_run_time)
        else:
            self.tasks[name] = self.scheduler.add_job(func, 'interval', seconds=interval)

        return True

    def remove_task(self, name):
        if name not in self.tasks:
            self.logger.warning('Trying to remove non-existing task <{}>'.format(name))
            return False

        self.tasks[name].remove()
        del self.tasks[name]
        return True

    def pause_task(self, name):
        job = self.__get_job(name)
        if not job:
            self.logger.error('Failed pausing task <{}>'.format(name))
            return False

        job.pause()
        return True

    def resume_task(self, name):
        job = self.__get_job(name)
        if not job:
            self.logger.error('Failed resuming task <{}>'.format(name))
            return False

        job.resume()
        return True

    def __get_job(self, name):
        if name not in self.tasks:
            self.logger.warning('No such task <{}>'.format(name))
            return None

        return self.tasks[name]

    def get_task_next_run_time(self, name):
        job = self.__get_job(name)
        if not job:
            return None

        return job.next_run_time

    def get_tasks(self):
        return self.tasks
