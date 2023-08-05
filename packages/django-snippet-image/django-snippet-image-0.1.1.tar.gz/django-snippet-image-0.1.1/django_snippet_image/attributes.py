from enum import Enum

from .conf import settings
from .validators import (
    is_required,
    is_2d,
    is_rgb_color,
    is_rgba_color,
)


class Attribute:
    def __init__(
            self,
            default_setting=None,
            default_value=None,
            validators=None,
    ):
        self.default_setting = default_setting
        self.default_value = default_value
        self.validators = validators or []

    def validate(self, value=None):
        value = value or self.default
        for validator in self.validators:
            validator(value)

    @property
    def default(self):
        return self.default_setting and getattr(settings, self.default_setting) \
            if self.default_value is None else self.default_value


class Attributes(Enum):
    font = Attribute(
        default_setting='SNIPPET_IMAGE_DEFAULT_FONT',
        validators=[is_required, ],
    )
    size = Attribute(
        default_setting='SNIPPET_IMAGE_DEFAULT_SIZE',
        validators=[is_2d, ]
    )
    text = Attribute(default_value='')
    background = Attribute(default_setting='SNIPPET_IMAGE_DEFAULT_BACKGROUND')
    background_color = Attribute(
        default_setting='SNIPPET_IMAGE_DEFAULT_BACKGROUND_COLOR',
        validators=[is_rgb_color, ],
    )
    overlay = Attribute(default_setting='SNIPPET_IMAGE_DEFAULT_OVERLAY')
    brightness = Attribute(default_setting='SNIPPET_IMAGE_DEFAULT_BRIGHTNESS')
    font_color = Attribute(
        default_setting='SNIPPET_IMAGE_DEFAULT_FONT_COLOR',
        validators=[is_rgba_color, ]
    )
    font_size = Attribute(default_setting='SNIPPET_IMAGE_DEFAULT_FONT_SIZE')
    padding = Attribute(default_setting='SNIPPET_IMAGE_DEFAULT_PADDING')
    center = Attribute(validators=[is_2d, ])
