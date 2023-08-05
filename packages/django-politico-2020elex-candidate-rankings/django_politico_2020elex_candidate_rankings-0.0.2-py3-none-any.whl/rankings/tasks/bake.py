import logging
import requests
from rankings.conf import settings
from rankings.models import Poll
from rankings.serializers import PollSerializer
from celery import shared_task

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def bake_poll(pk):
    poll = Poll.objects.get(pk=pk)
    data = PollSerializer(poll).data
    if settings.BAKERY_API:
        response = requests.post(
            settings.BAKERY_API,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
                "Authorization": "Token {}".format(settings.BAKERY_TOKEN),
            },
            json=data,
        )

        if response.status_code == requests.codes.ok:
            logger.info("Successfully posted candidate rankings")
        else:
            logger.error(
                "Error posting candidate rankings response {}".format(
                    response.status_code
                )
            )
    logger.info("No bakery registered")
