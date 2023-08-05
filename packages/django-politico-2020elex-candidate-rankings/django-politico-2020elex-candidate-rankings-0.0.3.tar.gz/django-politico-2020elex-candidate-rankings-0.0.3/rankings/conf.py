"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""
import os
from django.conf import settings as project_settings


class Settings:
    pass


Settings.ADMIN_GROUP = getattr(
    project_settings,
    "RANKINGS_ADMIN_GROUP",
    "Candidate Rankings Administrator",
)

Settings.VOTER_GROUP = getattr(
    project_settings, "RANKINGS_VOTER_GROUP", "Candidate Rankings Voter"
)

Settings.CROSSWALK_API = getattr(
    project_settings,
    "RANKINGS_CROSSWALK_API",
    "https://politicoapps.com/crosswalk/api/",
)

Settings.CROSSWALK_TOKEN = getattr(
    project_settings,
    "RANKINGS_CROSSWALK_TOKEN",
    os.getenv("CROSSWALK_TOKEN", None),
)

Settings.BAKERY_API = getattr(project_settings, "RANKINGS_BAKERY_API", None)

Settings.BAKERY_TOKEN = getattr(
    project_settings,
    "RANKINGS_BAKERY_TOKEN",
    os.getenv("RANKINGS_BAKERY_TOKEN", None),
)


settings = Settings
