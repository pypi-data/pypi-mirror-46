# -*- coding: utf-8 -*-
import abc
import collections
import copy
import importlib
import io
import logging
import os
import re
import time
import uuid
from collections import Mapping
from os import listdir

import six
from frutils import (
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_URL_ABBREVIATIONS_REPO,
    calculate_cache_location_for_url,
    is_url_or_abbrev,
)
from frutils.config import Cnf
from frutils.frutils import intersect_lists
from plumbum import local
from six import string_types

from frkl.utils import expand_string_to_git_details

from .defaults import TingValidator
from .ting_attributes import WrapTingAttribute
from .ting_cast import TingCast

PULL_CACHE = {}

STRING_CONTENT_TYPE_NAME = "string"

log = logging.getLogger("tings")


@six.add_metaclass(abc.ABCMeta)
class Tings(collections.Mapping):
    def __init__(
        self, repo_name, ting_cast=None, indexes=None, load_config=None, desc=None
    ):

        self._loaded = False

        self.repo_name = repo_name
        if indexes is None or not indexes:
            indexes = ["uuid"]
        self._index_names = indexes
        self._indexes = {}
        for index_key in self._index_names:
            self._indexes[index_key] = {}

        if load_config is None:
            cnf = Cnf({})
        elif isinstance(load_config, Cnf):
            cnf = load_config
        elif isinstance(load_config, Mapping):
            cnf = Cnf(load_config)
        else:
            raise Exception(
                "Invalid type for load config: {}".format(type(load_config))
            )

        if hasattr(self, "LOAD_CONFIG_SCHEMA"):
            schema = self.LOAD_CONFIG_SCHEMA
        else:
            schema = {}

        self._load_config = cnf.add_interpreter(self.__class__.__name__, schema)

        self._ting_cast = ting_cast
        self._desc = desc

        self._tings = None

    @property
    def index_names(self):
        return self._index_names

    @property
    def ting_cast(self):
        return self._ting_cast

    def desc(self):
        return self._desc

    @property
    def load_config(self):
        return self._load_config

    @abc.abstractmethod
    def provides(self):
        pass

    @abc.abstractmethod
    def load_tings(self):
        """Load available tings for this repo.

        Returns:
            dict: all available tings in the form ting_name/ting_initial_metadata
        """

        pass

    def __getitem__(self, ting_id):

        if not isinstance(ting_id, string_types):
            raise TypeError(
                "Invalid type for key '{}': {}".format(ting_id, type(ting_id))
            )

        if ting_id not in self.get_ting_names():
            raise KeyError("No entry (in default index) for key: {}".format(ting_id))

        return self.get_from_index(index_key=ting_id)

    def __len__(self):
        return len(self.indexes[self._index_names[0]])

    def __iter__(self):
        return iter(self.indexes[self._index_names[0]])

    def keys(self):
        return self.get_ting_names()

    def get_from_index(self, index_key, index_name=None):
        """
        Return a ting with a specific key value.

        Args:
            index_key (string): the key value
            index_name (string): the index where the key value should match (defaults to the first index_name or 'id')
        Returns:
            ting.ting.Ting: the ting in question
        """

        if index_name is None:
            index_name = self.index_names[0]

        result = self.indexes[index_name].get(index_key, None)
        return result

    def get_ting_map(self, index_name=None):

        if index_name is None:
            index_name = self.index_names[0]

        return self.indexes[index_name]

    def load_ting_values(self, attr_key, index_name=None):

        result = {}
        for t in self.tings:
            result[t.id] = getattr(t, attr_key)

        return result

    def get_ting_names(self, index_name=None):

        if index_name is None:
            index_name = self.index_names[0]

        if index_name not in self.indexes.keys():
            raise Exception("No index with name '{}' in tingset".format(index_name))

        return self.indexes[index_name].keys()

    @property
    def indexes(self):
        if self._loaded:
            return self._indexes

        _ = self.tings
        return self._indexes

    @property
    def tings(self):
        """Return a list of all tings available.

        Returns:
            list: all tings in this collection
        """

        if self._loaded:
            return self._tings

        if self.ting_cast is None:
            raise Exception("No 'TingCass' class provided, can't create Tings.")

        ting_list = self.load_tings()
        self._tings = []

        for ting_md in ting_list:

            try:
                ting = self.ting_cast.initialize_ting(ting_md)
            except (Exception) as e:
                log.error(e)
                raise e

            setattr(ting, "_parent_repo", self)
            setattr(ting, "_meta_parent_repo", self)

            self._tings.append(ting)
            for index_key in self.index_names:
                self._add_to_index(index_key=index_key, ting=ting)

        self._loaded = True

        return self._tings

    def _add_to_index(self, index_key, ting):

        index = self._indexes.setdefault(index_key, {})
        key = getattr(ting, index_key)
        if key is None:
            return
        if not key:
            raise Exception(
                "Invalid key for index_key '{}', can't be 'empty. Ting: {}".format(
                    index_key, ting.__dict__
                )
            )
        if key in index.keys():
            log.warning(
                "Duplicate index key '{}' for index '{}', ignoring...".format(
                    key, index_key
                )
            )
        else:
            index[key] = ting

    def __repr__(self):

        return str([t.id for t in self.tings])


class TingTings(Tings):

    TING_ATTRIBUTE_CONSTRUCTION_SCHEMA = {
        "type": "list",
        "schema": {"type": ["string", "dict"]},
    }

    TING_CONSTRUCTION_SCHEMA = {
        "class_name": {"type": "string", "empty": False, "required": True},
        "attributes": TING_ATTRIBUTE_CONSTRUCTION_SCHEMA,
        "ting_id_attr": {"type": "string", "required": False, "default": "id"},
        "mixins": {"type": "list"},
        "loaders": {
            "type": "dict",
            "keyschema": {"type": "string", "required": True, "empty": False},
            "valueschema": {
                "type": "dict",
                "schema": {
                    "attributes": TING_ATTRIBUTE_CONSTRUCTION_SCHEMA,
                    "load_config": {
                        "type": "dict",
                        "required": False,
                        "default": {},
                        "empty": True,
                    },
                    "class": {"type": "string", "required": True},
                },
            },
        },
        "repos": {"type": "list", "schema": {"type": "dict"}},
    }

    @classmethod
    def from_config(cls, tings_name, repos, cnf, **kwargs):
        if not isinstance(cnf, Cnf):
            cnf = Cnf(cnf)

        construction_config = cnf.add_interpreter(
            "ting_contstruction",
            schema=TingTings.TING_CONSTRUCTION_SCHEMA,
            validator=TingValidator,
        )
        all_tings = []
        for repo in repos:

            if isinstance(repo, string_types):
                repo = {"folder_url": repo}

            repo = copy.copy(repo)
            loader = repo.pop("loader", None)
            if loader is None:

                _loaders = construction_config.config["loaders"]
                if len(_loaders) != 1:
                    raise Exception("No loader provided for repo: {}".format(repo))

                loader = list(_loaders.keys())[0]
                log.debug("Auto-choosing single loader: {}".format(loader))

            loader_config = construction_config.config["loaders"].get(loader, None)
            if loader_config is None:
                raise Exception("No loader config for loader: {}".format(loader))

            loader_attributes = loader_config.get("attributes", [])
            general_attribuutes = construction_config.config.get("attributes", [])
            all_attributes = loader_attributes + general_attribuutes
            mixins = construction_config.get("mixins", [])

            tc_confing = {
                "class_name": construction_config.config["class_name"],
                "attributes": all_attributes,
                "ting_id_attr": construction_config.config["ting_id_attr"],
                "mixins": mixins,
            }
            tc = TingCast.from_config(tc_confing)

            module, class_name = loader_config["class"].rsplit(".", 1)
            loader_class = getattr(importlib.import_module(module), class_name)

            repo["ting_cast"] = tc
            repo["load_config"] = loader_config.get("load_config", {})

            if "repo_name" not in repo.keys():
                if "folder_url" in repo.keys() and repo["folder_url"]:
                    repo["repo_name"] = repo["folder_url"]

            tings = loader_class(**repo)
            all_tings.append(tings)

        result = TingTings(tings_name, tingsets=all_tings, **kwargs)

        return result

    @classmethod
    def from_folders(
        cls,
        tingset_name,
        repos,
        ting_cast=None,
        load_config=None,
        add_current_dir=False,
        **init_args
    ):
        """
        Generic factory method, to create a :class:`MetaTingSet` (child-class) object that contains only :class:`FolderTingSet` children.

        Args:
            tingset_name (str): the name/id of the new Tings object
            repos (dict, str): a dictionary or string that contains the folders to parse. If string, basename (without extension) will be used as key and whole string as value in a one-item dict.
            ting_cast (TingCast): the :class:`TingCast` object to use to create :class:`Ting`s. If None, a potential 'DEFAULT_TING_CAST' class attribute will be used.
            load_config (Cnf, dict): a :class:`Cnf` to configure certain aspects of loading Tings
            **init_args (dict): additional constructor args for the child class
        """

        if ting_cast is None:
            if not hasattr(cls, "DEFAULT_TING_CAST"):
                raise Exception(
                    "No 'ting_cast' attribute provided, and class '{}' does not have a 'DEFAULT_TING_CAST' class attribute".format(
                        cls.__name__
                    )
                )

            ting_cast = getattr(cls, "DEFAULT_TING_CAST")
            if not isinstance(ting_cast, TingCast):
                ting_cast = ting_cast()

        if isinstance(repos, string_types):
            if repos.endswith(os.path.sep):
                repos = repos[0, -1]
            basename = os.path.basename(repos).split(os.path.sep)[0]
            repos = {basename: repos}

        tingsets = []
        if add_current_dir:
            path = os.getcwd()
            ft = FileTings(
                repo_name="current",
                folder_url=path,
                ting_cast=ting_cast,
                force_non_recursive=True,
                load_config=load_config,
            )
            tingsets.append(ft)

        for alias, url in repos.items():
            ft = FileTings(
                repo_name=alias,
                folder_url=url,
                ting_cast=ting_cast,
                load_config=load_config,
            )
            tingsets.append(ft)

        return cls(
            repo_name=tingset_name,
            tingsets=tingsets,
            load_config=load_config,
            **init_args
        )

    def __init__(self, repo_name, tingsets, indexes=None, load_config=None, desc=None):

        super(TingTings, self).__init__(
            repo_name, indexes=indexes, load_config=load_config, desc=desc
        )
        if isinstance(tingsets, Tings):
            tingsets = [tingsets]

        all_provides = [ts.provides() for ts in tingsets]
        self._provide_attrs = intersect_lists(all_provides)
        self.tingsets = tingsets

    def provides(self):

        return self._provide_attrs

    def load_tings(self):

        # not necessary here
        pass

    def add_tings(self, tings):

        # if not issubclass(tings, Tings):
        #     raise Exception("Can't add non-Tings object to Tings: {}".format(Tings))

        for ting in tings.tings:

            setattr(ting, "_meta_parent_repo", self)
            self._tings.append(ting)
            for index_key in self.index_names:
                self._add_to_index(index_key, ting)

    @property
    def tings(self):
        """Return a list of all tings available.

        Returns:
            list: all tings in this collection
        """

        if self._tings is not None:
            return self._tings

        self._tings = []

        for t in self.tingsets:

            if not t.tings:
                for index_key in self.index_names:
                    self._indexes.setdefault(index_key, {})
            else:
                for ting in t.tings:

                    setattr(ting, "_meta_parent_repo", self)
                    self._tings.append(ting)
                    for index_key in self.index_names:
                        self._add_to_index(index_key, ting)

        return self._tings


class WrappedTings(Tings):
    def __init__(
        self,
        repo_name,
        tings,
        wrapped_ting_attr_name,
        wrapped_attr_names,
        extra_attributes=None,
        indexes=None,
        load_config=None,
        desc=None,
    ):

        """
        A Ting collection that wraps another list of tings, and optionally extra attributes.

        Args:
            repo_name (str): The repo name
            tings (list): A list of tings
            wrapped_ting_attr_name: The name of the attribute name under which the wrapped ting is accessible.
            wrapped_attr_names: A list of attribute names to make accessible directly in the wrapping ting.
            extra_attributes: extra attributes for the wrapping ting
            indexes: The indexes.
            load_config: The load config.
            desc: A description of this ting collection.
        """

        attributes = [
            WrapTingAttribute(
                wrapped_ting_attr_name=wrapped_ting_attr_name,
                attr_names=wrapped_attr_names,
            )
        ]
        attributes.extend(extra_attributes)

        mixins = []
        ting_cast = TingCast(
            "Pageling",
            ting_attributes=attributes,
            ting_id_attr="url_path",
            mixins=mixins,
        )

        super(WrappedTings, self).__init__(
            repo_name=repo_name,
            indexes=indexes,
            load_config=load_config,
            ting_cast=ting_cast,
            desc=desc,
        )

        self.wrapped_tings = tings
        self.wrapped_ting_attr_name = wrapped_ting_attr_name

    def load_tings(self):

        result = []

        for ting in self.wrapped_tings:

            id = str(uuid.uuid4())
            md = {"uuid": id, self.wrapped_ting_attr_name: ting}
            result.append(md)

        return result

    def provides(self):

        return [self.wrapped_ting_attr_name]


class DictTings(Tings):

    LOAD_CONFIG_SCHEMA = {}

    def __init__(
        self,
        repo_name,
        data,
        ting_cast,
        indexes=None,
        load_config=None,
        desc=None,
        key_name="name",
        meta_name="meta",
    ):
        """
        A collections of Tings, created from a dict.

        Args:
            repo_name: the alias of this repo
            data: the dict that is used to construct the Tings
            ting_cast: the ting cast
            indexes: the keys to create indexes from
            load_config: the load config
            desc: a description of this Ting repo
            key_name: the name that is used for the Ting name key
            meta_name: the name that is used for the Ting dict content
        """
        super(DictTings, self).__init__(
            repo_name=repo_name,
            indexes=indexes,
            load_config=load_config,
            ting_cast=ting_cast,
            desc=desc,
        )

        self.data = data
        self.key_name = key_name
        self.meta_name = meta_name

    def load_tings(self):

        result = []
        for k, v in self.data.items():

            id = str(uuid.uuid4())
            md = {"uuid": id, self.meta_name: v, self.key_name: k}
            result.append(md)
        return result

    def provides(self):

        return [self.key_name, self.meta_name]


def create_ting_filter_func(conf):

    ignore_prefixes = conf.get("folder_load_ignore_file_prefixes", [])
    ignore_postfixes = conf.get("folder_load_ignore_file_postfixes", [])
    filename_regex = conf.get("folder_load_file_match_regex", None)
    ignore_hidden_files = conf.get("folder_load_ignore_hidden_files", True)

    def filter_func(path):

        for ip in ignore_postfixes:
            if path.endswith(ip):
                return False

        file_name = os.path.basename(path)
        if ignore_hidden_files and file_name.startswith("."):
            return False
        for ip in ignore_prefixes:
            if file_name.startswith(ip):
                return False

        if filename_regex is not None:
            if not re.search(filename_regex, file_name):
                return False

        return True

    return filter_func


def load_content_func(full_path):
    def load_func():

        with io.open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content

    return load_func


class FileTings(Tings):

    LOAD_CONFIG_SCHEMA = {
        "folder_load_ignore_file_prefixes": {
            "type": "list",
            "default": [],
            "empty": True,
            "schema": {"type": "string"},
            "required": False,
        },
        "folder_load_ignore_file_postfixes": {
            "type": "list",
            "default": [],
            "empty": True,
            "schema": {"type": "string"},
            "required": False,
        },
        "folder_load_file_match_regex": {"type": "string", "required": False},
        "folder_load_use_subfolders": {
            "type": "boolean",
            "default": True,
            "required": False,
        },
        "folder_load_ignore_hidden_files": {
            "type": "boolean",
            "default": True,
            "required": False,
        },
    }

    def provides(self):

        return [
            "full_path",
            "rel_path",
            "filename",
            "filename_no_ext",
            "rel_path_no_ext",
            "uuid",
        ]

    def __init__(
        self,
        repo_name,
        folder_url,
        ting_cast,
        indexes=None,
        load_config=None,
        desc=None,
        force_non_recursive=False,
    ):
        """
        A :class:`Tings` implementation that walks recursively through a folder and gets all tings in it.


        Args:
            repo_name: the Tings alias
            folder_url (str): the local (or remote git) url to the folder
            ting_cast (TingCast): the :class:`TingCast` object to use to construct the :class:`Ting`s
            indexes (list): a list of attributes (added by the :class:`TingCast`s list of :class:`TingAttribute`s to use as index keys, one index per key will be created
            load_config (Cnf): the configuration that determines how to load the :class:`Ting`s
            desc (str): a description of this repo
            force_non_recursive (bool): can overwrite the 'subfolder' config option
        """

        super(FileTings, self).__init__(
            repo_name=repo_name,
            indexes=indexes,
            load_config=load_config,
            ting_cast=ting_cast,
            desc=desc,
        )

        self.ting_filter_func = create_ting_filter_func(self.load_config)
        self.folder_url = folder_url

        self.force_non_recursive = force_non_recursive

        if is_url_or_abbrev(folder_url):
            self.is_local = False
            self.git_details = expand_string_to_git_details(
                folder_url, default_abbrevs=DEFAULT_URL_ABBREVIATIONS_REPO
            )
            self.full_base_url = self.git_details["url"]

            basename = os.path.basename(self.full_base_url)
            if basename.endswith(".git"):
                basename = basename[0:-4]
            branch = self.git_details.get("branch", "master")
            postfix = os.path.join(branch, basename)
            self.local_path = calculate_cache_location_for_url(
                self.full_base_url, postfix=postfix
            )
        else:
            self.is_local = True
            self.git_details = None
            self.full_base_url = os.path.realpath(os.path.expanduser(self.folder_url))
            self.local_path = self.full_base_url

        self.local_parent_path = os.path.dirname(self.local_path)

    def load_tings(self):

        result = []

        if not os.path.exists(self.local_path):
            return result

        if os.path.isdir(self.local_path):
            is_folder = True
        else:
            is_folder = False

        if not is_folder:

            if self.ting_filter_func(self.local_path):

                md = self.construct_ting_metadata(self.local_path)

                return [md]

        else:

            if (
                self.load_config.get("folder_load_use_subfolders")
                and not self.force_non_recursive
            ):

                for root, dirnames, filenames in os.walk(self.local_path, topdown=True):

                    dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDE_DIRS]

                    for filename in [
                        f
                        for f in filenames
                        if self.ting_filter_func(os.path.join(root, f))
                    ]:

                        temp = os.path.join(root, filename)
                        md = self.construct_ting_metadata(temp)

                        result.append(md)

            else:
                paths = [
                    os.path.join(self.local_path, f)
                    for f in listdir(self.local_path)
                    if os.path.isfile(os.path.join(self.local_path, f))
                    and self.ting_filter_func(os.path.join(self.local_path, f))
                ]
                for path in paths:
                    md = self.construct_ting_metadata(path)
                    result.append(md)

            return result

    def construct_ting_metadata(self, abs_path):

        filename = os.path.basename(abs_path)
        filename_no_ext = filename.split(".")[0]
        ext = ".".join(filename.split(".")[1:])
        rel_path = os.path.relpath(abs_path, self.local_path)
        rel_path_no_ext = os.path.join(os.path.dirname(rel_path), filename_no_ext)

        id = str(uuid.uuid4())
        result = {
            "uuid": id,
            "full_path": abs_path,
            "rel_path": rel_path,
            "rel_path_no_ext": rel_path_no_ext,
            "filename": filename,
            "file_ext": ext,
            "filename_no_ext": filename_no_ext,
        }

        return result

    def ensure_local(self, force_update=False):
        """

        Args:
            force_update (bool): whether to force an update in case the repo is remote
        Returns:
            bool: whether the repo was updated or not
        """

        if self.is_local:
            return False

        if not self.load_config.get("allow_remote"):

            raise Exception("Remote repositories not allowed.")

        if os.path.exists(self.local_path) and not force_update:
            return False

        branch = self.git_details.get("branch", None)

        if not os.path.exists(self.local_path):

            log.debug("cloning repo: {}...".format(self.full_base_url))
            git = local["git"]
            cmd = ["clone"]
            if branch is not None:
                cmd.append("-b")
                cmd.append(branch)
            cmd.append(self.full_base_url)
            cmd.append(self.local_path)
            rc, stdout, stderr = git.run(cmd)

            if rc != 0:
                raise Exception(
                    "Could not clone repository '{}': {}".format(
                        self.full_base_url, stderr
                    )
                )
            PULL_CACHE[self.full_base_url] = time.time()
            return True

        else:
            # TODO: check how much time has passed
            if self.full_base_url in PULL_CACHE:
                log.debug("Not pulling again: {}".format(self.full_base_url))
                return False

            # TODO: check if remote/branch is right?
            log.debug("pulling from remote: {}...".format(self.full_base_url))
            git = local["git"]
            cmd = ["pull", "origin"]
            if branch is not None:
                cmd.append(branch)
            with local.cwd(self.local_parent_path):
                rc, stdout, stderr = git.run(cmd)

                if rc != 0:
                    raise Exception(
                        "Could not pull repository '{}': {}".format(
                            self.full_base_url, stderr
                        )
                    )

            PULL_CACHE[self.full_base_url] = time.time()

    def get_local_path(self, force_update=False):
        """
        Return the local path, optionally update the repo (in case it is remote).

        Args:
            force_update (boolean): update repo if remote
        Returns:
            str: the absolute path to the repo
        """

        self.ensure_local(force_update=force_update)

        return self.local_path
