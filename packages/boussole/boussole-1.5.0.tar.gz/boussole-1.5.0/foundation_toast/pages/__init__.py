# -*- coding: utf-8 -*-
"""
The project pages map for Foundation toast
"""
from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings

from .index import Index


# Enabled pages to build
PAGES = [
    Index(destination="index.html"),
    Index(lang="fr_FR"),
]
