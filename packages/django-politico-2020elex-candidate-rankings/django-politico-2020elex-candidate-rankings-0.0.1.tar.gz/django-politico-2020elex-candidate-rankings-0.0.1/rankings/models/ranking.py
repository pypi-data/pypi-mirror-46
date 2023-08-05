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

    class Meta:
        unique_together = (("poll", "ranking"), ("poll", "candidate"))
        ordering = ("-poll", "ranking")

    def __str__(self):
        return "{:%Y-%m-%d} -- {}. {}".format(
            self.poll.date, self.ranking, self.candidate.name
        )
