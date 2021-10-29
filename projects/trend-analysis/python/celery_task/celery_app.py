from __future__ import absolute_import

# Third party imports
from celery import Celery

celery = Celery('celery_test',
             broker='amqp://admin:admin@rabbitmq:5672/vhost',
             backend='rpc://',
             include=['celery_task.tasks.trend_analysis.market'])

