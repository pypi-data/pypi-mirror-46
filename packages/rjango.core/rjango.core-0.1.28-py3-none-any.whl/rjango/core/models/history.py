import typing
import json
import logging

from django.core import serializers, exceptions
from django.db import models
from django.contrib.postgres.fields import JSONField

from .main import Model

logger = logging.getLogger(__name__)


class HistoryModel(Model):
    """
    """

    class Meta:
        abstract = True

    class OPTIONS:
        mutatable_fields: typing.List[str] = []

    def save(self, *args, **kwargs):
        creating = self._state.adding is True
        model = self._meta.model

        try:
            self.full_clean()
        except exceptions.ValidationError as e:
            # Do something based on the errors contained in e.message_dict.
            # Display them to a user, or handle them programmatically.
            print("E!", e)
            raise e

        json_str = serializers.serialize("json", [self])
        json_str = json.loads(json_str)
        if creating:
            super().save(*args, **kwargs)
        else:
            print("Trying to update immutable model.")

            current_db_obj = model.objects.get(uuid=self.uuid)
            # Make sure non mutable fieids match current_db_obj

            # this should be for model fields not in mutatable fields
            for field in self.OPTIONS.mutatable_fields:
                # TODO write checks here
                pass
        # TODO write actual save method here


class HistoryStateModel(Model):
    """

    """

    class Meta:
        abstract = True
        get_latest_by = "created"

    @staticmethod
    def db_table_name(class_name):
        return ("immutable_history_" + class_name).lower().replace(".", "_")

    parent = models.ForeignKey("core.HistoryModel", on_delete=models.PROTECT)

    state = JSONField()
