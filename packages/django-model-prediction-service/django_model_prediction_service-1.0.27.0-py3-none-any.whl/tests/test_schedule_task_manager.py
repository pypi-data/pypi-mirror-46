import time
from unittest import TestCase
from unittest.mock import patch

from swiss_logger.log_utils import get_logger

from django_model_prediction_service.schedule_task.schedule_task_manager import ScheduleTaskManager
from tests.dummy_objects import DummyScheduler, DummyJob


def sleep_func1():
    time.sleep(1)


def sleep_func2():
    time.sleep(2)


class TestScheduleTaskManager(TestCase):
    logger = get_logger('TestScheduleTaskManager')

    task_name = 'arbitrary_task_name'
    interval = 5

    def setUp(self):
        self.target = ScheduleTaskManager(scheduler=DummyScheduler())

    def tearDown(self):
        del self.target  # Called after each test to make sure all scheduled tasks are removed

    def test_add_task_when_task_name_already_exists(self):
        with patch.object(DummyScheduler, 'add_job') as mock_add_job:
            res = self.target.add_task(name=self.task_name, interval=self.interval, func=sleep_func1)

            self.assertTrue(res, msg='Failed to add first task')

            # This call should yield an error log without any other effect
            res = self.target.add_task(name=self.task_name, interval=self.interval, func=sleep_func2)
            self.assertFalse(res, msg='Successfully added existing task')

            jobs = self.target.get_tasks()
            self.assertTrue(len(jobs) == 1)

            self.assertEqual(mock_add_job.call_count, 1)

    def test_remove_task(self):
        with patch.object(DummyScheduler, 'add_job') as mock_add_job:
            mock_add_job.return_value = DummyJob()
            with patch.object(DummyJob, 'remove') as mock_remove:
                res = self.target.add_task(name=self.task_name, interval=self.interval, func=sleep_func1)
                self.assertTrue(res, msg='Failed to add task')

                res = self.target.remove_task(name=self.task_name)
                self.assertTrue(res, msg='Failed to remove task')

                jobs = self.target.get_tasks()
                self.assertTrue(len(jobs) == 0)

                self.assertEqual(mock_remove.call_count, 1)

    def test_remove_task_non_existing_task(self):
        res = self.target.remove_task(name='non-existing-task')  # Yields logger error
        self.assertFalse(res, 'Successfully removed non-existing task. WHAT?!?')

        jobs = self.target.get_tasks()
        self.assertEqual(len(jobs), 0)

    def test_pause_task(self):
        with patch.object(DummyScheduler, 'add_job') as mock_add_job:
            mock_add_job.return_value = DummyJob()

            res = self.target.add_task(name=self.task_name, interval=self.interval, func=sleep_func1)
            self.assertTrue(res, msg='Failed to add task')

            with patch.object(DummyJob, 'pause') as mock_pause:
                res = self.target.pause_task(name=self.task_name)
                self.assertTrue(res, msg='Failed to pause task')

                self.assertTrue(mock_pause.call_count, 1)

    def test_pause_task_non_existing_task(self):
        res = self.target.pause_task(name='non-existing-task')  # Yields logger error
        self.assertFalse(res, 'Successfully paused non-existing task. WHAT?!?')

        jobs = self.target.get_tasks()
        self.assertEqual(len(jobs), 0)

    def test_resume_task(self):
        with patch.object(DummyScheduler, 'add_job') as mock_add_job:
            mock_add_job.return_value = DummyJob()

            res = self.target.add_task(name=self.task_name, interval=self.interval, func=sleep_func1)
            self.assertTrue(res, msg='Failed to add task')

            with patch.object(DummyJob, 'resume') as mock_resume:
                res = self.target.resume_task(name=self.task_name)
                self.assertTrue(res, msg='Failed to resume task')

                self.assertTrue(mock_resume.call_count, 1)

    def test_resume_task_non_existing_task(self):
        res = self.target.resume_task(name='non-existing-task')  # Yields logger error
        self.assertFalse(res, 'Successfully resumed non-existing task. WHAT?!?')

        jobs = self.target.get_tasks()
        self.assertEqual(len(jobs), 0)

    def test_get_task_next_runtime_non_existing_task(self):
        res = self.target.get_task_next_run_time(name='non-existing-task')  # Yields logger error
        self.assertIsNone(res, 'Successfully got task next runtime on non-existing task. WHAT?!?')

        jobs = self.target.get_tasks()
        self.assertEqual(len(jobs), 0)
