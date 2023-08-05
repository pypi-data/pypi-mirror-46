from django.db import models
from rankings.fields import MarkdownField


class CandidateNote(models.Model):
    poll = models.ForeignKey(
        "Poll",
        on_delete=models.PROTECT,
        related_name="candidate_notes",
        related_query_name="candidate_note",
    )
    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.PROTECT,
        related_name="candidate_notes",
        related_query_name="candidate_note",
    )
    note = MarkdownField(blank=True, null=True)

    class Meta:
        unique_together = (("poll", "candidate"),)

    def __str__(self):
        return "{:%Y-%m-%d} {}".format(self.poll.date, self.candidate.name)
