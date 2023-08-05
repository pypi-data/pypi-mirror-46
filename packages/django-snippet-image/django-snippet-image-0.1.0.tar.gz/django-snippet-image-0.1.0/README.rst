===========================
django-snippet-image
===========================

The python package provides a django field for automatic
generation of images for sharing in social networks.

django-snippet-image based on snippet-image_ package.

.. _snippet-image: https://github.com/acrius/snippet-image

Installation
-------------------------

`
pip3 install django-snippet-image
`

User guide
-------------------------

Import package field:

.. code-block:: python

    from django_snippet_image import SnippetImageField


Use it in model:

.. code-block:: python

    class ExampleModel(Model):
        text = CharField(
            max_length=200,
            verbose_name='Text for snippet image',
        )
        background = ImageField(
            verbose_name='Background for snippet image',
            blank=True,
            null=True,
        )
        snippet_image_field = SnippetImageField(
            verbose_name='Example snippet image field',
            null=True,
        )

Set static params:

.. code-block:: python

    snippet_image_field = SnippetImageField(
            overlay='/user/python/app/assets/overlay.png',
            background_color=(0, 75, 125),
            font='/user/python/app/assets/OpenSans-Bold.ttf',
            verbose_name='Example snippet image field',
            null=True,
        )

Set dynamic params. They are set using model methods:

.. code-block:: python

    def get_snippet_image_text(self, snippet_type):
        return self.text if snippet_type == 'default' and self.text else ''

    def get_snippet_image_background(self, snippet_type):
        if snippet_type == 'default' and self.background:
            return self.background.path

Full example:

.. code-block:: python

    from django.db.models import (
        Model,
        CharField,
        ImageField,
    )
    from django_snippet_image import SnippetImageField


    class Statuses:
        DRAFT = 'draft'
        PUBLISH = 'publish'

        CHOICES = (
            (DRAFT, 'Draft'),
            (PUBLISH, 'Publish'),
        )


    class ExampleModel(Model):
        text = CharField(
            max_length=200,
            verbose_name='Text for snippet image',
        )
        background = ImageField(
            verbose_name='Background for snippet image',
            blank=True,
            null=True,
        )
        snippet_image_field = SnippetImageField(
            verbose_name='Example snippet image field',
            null=True,
        )
        status = CharField(
            max_length=20,
            choices=Statuses.CHOICES,
        )

        # Methods for collect data for snippet image.

        def get_snippet_image_text(self, snippet_type):
            return self.text if snippet_type == 'default' and self.text else ''

        def get_snippet_image_background(self, snippet_type):
            if snippet_type == 'default' and self.background:
                return self.background.path

        def snippet_image_should_be_created(self):
            return self.status == Statuses.PUBLISH

        class Meta:
            verbose_name = 'example object'
            verbose_name_plural = 'example objects'

And use in template:

.. code-block:: html
    <meta property="og:image" content="{{ instance.snippet_image_field.url }}" />

Read more on home page_.

.. _page: https://github.com/acrius/django-snippet-image
