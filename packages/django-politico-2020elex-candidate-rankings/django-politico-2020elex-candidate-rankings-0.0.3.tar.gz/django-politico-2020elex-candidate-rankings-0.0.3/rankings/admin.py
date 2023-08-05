from django.contrib import admin
from rankings.models import (
    Poll,
    Candidate,
    CandidateNote,
    Voter,
    Ballot,
    Ranking,
    UserBallot,
    AdminBallot,
    OpenRanking,
)
from rankings.conf import settings
from django.forms import Textarea
from django.db import models


class ChangeOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyMixin(ChangeOnlyMixin):
    def has_change_permission(self, request, obj=None):
        return False


class BaseAdminModelAdmin(ChangeOnlyMixin, admin.ModelAdmin):
    @staticmethod
    def is_admin(request):
        return request.user.groups.filter(name=settings.ADMIN_GROUP).exists()

    def has_module_permission(self, request, obj=None):
        return self.is_admin(request)

    def has_change_permission(self, request, obj=None):
        return self.is_admin(request)


class BaseVoterModelAdmin(ChangeOnlyMixin, admin.ModelAdmin):
    @staticmethod
    def is_voter(request):
        return request.user.groups.filter(name=settings.VOTER_GROUP).exists()

    def has_module_permission(self, request, obj=None):
        return self.is_voter(request)

    def has_change_permission(self, request, obj=None):
        return self.is_voter(request)


def reset_rankings(modeladmin, request, queryset):
    queryset.update(ranking=None)


reset_rankings.short_description = "Reset rankings"


class UserBallotAdmin(BaseVoterModelAdmin):
    actions = [reset_rankings]
    list_display = ("candidate", "ranking", "note")
    list_editable = ("ranking", "note")
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 100})}
    }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(voter__user=request.user, poll__complete=False)


class AdminBallotAdmin(BaseAdminModelAdmin):
    list_display = ("poll", "voter", "candidate", "ranking")
    list_filter = ("poll__date",)
    search_fields = ("voter__user__username", "candidate__name")
    actions = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(ranking__isnull=True, poll__complete=False)


class DevBallotAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_filter = ("poll__date",)
    list_display = ("poll", "voter", "candidate", "ranking")
    search_fields = ("voter__user__username", "candidate__name")


class CandidateNoteAdmin(BaseAdminModelAdmin):
    actions = None
    list_display = ("poll", "candidate", "ranking", "has_note")
    list_filter = ("poll__date",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(poll__complete=False)


class PollAdmin(admin.ModelAdmin):
    list_display = ("date", "votes", "complete")


class RankingAdmin(ChangeOnlyMixin, admin.ModelAdmin):
    list_filter = ("poll__date",)
    list_display = ("poll", "candidate", "ranking")
    search_fields = ("candidate__name",)


class OpenRankingAdmin(BaseAdminModelAdmin):
    actions = None
    list_display = ("poll", "candidate", "ranking", "points", "votes")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(poll__complete=False)


class VoterAdmin(admin.ModelAdmin):
    list_display = ("user", "ballots_cast")


admin.site.register(Poll, PollAdmin)
admin.site.register(Candidate)
admin.site.register(CandidateNote, CandidateNoteAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(OpenRanking, OpenRankingAdmin)
admin.site.register(Ballot, DevBallotAdmin)
admin.site.register(AdminBallot, AdminBallotAdmin)
admin.site.register(UserBallot, UserBallotAdmin)
