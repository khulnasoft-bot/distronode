# Python
import logging

# API
from api.main.analytics.subsystem_metrics import DispatcherMetrics, CallbackReceiverMetrics
from api.main.dispatch.publish import task
from api.main.dispatch import get_task_queuename

logger = logging.getLogger('api.main.scheduler')


@task(queue=get_task_queuename)
def send_subsystem_metrics():
    DispatcherMetrics().send_metrics()
    CallbackReceiverMetrics().send_metrics()
