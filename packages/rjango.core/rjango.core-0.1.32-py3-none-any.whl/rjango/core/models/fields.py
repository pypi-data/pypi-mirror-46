from django.db import models

import typing
import logging

logger = logging.getLogger(__name__)


class ImmutableCharField(models.CharField):
    description = "An immutable parent key."

    def __init__(self, *args, **kwargs):
        kwargs["editable"] = False
        kwargs["max_length"] = 256
        kwargs["null"] = False
        kwargs["blank"] = False

        super().__init__(*args, **kwargs)

    def validate(self, value, model):
        super().validate(value, model)


class ImmutableForeignKeyField(models.ForeignKey):
    description = "An immutable parent key."

    def __init__(self, *args, **kwargs):
        kwargs["editable"] = False
        kwargs["null"] = False
        kwargs["blank"] = False
        kwargs["on_delete"] = models.PROTECT

        super().__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)


class ImmutableOneToOneField(models.ForeignKey):
    description = "An immutable parent key."

    def __init__(self, *args, **kwargs):
        kwargs["null"] = False
        kwargs["blank"] = False
        kwargs["on_delete"] = models.PROTECT

        super().__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)


class ImmutableFieldTestCase:
    def __init__(self, *args):
        super().__init__(*args)
        self.factory = None
        self.qs = None

        self.kwargs_initial: typing.Dict[str] = {}
        self.kwargs_updated: typing.Dict[str] = {}

    def assert_field_immutability(
        self, key: str, value_initial: typing.Any, value_updated: typing.Any
    ):
        """
        Test if the model key (imei) can be changed,
        and saved to freshly created model (Device)
        using self.factory.
        """

        ###
        # Initial set up.
        # Here we define the value we are checking for immutability as well as
        # the initial and attempted updated values.
        # Get the set of key word arguments we are using

        self.kwargs_initial[key] = value_initial
        self.kwargs_updated[key] = value_updated
        #
        obj = self.factory(**self.kwargs_initial)
        db_obj = self.qs.get(**self.kwargs_initial)
        ##
        #
        self.assertEqual(db_obj.uuid, obj.uuid)
        self.assertEqual(getattr(db_obj, key), self.kwargs_initial[key])
        #
        ###

        # Try to update our local obj model,
        # we set key attribute
        # then refresh our local db_obj model.
        setattr(obj, key, value_updated)
        obj.save()
        db_obj.refresh_from_db()
        #
        ###

        # Here we check that the original value for key is still set.
        self.assertEqual(getattr(db_obj, key), self.kwargs_initial[key])
