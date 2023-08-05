from rest_framework import serializers
from rankings.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ("name", "politico_uid", "fec_candidate_id")
