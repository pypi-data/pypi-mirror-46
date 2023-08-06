import typing
import json
import logging

from django.core import serializers, exceptions
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.apps import apps
from .main import Model

logger = logging.getLogger(__name__)


def get_history_model(
    app_name: typing.AnyStr,
    model_name: typing.AnyStr,
    history_suffix: typing.AnyStr = "History",
):
    model_name = model_name + history_suffix
    return apps.get_model(app_name, model_name)


class HistoryModel(Model):
    """
    """

    class Meta:
        abstract = True

    class OPTIONS:
        mutatable_fields: typing.List[str] = []

    def get_history_model(self, **kwargs):
        model = self._meta.label.split(".")
        self.app_name = model[0]

        # print("set_history_model", self.history_model_name)

        self.history_model_name = model[1]
        return get_history_model(
            app_name=self.app_name, model_name=self.history_model_name
        )

    def create_history_point(self):
        history_model = self.get_history_model()

        serialized_qs = serializers.serialize("json", [self])
        serialized_obj = json.loads(serialized_qs)[0]["fields"]

        history_model.objects.create(parent=self, state=serialized_obj)

    def save(self, *args, **kwargs):

        creating = self._state.adding is True

        try:
            self.full_clean()
        except exceptions.ValidationError as e:
            # Do something based on the errors contained in e.message_dict.
            # Display them to a user, or handle them programmatically.
            print("E!", e)
            raise e

        super().save(*args, **kwargs)
        self.create_history_point()


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


class HistoryModelTestCase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.history_model = None
        self.history_model_name: str = "History"

    def set_history_model(self):
        model_label = self.model._meta.label.split(".")
        self.app_name = model_label[0]

        self.history_model_name = model_label[1]
        self.history_model = get_history_model(
            app_name=self.app_name,
            model_name=self.history_model_name,
            history_suffix="History",
        )
        return self.history_model

    def setUp(self):
        self.set_history_model()

    def test_history(
        self, key: typing.AnyStr, value_initial: typing.Any, value_updated: typing.Any
    ):
        db_obj = self.factory(**{key: value_initial})
        uuid = db_obj.uuid
        db_obj = self.model.objects.get(**{key: value_initial})

        db_h_model = self.set_history_model()

        model_history = db_h_model.objects.filter(parent__uuid=uuid)
        count = model_history.count()

        self.assertTrue(model_history.exists())
        self.assertGreaterEqual(1, count)

        db_obj.email = value_updated
        db_obj.save()
        db_obj.refresh_from_db()
        self.assertEqual(value_updated, db_obj.email)

        count = model_history.all().count()
        self.assertGreaterEqual(2, count)
