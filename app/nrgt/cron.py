from .models import NRGTForm
from .admin import sync_answers, sync_answersgs
from kobo.utils import get_kobo_data, normalize_data
from django.db.models import F
from datetime import datetime
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


def check_for_updates():

    queryset = NRGTForm.objects.filter(kobo_managed__eq=True).filter(last_submission_time__gt=F('last_update_time'))

    for form in queryset:

        dataset = get_kobo_data(form.auth_user, form.dataset_id)
        dataset = normalize_data(dataset)
        now = datetime.now()

        a = sync_answers(dataset, form.dataset_uuid, now)
        if a["status"] == "success":
            logger.info("Successfully updated {} answers for form {}".format(a["count"], form.dataset_name))

            b = sync_answersgs(dataset, form.dataset_uuid, now)
            if b["status"] == "success":
                logger.info("Successfully updated {} Group Score entries for form {}".format(b["count"], form.dataset_name))
            else:
                logger.error("Failed to updated Group Score entries for form {}".format(form.dataset_name))

            form.last_update_time = datetime.now()
            form.save()

        else:
            logger.error('Something went wrong!')
