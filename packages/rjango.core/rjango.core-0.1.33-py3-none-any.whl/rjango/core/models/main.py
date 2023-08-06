from typing import *

import uuid as uuid_lib

from enum import Enum, unique, auto

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

import logging

logger = logging.getLogger(__name__)


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides created and modified fields.

    We also automatically order by created time/

    Attributes:
        :type created:
        :type modified:
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created"]


class UUIDModel(models.Model):
    """
    An abstract base class model that provides uuid field.

    Attributes:
        :type uuid: str
    """

    uuid = models.UUIDField(
        primary_key=True, db_index=True, default=uuid_lib.uuid4, editable=False
    )

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    """
    An owned model has a current owner and previous owners.
    """

    class Meta:
        abstract = True

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Model(UUIDModel, TimeStampedModel):
    """
    Base model that uses a UUID as it's primary key
    and also has created and modified fields.

        Attributes:
        :type uuid: str
        :type created:
        :type modified:
    """

    class Meta:
        abstract = True


@unique
class LocalEnums(AutoName):
    EN = auto()


class BaseUser(AbstractUser, UUIDModel, TimeStampedModel):
    """
    Base user with sane defaults.

    Attributes:
    :type email: str
    :type verified_email: bool

    :type phone_number:
    :type verified_phone_number: bool
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email: str = models.EmailField(unique=True)
    verified_email: bool = models.BooleanField(default=False)

    phone_number = PhoneNumberField()
    verified_phone_number = models.BooleanField(default=False)

    username: AnyStr = models.TextField(blank=True, null=True)

    local: AnyStr = models.CharField(
        max_length=10,
        db_index=True,
        null=False,
        blank=False,
        choices=[(tag.value, tag.name) for tag in LocalEnums],
        default=LocalEnums.EN.value,
    )
    photo_url: AnyStr = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        abstract = True


class ImmutableModel(Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        creating = self._state.adding is True
        model = self._meta.model

        if creating:
            logger.info("Creating immutable model")
            super().save(*args, **kwargs)
        else:
            logger.info("Trying to update immutable model.")
