from .models import BNSForm, BNSFormPrice
from .admin import sync_answers, sync_answersnr, sync_answershhmembers, sync_answersgps, sync_answersgs, sync_price
from kobo.utils import get_kobo_data, normalize_data
from django.db.models import F
from datetime import datetime
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


def check_for_updates():

    # Update BNS Surveys
    queryset = BNSForm.objects.filter(kobo_managed__eq=True).filter(last_submission_time__gt=F('last_update_time'))
    for form in queryset:

        dataset = get_kobo_data(form.auth_user, form.dataset_id)
        dataset = normalize_data(dataset)

        now = datetime.now()

        a = sync_answers(dataset, form.dataset_uuid, now)
        if a["status"] == "success":
            logger.info("Successfully updated {} answers for form {}".format(a["count"], form.dataset_name))
            b = sync_answersgps(dataset, form.dataset_uuid, now)
            if b["status"] == "success":
                logger.info("Successfully updated {} GPS coordinates for form {}".format(b["count"], form.dataset_name))
            else:
                logger.error("Failed to updated GPS coordinates for form {}".format(form.dataset_name))

            c = sync_answersgs(dataset, form.dataset_uuid, now)
            if c["status"] == "success":
                logger.info("Successfully updated {} Goods & Service entries for form {}".format(c["count"], form.dataset_name))
            else:
                logger.error("Failed to updated Goods & Service entries for form {}".format(form.dataset_name))

            d = sync_answershhmembers(dataset, form.dataset_uuid, now)
            if d["status"] == "success":
                logger.info("Successfully updated {} household member entries for form {}".format(d["count"], form.dataset_name))
            else:
                logger.error("Failed to updated household member entries for form {}".format(form.dataset_name))

            e = sync_answersnr(dataset, form.dataset_uuid, now)
            if e["status"] == "success":
                logger.info("Successfully updated {} natural resource entries for form {}".format(d["count"], form.dataset_name))
            else:
                logger.error("Failed to updated Natural Resources entries for form {}".format(form.dataset_name))

            form.last_update_time = datetime.now()
            form.save()
        else:
            logger.error("Failed to updated answers for form {}".format(form.dataset_name))

    # Update BNS Prices
    queryset = BNSFormPrice.objects.filter(kobo_managed__eq=True).filter(last_submission_time__gt=F('last_update_time'))

    for form in queryset:

        dataset = get_kobo_data(form.auth_user, form.dataset_id)
        now = datetime.now()

        a = sync_price(dataset, form.related_uuid, now)

        if a["status"] == "success":

            form.last_update_time = datetime.now()
            form.save()

            logger.info("Successfully updated {} prices for form {}".format(len(dataset), form.dataset_name))

        else:
            logger.error("Failed to updated prices for form {}".format(form.dataset_name))
