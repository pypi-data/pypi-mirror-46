from django.db.models import ImageField
from uuid import uuid4
from snippet_image import create_snippet_image

from .attributes import Attributes


class BaseSnippetImageFieldMixin:
    method_prefix = 'get_snippet_image'
    snippet_type = 'default'
    kwargs = {}
    should_be_created_method = 'snippet_image_should_be_created'

    def should_be_created(self, instance):
        method = getattr(instance, self.should_be_created_method, None)
        return method() if method else True

    @staticmethod
    def get_file_name():
        return '{}.jpeg'.format(str(uuid4()))

    def collect_data(self, instance):
        data = {
            attribute.name: self.get_attribute_value(instance, attribute) for attribute in Attributes
        }

        return data

    def get_attribute_value(self, instance, attribute):
        attribute_name = attribute.name
        value = self.get_attribute_from_kwargs(attribute_name)

        if not value:
            value = self.get_attribute_from_instance(instance, attribute_name)

        if not value:
            value = attribute.value.default

        self.validate_attribute(attribute, value)

        return value

    @staticmethod
    def validate_attribute(attribute, value):
        try:
            attribute.value.validate(value)
        except ValueError as error:
            raise ValueError('Validation error for attribute {}: {}'.format(attribute.name, str(error)))

    def get_attribute_from_kwargs(self, attribute_name):
        return self.kwargs.get(attribute_name)

    def get_attribute_from_instance(self, instance, attribute_name):
        method_name = '{}_{}'.format(self.method_prefix, attribute_name)
        method = getattr(instance, method_name, None)
        if method:
            value = method(self.snippet_type)
        else:
            value = None

        return value

    @staticmethod
    def create_snippet_image(data):
        return create_snippet_image(**data)

    def get_specific_deconstruct_kwargs(self):
        kwargs = {
            attribute.name: self.kwargs.get(attribute.name)
            for attribute in Attributes
            if not self.kwargs.get(attribute.name) is None
        }
        kwargs['snippet_type'] = self.snippet_type

        return kwargs


class SnippetImageField(BaseSnippetImageFieldMixin, ImageField):
    def __init__(
            self,
            snippet_type='default',
            **kwargs
    ):
        """

        :param snippet_type (str): To collect different data for different fields.
                                   For example value: 'facebook', 'twitter' and etc.
        :param kwargs: snippet_image.create_snippet_image and ImageField params.
            If create_snippet_image parameter was not set in the constructor,
            it will be taken from the method get_snippet_image_{param} of instance or default settings.
            create_snippet_image:
                :param font: Path to font file. Is required. For load font used PIL.ImageFont.
                :type font: str
                :param size: Size of snippet image. tuple(width, height).
                :type size: tuple(int, int)
                :param text: Text of snippet image. By default is an empty string.
                :type text: str
                :param background: Path to background image file.
                :type background: str
                :param background_color: Background color of snippet image. Used when background is None.
                :type background_color: tuple(int, int, int)
                :param overlay: Path to overlay image. if size is None, overlay size is used.
                                As an overlay, an image with a transparent background is used.
                :type overlay: str
                :param brightness: Brightness of background of snippet image. Value from 0 to 1.
                :type brightness: float
                :param font_color: Font color in RGBA. By default is (255, 255, 255, 255).
                :type font_color: tuple(int, int, int, int)
                :param font_size: Size of snippet image text. By default is 64.
                :type font_size: int
                :param padding: Text indents to the left and right of the snippet image.
                                Value from 0 to 1.
                                0 - 0% width;
                                1 - 100% width.
                :type padding: float
                :param center : Background image center for crop and resize image. tuple(x, y).
                                Defaults is center of background image.
                :type center: tuple(int, int)

            ImageField params:
                 :param verbose_name:
                 :param name:
                 :param width_field:
                 :param height_field:
                 :param upload_to:
                 :param storage:
        """
        self.snippet_type = snippet_type
        self.kwargs = kwargs
        kwargs['blank'] = True
        super().__init__(**kwargs)

    def pre_save(self, instance, add):
        file = getattr(instance, self.attname)

        if (not file or not file.file) and self.should_be_created(instance):
            file_name = self.get_file_name()
            data = self.collect_data(instance)
            image = self.create_snippet_image(data)
            file.save(file_name, image, save=False)
        elif not file._committed:
            file.save(file.name, file.file, save=False)

        return file

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        specific_attributes_values = self.get_specific_deconstruct_kwargs()
        kwargs.update(specific_attributes_values)

        return name, path, args, kwargs
