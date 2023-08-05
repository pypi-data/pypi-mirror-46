# -*- coding: utf-8 -*-
import json

from txlib_too.api.base import BaseModel


class Statistics(BaseModel):
    """Model class for statistics."""

    _path_to_item = '/project/%(project_slug)s/resource/%(slug)s/stats/'
    _path_to_collection = '/project/%(project_slug)s/resource/%(slug)s/stats/'

    url_fields = {'project_slug', 'slug'}