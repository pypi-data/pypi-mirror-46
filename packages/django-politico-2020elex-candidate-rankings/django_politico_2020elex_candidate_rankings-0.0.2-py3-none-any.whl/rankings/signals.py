from django.db.models.signals import post_save
from django.dispatch import receiver
from rankings.models import (
    Poll,
    Voter,
    Ballot,
    Candidate,
    Ranking,
    CandidateNote,
    UserBallot,
    AdminBallot,
)
from crosswalk_client import Client
from django.contrib.auth.models import Group
from .celery import bake_poll as bake


@receiver(post_save, sender=Poll)
def create_ballots(sender, instance, created, **kwargs):
    for voter in Voter.objects.all():
        for candidate in Candidate.objects.all():
            Ballot.objects.get_or_create(
                poll=instance, voter=voter, candidate=candidate
            )


@receiver(post_save, sender=Poll)
def create_candidate_notes(sender, instance, created, **kwargs):
    for candidate in Candidate.objects.all():
        CandidateNote.objects.get_or_create(poll=instance, candidate=candidate)


@receiver(post_save, sender=Poll)
def bake_poll(sender, instance, created, **kwargs):
    if instance.complete:
        bake.delay(pk=instance.pk)


@receiver(post_save, sender=AdminBallot)
@receiver(post_save, sender=Ballot)
@receiver(post_save, sender=UserBallot)
def create_rankings(sender, instance, created, **kwargs):
    candidates = {
        c.id: {"model": c, "points": 0, "distribution": []}
        for c in Candidate.objects.all()
    }
    for ballot in instance.poll.ballots.exclude(ranking__isnull=True):
        candidates[ballot.candidate.id]["points"] += ballot.points
        candidates[ballot.candidate.id]["distribution"].append(ballot.ranking)

    points = [candidates[id]["points"] for id in candidates]
    points.sort(reverse=True)

    for id, candidate in candidates.items():
        if not candidate["points"]:
            Ranking.objects.filter(
                poll=instance.poll, candidate=candidate["model"]
            ).delete()
        else:
            Ranking.objects.update_or_create(
                poll=instance.poll,
                candidate=candidate["model"],
                defaults={
                    "ranking": points.index(candidate["points"]) + 1,
                    "points": candidate["points"],
                },
            )


@receiver(post_save, sender=Voter)
def add_voter_to_group(sender, instance, created, **kwargs):
    from rankings.conf import settings

    if created:
        group = Group.objects.get(name=settings.VOTER_GROUP)
        group.user_set.add(instance.user)


def create_admin_groups(sender, **kwargs):

    from rankings.conf import settings

    Group.objects.get_or_create(name=settings.ADMIN_GROUP)
    Group.objects.get_or_create(name=settings.VOTER_GROUP)


def create_default_candidates(sender, **kwargs):
    from rankings.conf import settings

    if settings.CROSSWALK_TOKEN:
        try:
            crosswalk = Client(
                settings.CROSSWALK_TOKEN, settings.CROSSWALK_API
            )
        except Exception:
            return
        domain = crosswalk.get_domain("2020-presidential-candidates")
        candidates = domain.get_entities({"party": "dem"})

        for candidate in candidates:
            if candidate.nickname:
                name = "{} {}".format(candidate.nickname, candidate.last_name)
            else:
                name = "{} {}".format(
                    candidate.first_name, candidate.last_name
                )
            Candidate.objects.update_or_create(
                politico_uid=candidate.politico_uid,
                defaults={
                    "fec_candidate_id": candidate.fec_candidate_id or None,
                    "name": name,
                },
            )
