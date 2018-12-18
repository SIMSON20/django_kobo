from .models import BNSForm
from .admin import sync_answers, sync_answersnr, sync_answershhmembers, sync_answersgps, sync_answersgs
from kobo.utils import get_kobo_data, normalize_data
from django.db.models import F
from datetime import datetime


def check_for_updates():
    queryset = BNSForm.objects.filter(last_submission_time__gt=F('last_update_time'))
    for form in queryset:
        # TODO: make sure to remove archived forms from queryset

        dataset = get_kobo_data(form.auth_user, form.dataset_id)
        dataset = normalize_data(dataset)

        now = datetime.now()

        a = sync_answers(dataset, form.dataset_uuid, now)
        if a["status"] == "success":

            b = sync_answersgps(dataset, form.dataset_uuid, now)
            c = sync_answersgs(dataset, form.dataset_uuid, now)
            d = sync_answershhmembers(dataset, form.dataset_uuid, now)
            e = sync_answersnr(dataset, form.dataset_uuid, now)

            form.last_update_time = datetime.now()
            form.save()

