from django.contrib import admin
from rankings.models import (
    Poll,
    Candidate,
    CandidateNote,
    Voter,
    Ballot,
    Ranking,
)
from rankings.conf import settings
from django.forms import Textarea
from django.db import models


class NoAddNoDeleteModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseAdminModelAdmin(NoAddNoDeleteModelAdmin):
    @staticmethod
    def is_admin(request):
        return request.user.groups.filter(name=settings.ADMIN_GROUP).exists()

    def has_module_permission(self, request, obj=None):
        return self.is_admin(request)

    def has_change_permission(self, request, obj=None):
        return self.is_admin(request)


class BaseVoterModelAdmin(NoAddNoDeleteModelAdmin):
    @staticmethod
    def is_voter(request):
        return request.user.groups.filter(name=settings.VOTER_GROUP).exists()

    def has_module_permission(self, request, obj=None):
        return self.is_voter(request)

    def has_change_permission(self, request, obj=None):
        return self.is_voter(request)


class UserBallot(Ballot):
    class Meta:
        proxy = True
        verbose_name_plural = "My ballots"
        ordering = ("ranking", "candidate__name")


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


class AdminBallot(Ballot):
    class Meta:
        proxy = True
        verbose_name_plural = "Admin ballots"
        ordering = ("poll", "voter", "ranking")


class AdminBallotAdmin(BaseAdminModelAdmin):
    list_display = ("poll", "voter", "candidate", "ranking")
    list_filter = ("poll__date",)
    search_fields = ("voter__user__username", "candidate__name")
    actions = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(ranking__isnull=True)


class DevBallotAdmin(admin.ModelAdmin):
    list_filter = ("poll__date",)
    list_display = ("poll", "voter", "candidate", "ranking")
    search_fields = ("voter__user__username", "candidate__name")


class CandidateNoteAdmin(admin.ModelAdmin):
    actions = None
    list_filter = ("poll__date",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(poll__complete=False)


class PollAdmin(admin.ModelAdmin):
    list_display = ("date", "complete")


class RankingAdmin(admin.ModelAdmin):
    list_filter = ("poll__date",)
    list_display = ("poll", "candidate", "ranking")
    search_fields = ("candidate__name",)


admin.site.register(Poll, PollAdmin)
admin.site.register(Candidate)
admin.site.register(CandidateNote, CandidateNoteAdmin)
admin.site.register(Voter)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(Ballot, DevBallotAdmin)
admin.site.register(AdminBallot, AdminBallotAdmin)
admin.site.register(UserBallot, UserBallotAdmin)
