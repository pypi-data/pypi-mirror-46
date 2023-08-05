# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_snippet_image']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.11,<3.0', 'snippet-image>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'django-snippet-image',
    'version': '0.1.2',
    'description': 'Django field for create snippet image for sharing in social networks.',
    'long_description': '===========================\ndjango-snippet-image\n===========================\n\nThe python package provides a django field for automatic\ngeneration of images for sharing in social networks.\n\ndjango-snippet-image based on snippet-image_ package.\n\n.. _snippet-image: https://github.com/acrius/snippet-image\n\nInstallation\n-------------------------\n\n`\npip3 install django-snippet-image\n`\n\nExample\n-------------------------\n\nUse SnippetImageField:\n\n.. code-block:: python\n\n    from django.db.models import (\n        Model,\n        CharField,\n        ImageField,\n    )\n    from django_snippet_image import SnippetImageField\n\n\n    class Statuses:\n        DRAFT = \'draft\'\n        PUBLISH = \'publish\'\n\n        CHOICES = (\n            (DRAFT, \'Draft\'),\n            (PUBLISH, \'Publish\'),\n        )\n\n\n    class ExampleModel(Model):\n        text = CharField(\n            max_length=200,\n            verbose_name=\'Text for snippet image\',\n        )\n        background = ImageField(\n            verbose_name=\'Background for snippet image\',\n            blank=True,\n            null=True,\n        )\n        snippet_image_field = SnippetImageField(\n            verbose_name=\'Example snippet image field\',\n            null=True,\n        )\n        status = CharField(\n            max_length=20,\n            choices=Statuses.CHOICES,\n        )\n\n        # Methods for collect data for snippet image.\n\n        def get_snippet_image_text(self, snippet_type):\n            return self.text if snippet_type == \'default\' and self.text else \'\'\n\n        def get_snippet_image_background(self, snippet_type):\n            if snippet_type == \'default\' and self.background:\n                return self.background.path\n\n        def snippet_image_should_be_created(self):\n            return self.status == Statuses.PUBLISH\n\n        class Meta:\n            verbose_name = \'example object\'\n            verbose_name_plural = \'example objects\'\n\nAnd use in template:\n\n.. code-block:: html\n\n    <meta property="og:image" content="{{ instance.snippet_image_field.url }}" />\n\nRead more on home page_.\n\n.. _page: https://github.com/acrius/django-snippet-image\n',
    'author': 'acrius',
    'author_email': 'acrius@mail.ru',
    'url': 'https://github.com/acrius/django-snippet-image',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
