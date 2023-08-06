"""
DEFAULT SETTINGS for create sharing snippets images.

Allowed settings:
SNIPPET_IMAGE_DEFAULT_SIZE,
SNIPPET_IMAGE_DEFAULT_BACKGROUND,
SNIPPET_IMAGE_DEFAULT_BACKGROUND_COLOR: as default is (0, 0, 0),
SNIPPET_IMAGE_DEFAULT_OVERLAY,
SNIPPET_IMAGE_DEFAULT_BRIGHTNESS: as default is 0.5,
SNIPPET_IMAGE_DEFAULT_FONT,
SNIPPET_IMAGE_DEFAULT_FONT_SIZE: as default is 64,
SNIPPET_IMAGE_DEFAULT_FONT_COLOR: as default is (255, 255, 255, 255),
SNIPPET_IMAGE_DEFAULT_PADDING: as defaults is 0.1,
"""
from django.conf import settings as django_settings


class LazySettings:
    def __init__(
            self,
            **defaults
    ):
        self.defaults = defaults

    def __getattr__(self, name):
        value = getattr(django_settings, name, self.defaults.get(name))

        return value


settings = LazySettings(
    SNIPPET_IMAGE_DEFAULT_BACKGROUND_COLOR=(0, 0, 0),
    SNIPPET_IMAGE_DEFAULT_BRIGHTNESS=0.5,
    SNIPPET_IMAGE_DEFAULT_FONT_SIZE=64,
    SNIPPET_IMAGE_DEFAULT_FONT_COLOR=(255, 255, 255, 255),
    SNIPPET_IMAGE_DEFAULT_PADDING=0.1,
)
