import logging

from django.db import models

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
