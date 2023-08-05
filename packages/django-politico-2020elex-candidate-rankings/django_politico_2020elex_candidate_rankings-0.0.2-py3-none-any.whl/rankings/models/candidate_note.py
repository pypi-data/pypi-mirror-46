from django.db import models
from rankings.fields import MarkdownField


class CandidateNote(models.Model):
    poll = models.ForeignKey(
        "Poll",
        on_delete=models.CASCADE,
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

    @property
    def ranking(self):
        try:
            return self.poll.rankings.get(candidate=self.candidate).ranking
        except Exception:
            return "-"

    @property
    def has_note(self):
        return "Y" if self.note is not None and self.note != "" else "-"

    class Meta:
        unique_together = (("poll", "candidate"),)

    def __str__(self):
        return "{:%Y-%m-%d} {}".format(self.poll.date, self.candidate.name)
