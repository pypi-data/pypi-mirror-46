from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=250)
    politico_uid = models.SlugField(max_length=500, unique=True)
    fec_candidate_id = models.SlugField(
        max_length=50, unique=True, blank=True, null=True
    )

    def __str__(self):
        return self.name
