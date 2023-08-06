# -*- coding: utf-8 -*-
from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings


class Index(PageViewBase):
    """
    Default index page
    """
    title = "My project"
    template_name = "index.html"
    destination = "{language_code}/index.html"

    def get_context(self):
        super().get_context()

        self.context.update({
            'DEFAULT_LANGUAGE': settings.LANGUAGE_CODE,
            'LANGUAGES': settings.LANGUAGES,
        })

        return self.context
