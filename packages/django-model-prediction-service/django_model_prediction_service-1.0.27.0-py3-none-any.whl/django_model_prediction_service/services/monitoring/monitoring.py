from django.utils import timezone

from django_model_prediction_service import app_globals

'''
Monitoring task responsible for collecting the remaining time of all the scheduled tasks
as metrics 
'''


def monitor_schedule_tasks():
    tasks_names = app_globals.schedule_task_manager.get_tasks().keys()
    for task_name in tasks_names:
        if task_name == 'monitoring_task':
            continue  # Exclude self

        task_next_run_time = app_globals.schedule_task_manager.get_task_next_run_time(name=task_name)

        time_diff = task_next_run_time - timezone.now()

        remainig_time_seconds = int(time_diff.total_seconds())
        app_globals.metrics_registrar.gauge(name=task_name,
                                            documentation=' '.join([task_name, 'remaining seconds to next run'])).set(
            remainig_time_seconds)
