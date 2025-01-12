# Copyright (c) 2015 Distronode, Inc.
# All Rights Reserved.

from django.conf import settings
from django.core.management.base import BaseCommand
from api.main.analytics.subsystem_metrics import CallbackReceiverMetricsServer

from api.main.dispatch.control import Control
from api.main.dispatch.worker import APIConsumerRedis, CallbackBrokerWorker


class Command(BaseCommand):
    """
    Save Job Callback receiver
    Runs as a management command and receives job save events.  It then hands
    them off to worker processors (see Worker) which writes them to the database
    """

    help = 'Launch the job callback receiver'

    def add_arguments(self, parser):
        parser.add_argument('--status', dest='status', action='store_true', help='print the internal state of any running dispatchers')

    def handle(self, *arg, **options):
        if options.get('status'):
            print(Control('callback_receiver').status())
            return
        consumer = None

        CallbackReceiverMetricsServer().start()

        try:
            consumer = APIConsumerRedis(
                'callback_receiver',
                CallbackBrokerWorker(),
                queues=[getattr(settings, 'CALLBACK_QUEUE', '')],
            )
            consumer.run()
        except KeyboardInterrupt:
            print('Terminating Callback Receiver')
            if consumer:
                consumer.stop()
