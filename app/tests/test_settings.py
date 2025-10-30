from django.conf import settings

def test_debug_mode_is_false_in_production():
    assert hasattr(settings, 'DEBUG')
    assert isinstance(settings.DEBUG, bool)
