from django.db import models


class Ranking(models.Model):
    poll = models.ForeignKey(
        "Poll",
        on_delete=models.CASCADE,
        related_name="rankings",
        related_query_name="ranking",
    )
    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.PROTECT,
        related_name="rankings",
        related_query_name="ranking",
    )
    ranking = models.PositiveSmallIntegerField()
    points = models.PositiveSmallIntegerField()

    @property
    def votes(self):
        return self.poll.ballots.filter(
            candidate=self.candidate, ranking__isnull=False
        ).count()

    class Meta:
        unique_together = (("poll", "candidate"),)
        ordering = ("-poll", "ranking")

    def __str__(self):
        return "{:%Y-%m-%d} -- {}. {}".format(
            self.poll.date, self.ranking, self.candidate.name
        )


class OpenRanking(Ranking):
    class Meta:
        proxy = True
        verbose_name_plural = "Open rankings"
