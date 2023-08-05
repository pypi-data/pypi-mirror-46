from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rankings.models import Poll
from rankings.serializers import PollSerializer, PollListSerializer


class PollViewSet(ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Poll.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PollListSerializer
        else:
            return PollSerializer
