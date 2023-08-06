# -*- coding: utf-8 -*-

"""Main module."""
import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Ting(object):
    def __init__(self, **kwargs):
        """

        Args:
            name (str): the ting name (unique among this set of Tings
            content (dict): a dict of content_type/[content_string or content_load_func]
            **kwargs (dict): unstructured metadata that will be converted into attributes
        """
        self.id = None

        for k, v in kwargs.items():
            setattr(self, k, v)
