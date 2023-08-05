from django.db import models
from django.contrib.auth.models import User


class Voter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, limit_choices_to={"is_staff": True}
    )

    @property
    def ballots_cast(self):
        return self.ballots.filter(ranking__isnull=False).count()

    def __str__(self):
        return self.user.username
