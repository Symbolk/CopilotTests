
def is_sites_framework_enabled() -> bool:
    """
    Check project's settings to see if the optional Sites framework is installed.
    """
    from django.conf import settings
    return "django.contrib.sites" in settings.INSTALLED_APPS



def test_is_sites_framework_enabled():
    """Check the correctness of is_sites_framework_enabled
    """
    import os
    os.environ["DJANGO_SETTINGS_MODULE"] = "plib_runnable.settings"
    assert is_sites_framework_enabled() is True
    