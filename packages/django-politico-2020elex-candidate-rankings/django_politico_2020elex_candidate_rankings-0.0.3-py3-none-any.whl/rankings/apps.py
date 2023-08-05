from django.apps import AppConfig
from django.db.models.signals import post_migrate


class RankingsConfig(AppConfig):
    name = "rankings"

    def ready(self):
        from rankings import signals  # noqa

        post_migrate.connect(signals.create_admin_groups, sender=self)
        post_migrate.connect(signals.create_default_candidates, sender=self)
