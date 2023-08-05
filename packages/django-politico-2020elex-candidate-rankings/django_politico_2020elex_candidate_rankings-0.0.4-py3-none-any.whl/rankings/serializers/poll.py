from rest_framework import serializers
from rankings.models import Poll, Candidate, Ranking, CandidateNote
from .candidate import CandidateSerializer


class PollListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ("url", "date", "complete")


class PollSerializer(serializers.ModelSerializer):
    rankings = serializers.SerializerMethodField()
    series = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ("series", "date", "note", "complete", "rankings")

    def get_series(self, obj):
        return [p.date for p in Poll.objects.all().order_by("date")]

    def get_history(self, poll, candidate):
        polls = Poll.objects.filter(date__lt=poll.date).order_by("date")
        rankings = []

        for p in polls:
            try:
                r = Ranking.objects.get(candidate=candidate, poll__date=p.date)
                rankings.append(r.ranking)
            except Ranking.DoesNotExist:
                rankings.append(None)

        return rankings

    def get_rankings(self, obj):
        if not obj.complete:
            return []
        candidates = {
            c.id: {"model": c, "points": 0, "distribution": []}
            for c in Candidate.objects.all()
        }
        for ballot in obj.ballots.exclude(ranking__isnull=True):
            candidates[ballot.candidate.id]["points"] += ballot.points
            candidates[ballot.candidate.id]["distribution"].append(
                ballot.ranking
            )

        points = [candidates[id]["points"] for id in candidates]
        points.sort(reverse=True)

        rankings = []
        for id, candidate in candidates.items():
            if not candidate["points"]:
                continue
            rankings.append(
                {
                    "rank": points.index(candidate["points"]) + 1,
                    "history": self.get_history(obj, candidate["model"]),
                    "points": candidate["points"],
                    "distribution": candidate["distribution"],
                    "candidate": CandidateSerializer(candidate["model"]).data,
                    "note": CandidateNote.objects.get(
                        candidate=candidate["model"], poll=obj
                    ).note,
                }
            )
        return rankings
