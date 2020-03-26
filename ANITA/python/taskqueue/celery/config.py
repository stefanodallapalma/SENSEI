from __future__ import absolute_import

# Third party imports
from celery import Celery

celery = Celery('celery_test',
             broker='amqp://admin:admin@rabbitmq:5672/vhost',
             backend='rpc://',
             include=['taskqueue.celery.tasks.software_quality.projects',
                      'taskqueue.celery.tasks.software_quality.experimentations'])

