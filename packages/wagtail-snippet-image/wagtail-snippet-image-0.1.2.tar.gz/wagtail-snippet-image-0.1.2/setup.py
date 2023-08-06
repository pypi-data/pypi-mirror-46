# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wagtail_snippet_image']

package_data = \
{'': ['*']}

install_requires = \
['django-snippet-image>=0.1.2,<0.2.0', 'wagtail>=2.5,<3.0']

setup_kwargs = {
    'name': 'wagtail-snippet-image',
    'version': '0.1.2',
    'description': 'Creating a snippet images on Wagtail for sharing for social media.',
    'long_description': '==============================\nwagtail-snippet-image\n==============================\n\nPackage for creating a snippet images for sharing in social networks and etc.\nBased on django-snippet-image_ and snippet-image_.\nBut for storage of images used Wagtail Images_.\n\n.. _django-snippet-image: https://github.com/acrius/django-snippet-image\n.. _snippet-image: https://github.com/acrius/snippet-image\n.. _Images: https://docs.wagtail.io/en/stable/advanced_topics/images/index.html\n\nInstallation\n--------------------------\n\n`pip3 install wagtail-snippet-image`\n\nHow use it\n--------------------------\n\n.. code-block:: python\n\n    from django.db.models import (\n        CharField,\n        ForeignKey,\n        SET_NULL,\n        CASCADE,\n    )\n    from wagtail_snippet_image import SnippetImageField\n    from wagtail.core.models import Page\n    from wagtail.admin.edit_handlers import FieldPanel\n    from wagtail.images.edit_handlers import ImageChooserPanel\n    from modelcluster.fields import ParentalKey\n    from modelcluster.contrib.taggit import ClusterTaggableManager\n    from taggit.models import TaggedItemBase\n\n\n    class PageTag(TaggedItemBase):\n        content_object = ParentalKey(\n            \'home.HomePage\',\n            on_delete=CASCADE,\n            related_name=\'tagged_items\',\n        )\n\n\n    class Statuses:\n        DRAFT = \'draft\'\n        PUBLISH = \'publish\'\n\n        CHOICES = (\n            (DRAFT, \'Draft\'),\n            (PUBLISH, \'Publish\'),\n        )\n\n\n    class HomePage(Page):\n        background = ForeignKey(\n            \'wagtailimages.Image\',\n            verbose_name=\'Изображение для обложки\',\n            related_name=\'cover_images\',\n            on_delete=SET_NULL,\n            blank=True,\n            null=True,\n        )\n\n        snippet_image_field = SnippetImageField(\n            verbose_name=\'Example snippet image field\',\n            null=True,\n        )\n\n        status = CharField(\n            max_length=20,\n            choices=Statuses.CHOICES,\n            default=Statuses.DRAFT,\n        )\n\n        tags = ClusterTaggableManager(through=PageTag, blank=True)\n\n        content_panels = Page.content_panels + [\n            ImageChooserPanel(\'background\'),\n            ImageChooserPanel(\'snippet_image_field\'),\n            FieldPanel(\'status\'),\n            FieldPanel(\'tags\'),\n        ]\n\n        def get_snippet_image_background(self, snippet_type):\n            return self.background and self.background.file and self.background.file.path \\\n                if snippet_type == \'default\' else None\n\n        def get_snippet_image_center(self, snippet_type):\n            return (self.background.focal_point_x, self.background.focal_point_y) \\\n                if snippet_type == \'default\' and self.background \\\n                   and self.background.focal_point_x and self.background.focal_point_y \\\n                else None\n\n        def get_snippet_image_text(self, snippet_type):\n            return self.title if snippet_type == \'default\' else None\n\n        def snippet_image_should_be_created(self):\n            return self.status == Statuses.PUBLISH\n\n        # Wagtail custom methods for create wagtail images for sharing snippet image\n        def get_snippet_image_title(self, snippet_type):\n            return self.title if snippet_type == \'default\' else None\n\n        def get_snippet_image_tags(self, snippet_type):\n            return self.tags.names() if snippet_type == \'default\' else None\n\n\nAnd use it in template:\n\n.. code-block:: html\n\n    <meta property="og:image" content="{{ image(page.snippet_image_field, \'original\') }}" />\n\n\nRead more in home_.\n\n.. _home: https://github.com/acrius/wagtail-snippet-image\n',
    'author': 'acrius',
    'author_email': 'acrius@mail.ru',
    'url': 'https://github.com/acrius/wagtail-snippet-image',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
