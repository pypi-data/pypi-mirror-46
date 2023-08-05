from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MAX_RANK = 10


def validate_rank(value):
    if value > MAX_RANK or value < 1:
        raise ValidationError(
            _("%(value) is not between 1 and 10"), params={"value": value}
        )


class Ballot(models.Model):
    poll = models.ForeignKey(
        "Poll",
        on_delete=models.CASCADE,
        related_name="ballots",
        related_query_name="ballot",
    )
    voter = models.ForeignKey(
        "Voter",
        on_delete=models.PROTECT,
        related_name="ballots",
        related_query_name="ballot",
    )
    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.PROTECT,
        related_name="ballots",
        related_query_name="ballot",
    )
    ranking = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[validate_rank]
    )
    note = models.TextField(blank=True, null=True)

    @property
    def points(self):
        valueScaled = float(self.ranking - 1) / float(MAX_RANK - 1)
        return MAX_RANK + (valueScaled * (1 - MAX_RANK))

    class Meta:
        unique_together = (
            ("poll", "voter", "ranking"),
            ("poll", "voter", "candidate"),
        )

    def __str__(self):
        return "{:%Y-%m-%d} {} {}".format(
            self.poll.date, self.voter.user.username, self.candidate.name
        )


class UserBallot(Ballot):
    class Meta:
        proxy = True
        verbose_name_plural = "My ballots"
        ordering = ("ranking", "candidate__name")


class AdminBallot(Ballot):
    class Meta:
        proxy = True
        verbose_name_plural = "Open ballots"
        ordering = ("poll", "voter", "ranking")
