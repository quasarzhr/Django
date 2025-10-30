# app/tests/test_admin_checks.py

from django import forms
from django.contrib import admin
from django.core import checks
from django.test import SimpleTestCase, override_settings
from django.contrib.auth.backends import ModelBackend

from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        app_label = "app"


class MyAdmin(admin.ModelAdmin):
    def check(self, **kwargs):
        return ["error!"]


class ModelBackendSubclass(ModelBackend):
    pass


@override_settings(
    SILENCED_SYSTEM_CHECKS=["fields.W342"],  # ForeignKey(unique=True)
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "app",
    ],
)
class SystemChecksTestCase(SimpleTestCase):
    databases = "__all__"

    def test_checks_are_performed(self):
        admin.site.register(Song, MyAdmin)
        try:
            errors = checks.run_checks()
            expected = ["error!"]
            self.assertEqual(errors, expected)
        finally:
            admin.site.unregister(Song)

    @override_settings(INSTALLED_APPS=["django.contrib.admin"])
    def test_apps_dependencies(self):
        errors = admin.checks.check_dependencies()
        expected = [
            checks.Error(
                "'django.contrib.contenttypes' must be in "
                "INSTALLED_APPS in order to use the admin application.",
                id="admin.E401",
            ),
            checks.Error(
                "'django.contrib.auth' must be in INSTALLED_APPS in order "
                "to use the admin application.",
                id="admin.E405",
            ),
            checks.Error(
                "'django.contrib.messages' must be in INSTALLED_APPS in order "
                "to use the admin application.",
                id="admin.E406",
            ),
        ]
        self.assertEqual(errors, expected)

    @override_settings(TEMPLATES=[])
    def test_no_template_engines(self):
        self.assertEqual(
            admin.checks.check_dependencies(),
            [
                checks.Error(
                    "A 'django.template.backends.django.DjangoTemplates' "
                    "instance must be configured in TEMPLATES in order to use "
                    "the admin application.",
                    id="admin.E403",
                )
            ],
        )

    @override_settings(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [],
                },
            }
        ],
    )
    def test_context_processor_dependencies(self):
        expected = [
            checks.Error(
                "'django.contrib.auth.context_processors.auth' must be "
                "enabled in DjangoTemplates (TEMPLATES) if using the default "
                "auth backend in order to use the admin application.",
                id="admin.E402",
            ),
            checks.Error(
                "'django.contrib.messages.context_processors.messages' must "
                "be enabled in DjangoTemplates (TEMPLATES) in order to use "
                "the admin application.",
                id="admin.E404",
            ),
            checks.Warning(
                "'django.template.context_processors.request' must be enabled "
                "in DjangoTemplates (TEMPLATES) in order to use the admin "
                "navigation sidebar.",
                id="admin.W411",
            ),
        ]
        self.assertEqual(admin.checks.check_dependencies(), expected)
        # The first error doesn't happen if
        # 'django.contrib.auth.backends.ModelBackend' isn't in
        # AUTHENTICATION_BACKENDS.
        with self.settings(AUTHENTICATION_BACKENDS=[]):
            self.assertEqual(admin.checks.check_dependencies(), expected[1:])
