from django.db import models
from django.db.models import CharField, TextField, NullBooleanField, DateTimeField

CHOICES_IS_GLOBSTAR = ((None, ''), (True, 'Yes'), (False, 'No'))


class TimestampedModel(models.Model):
    """ Abstract base class with self-updating ``created`` and ``modified`` fields. """
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthoredModel(TimestampedModel):
    """ Abstract base class with ``author`` field. """
    author = CharField(max_length=100)

    class Meta:
        abstract = True


class TriggerResponse(AuthoredModel):
    trigger = CharField(max_length=200)
    response = TextField()
    source_state = CharField(max_length=200)
    dest_state = CharField(max_length=200)
    is_globstar = NullBooleanField(choices=CHOICES_IS_GLOBSTAR, max_length=3, null=True, blank=True, default=None)
