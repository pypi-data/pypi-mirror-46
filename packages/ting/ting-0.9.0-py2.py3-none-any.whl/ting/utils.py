# -*- coding: utf-8 -*-
import logging
import os
from collections import Mapping

from frutils.frutils import get_all_subclasses
from six import string_types

from .ting_attributes import TingAttribute

log = logging.getLogger("ting")


def create_folder_index_configuration(local_paths, loader_name):

    folder_index_conf = []
    used_aliases = []

    for f in local_paths:

        url = f

        alias = os.path.basename(url).split(".")[0]
        i = 1
        while alias in used_aliases:
            i = i + 1
            alias = "{}_{}".format(alias, i)

        used_aliases.append(alias)
        folder_index_conf.append(
            {"repo_name": alias, "folder_url": url, "loader": loader_name}
        )

    return folder_index_conf


def create_ting_attribute_objects(conf_list):

    result = []
    for c in conf_list:
        obj = create_ting_attribute_obj(c)
        result.append(obj)

    return result


def create_ting_attribute_obj(conf):

    if isinstance(conf, string_types):
        init = {}
        ta = conf
    elif isinstance(conf, Mapping):
        if len(conf) > 1:
            raise Exception(
                "Invalid TingAttribute construction configuration: {}".format(conf)
            )
        ta = next(iter(conf.keys()))
        init = conf[ta]
    else:
        raise Exception(
            "Invalid TingAttribute construction configuration, needs to be dict or string: {}".format(
                conf
            )
        )
    tac = None
    for n in get_all_subclasses(TingAttribute):
        if n.__name__ != ta:
            continue
        tac = n
        break

    if tac is None:
        raise Exception("Could not find TingAttribute subclass: {}".format(ta))

    ta_obj = tac(**init)
    return ta_obj
