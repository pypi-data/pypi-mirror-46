# -*- coding: utf-8 -*-
import logging
import time
from collections import OrderedDict
from functools import partial
from weakref import WeakKeyDictionary

from frutils import readable, special_dict_to_dict
from frutils.config import Cnf

from . import Ting
from .defaults import TingValidator
from .exceptions import TingException, TingTingImplementationException
from .ting_attributes import MultiCacheResult
from .utils import create_ting_attribute_obj

log = logging.getLogger("ting")


def timeit(method):
    def timed(*args, **kw):

        attr_name = kw["attribute_name"]
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print("%r  %2.2f ms" % (attr_name, (te - ts) * 1000))
        return result

    return timed


class CacheManager(object):
    def __init__(self):

        self.caches = {}

    def get_cache(self, cache_class):

        if cache_class not in self.caches.keys():
            self.caches[cache_class] = WeakKeyDictionary()

        return self.caches[cache_class]

    def create_cache_wrapper(self, cache_class, deferred, no_cache_list):
        def wrapper(ting, attribute_name):

            try:
                if attribute_name in no_cache_list:
                    result = deferred(ting, attribute_name=attribute_name)
                else:
                    cache = self.get_cache(cache_class)
                    cached = cache.get(ting, {}).get(attribute_name, None)
                    if cached is not None:
                        result = cached
                    else:
                        result = deferred(ting, attribute_name=attribute_name)

                if isinstance(result, MultiCacheResult):
                    if attribute_name not in result.results.keys():
                        raise TingTingImplementationException(
                            "No result attribute '{}', this is an implementation bug.".format(
                                attribute_name
                            )
                        )
                    r = result.results[attribute_name]
                    for k, v in result.results.items():
                        if k not in no_cache_list:
                            cache.setdefault(ting, {})[k] = v
                else:
                    if attribute_name not in no_cache_list:
                        cache.setdefault(ting, {})[attribute_name] = result
                    r = result
            except (Exception) as e:
                log.debug(e, exc_info=1)
                raise TingException(
                    ting=ting, attribute_name=attribute_name, parent_exception=e
                )

            return r

        # return timeit(wrapper)
        return wrapper


def ting_constructor(obj_self, **ting_init_metadata):

    # not initializing mixins at all
    # super(self.__class__, self).__init__(**ting_init_metadata)

    Ting.__init__(obj_self, **ting_init_metadata)


def ting_repr(obj_self):

    repr = OrderedDict()

    for n in obj_self._ting_attribute_names:
        try:
            repr[n] = getattr(obj_self, n)
        except (Exception) as e:
            repr[n] = "error processing: {}".format(e)

    return readable(special_dict_to_dict(repr), out="pformat")


class TingCast(object):
    """
    A class to 'shape' a new 'Ting' child class. Takes all augmenters and adds them as lazy-loading
    attributes to the new class.
    """

    TING_ATTRIBUTE_CONSTRUCTOR_SCHEMA = {
        "type": "list",
        "schema": {"type": ["string", "dict"]},
    }

    TING_CAST_CONSTRUCTOR = {
        "class_name": {"type": "string", "empty": False},
        "attributes": TING_ATTRIBUTE_CONSTRUCTOR_SCHEMA,
        "ting_id_attr": {"type": "string", "default": "uuid"},
        "mixins": {"type": "list"},
    }

    @classmethod
    def from_config(cls, config):

        if not issubclass(config.__class__, Cnf):
            config = Cnf(config, validator=TingValidator)

        cc = config.add_interpreter(
            "ting_cast_constructor",
            TingCast.TING_CAST_CONSTRUCTOR,
            validator=TingValidator,
        )
        tas = []
        for attr in cc.config["attributes"]:

            ta_obj = create_ting_attribute_obj(attr)
            tas.append(ta_obj)
            # add_attr = ta_obj.provides()

        tc = TingCast(
            class_name=cc.config["class_name"],
            ting_attributes=tas,
            ting_id_attr=cc.config["ting_id_attr"],
            mixins=cc.config["mixins"],
        )
        return tc

    def __init__(self, class_name, ting_attributes, ting_id_attr="uuid", mixins=None):

        self.cache_manager = CacheManager()
        self.class_name = class_name
        self.ting_attributes = ting_attributes
        self.ting_id_attr = ting_id_attr
        if mixins is None:
            mixins = []
        self.mixins = mixins

        self.attributes = {"__init__": ting_constructor}

        all_attr = []
        for augmenter in self.ting_attributes:

            if hasattr(augmenter, "no_cache"):
                no_cache_attrs = getattr(augmenter, "no_cache")()
            else:
                no_cache_attrs = []

            function = getattr(augmenter, "get_attribute")
            cached_function = self.cache_manager.create_cache_wrapper(
                cache_class=self.class_name,
                deferred=function,
                no_cache_list=no_cache_attrs,
            )

            for attr in augmenter.provides():
                at = attr
                all_attr.append(at)

                partial_func = partial(cached_function, attribute_name=at)

                # TODO: check for only one arg
                self.attributes[at] = property(fget=partial_func)

        hierarchy = []
        for mixin in reversed(self.mixins):
            hierarchy.append(mixin)
        hierarchy.append(Ting)

        self.attributes["_ting_attribute_names"] = sorted(all_attr)
        self.class_ipml = type(self.class_name, tuple(hierarchy), self.attributes)

    def initialize_ting(self, ting_init_metadata):

        # TODO: check if all 'promised' init attributes are there
        obj = self.class_ipml(**ting_init_metadata)
        obj.id = getattr(obj, self.ting_id_attr)
        # print(self.ting_id_attr)
        # print(obj.id)
        return obj

    def get_ting_class(self):

        return self.class_ipml
