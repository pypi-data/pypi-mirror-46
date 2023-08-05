from django.db import models
from rankings.fields import MarkdownField


class Poll(models.Model):
    date = models.DateField(unique=True)
    complete = models.BooleanField(default=False)

    note = MarkdownField(blank=True, null=True)

    def __str__(self):
        return "{:%Y-%m-%d}".format(self.date)
