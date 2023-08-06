# -*- coding: utf-8 -*-
import abc
import copy
import io
import logging
import uuid
from collections import Mapping
from typing import Sequence

import click
import six
from frutils import dict_merge, get_template_keys
from frutils.doc import Doc
from frutils.frutils import auto_parse_string
from frutils.parameters import VarsTypeSimple
from markdown import Markdown
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from six import string_types

log = logging.getLogger("tings")

yaml = YAML()


class MultiCacheResult(object):
    def __init__(self, **results):
        self.results = results


@six.add_metaclass(abc.ABCMeta)
class TingAttribute(object):
    @classmethod
    def create(cls, attr_func, provides, requires=[]):

        if not provides:
            raise Exception("Invalid call.")
        class_name = "".join([s.title() for s in provides]) + "Ting"
        class_name = class_name.replace("_", "")

        def provides_func(ting):
            return provides

        def requires_func(ting):
            return requires

        attr_map = {
            "get_attribute": attr_func,
            "requires": lambda: requires_func,
            "provides": lambda: provides_func,
        }

        new_class = type(class_name, (), attr_map)
        return new_class()

    def __init__(self):
        pass

    def requires(self):
        """Return an list of attributes this object requires to be able to augment the Ting."""
        return []

    def requires_optional(self):
        """Return a list of optional attributes this object can use to augment a ting."""

        return []

    @abc.abstractmethod
    def provides(self):
        """Return a list of attributes this object will add to a Ting."""
        pass

    @abc.abstractmethod
    def get_attribute(self, ting, attribute_name=None):

        pass

    # def optional(self):
    #     """Returns an list of optional attributes this object can use to do a better job augmenting the Ting."""
    #     return []


class FileStringContentAttribute(TingAttribute):
    def __init__(self, target_attr_name="ting_content"):

        self.target_attr_name = target_attr_name

    def get_attribute(self, ting, attribute_name=None):

        with io.open(ting.full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content

    def requires(self):

        return ["full_path"]

    def provides(self):

        return [self.target_attr_name]


class StaticDictContentAttribute(TingAttribute):
    def __init__(self, dict_data, target_attr_name="default_metadata"):

        self.dict_data = dict_data
        self.target_attr_name = target_attr_name

    def requires(self):
        return []

    def provides(self):

        return [self.target_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        return self.dict_data


class DictContentAttribute(TingAttribute):
    def __init__(
        self,
        dict_name="metadata",
        source_attr_name="ting_content",
        default=None,
        copy_default=True,
        content_type="auto",
    ):

        self.dict_name = dict_name
        self.source_attr_name = source_attr_name
        self.default = default
        self.copy_default = True
        self.content_type = content_type

    def requires(self):

        return [self.source_attr_name]

    def provides(self):

        return [self.dict_name]

    def get_attribute(self, ting, attribute_name=None):

        content = getattr(ting, self.source_attr_name)
        if not content:
            if self.default is None:
                return None
            if self.copy_default:
                return copy.deepcopy(self.default)
            else:
                return self.default

        if not isinstance(content, string_types):
            raise Exception("Internal error: raw metadata is not a string type")

        loaded = auto_parse_string(
            content, content_type=self.content_type, default_if_empty={}
        )
        return loaded


class MirrorAttribute(TingAttribute):
    def __init__(self, source_attr_name, target_attr_name):
        self.target_attr_name = target_attr_name
        self.source_attr_name = source_attr_name

    def provides(self):

        return [self.target_attr_name]

    def requires_optional(self):

        return [self.source_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        return getattr(ting, self.source_attr_name)


class ValueAttribute(TingAttribute):
    def __init__(self, target_attr_name, source_attr_name="metadata", default=None):

        self.target_attr_name = target_attr_name
        self.parent_attr_name = source_attr_name
        self.default = default

    def provides(self):

        return [self.target_attr_name]

    def requires(self):

        return [self.parent_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        parent = getattr(ting, self.parent_attr_name)

        if isinstance(parent, Mapping):
            result = parent.get(self.target_attr_name, None)

        elif hasattr(parent, self.target_attr_name):
            result = getattr(parent, self.target_attr_name)

        if result is None and self.default is not None:
            return copy.deepcopy(self.default)
        else:
            return result


class FrontmatterAndContentAttribute(TingAttribute):
    def __init__(
        self,
        metadata_name="frontmatter",
        content_name="content",
        source_attr_name="ting_content",
        default_metadata_attr_name=None,
        metadata_strategies=None,
        metadata_formats=None,
        frontmatter_separator="---",
        comment_token="#",
    ):
        """
        An attribute to create metadata and content attributes out of a Ting.

        There are several ways metadata can be retrieved, depending on the configuration of this Attribute.
        The most common case is the content of a text file and splitting that up into frontmatter (metadata) and content
        (like a lot of static site generators do). If the 'metadata_strategies' value is None, then this attribute
        will do this, it'll interprete content that is located at the beginning of the text content, two lines containing
        the frontmatter seperator ('---' by default).

        Currently only the 'frontmatter' and 'comments' strategies are implemented. In the future it will be possible
        to try several strategies until one of them works, but this is not supported just yet.

        Args:
            metadata_name:
            content_name:
            source_attr_name:
            default_metadata_attr_name:
        """

        self.metadata_name = metadata_name
        self.content_name = content_name
        self.source_attr_name = source_attr_name
        self.default_metadata_attr_name = default_metadata_attr_name
        self.metadata_strategies = []
        if metadata_strategies is None:
            metadata_strategies = ["frontmatter"]
        for s in metadata_strategies:
            s = s.lower()
            if s in self.metadata_strategies:
                continue
            if s not in ["frontmatter", "comments"]:
                raise Exception("Metadata strategy '{}' not supported.".format(s))
            self.metadata_strategies.append(s)
        self.metadata_formats = []
        if metadata_formats is None:
            metadata_formats = ["yaml"]
        for f in metadata_formats:
            f = f.lower()
            if f in self.metadata_formats:
                continue
            if f not in ["yaml"]:
                raise Exception("Metadata format '{}' not supported yet.".format(f))
            self.metadata_formats.append(f)
        self.frontmatter_separator = frontmatter_separator
        self.comment_token = comment_token

    def requires(self):

        return [self.source_attr_name]

    def provides(self):

        return [self.content_name, self.metadata_name]

    def get_attribute(self, ting, attribute_name=None):

        for strategy in self.metadata_strategies:

            if strategy == "frontmatter":

                metadata, content = self.get_from_frontmatter(ting)

            elif strategy == "comments":

                metadata, content = self.get_from_comments(ting)

            else:
                raise Exception("Invalid metadata strategy: {}".format(strategy))

            if metadata is None:
                continue

            if self.default_metadata_attr_name is not None:
                default_metadata = getattr(ting, self.default_metadata_attr_name)
                metadata = dict_merge(default_metadata, metadata, copy_dct=True)

            result = {self.content_name: content, self.metadata_name: metadata}
            return MultiCacheResult(**result)

    def get_from_comments(self, ting):

        string_content = getattr(ting, self.source_attr_name)
        lines = string_content.strip().split("\n")

        if not lines:
            return {}, ""

        start = 0

        if lines[0].strip().startswith("#!"):
            start = 1

        metadata_part_finished = False
        metadata_lines = []
        content = []
        for line in lines[start:]:

            if not line.strip():
                continue

            if not metadata_part_finished:
                if line.startswith(self.comment_token):
                    metadata_lines.append(line)
                    continue

            metadata_part_finished = True
            content.append(line)

        if not metadata_lines:
            return {}, "\n".join(content)

        content_string = ""
        remove_length = None
        for line in metadata_lines:
            if remove_length is None:
                temp = line[len(self.comment_token) :].strip()  # noqa
                if not temp:
                    continue

                remove_length = line.find(temp)

            line = line[remove_length:]
            content_string = content_string + line + "\n"

        try:
            metadata = yaml.load(content_string)
        except (Exception) as e:
            log.warning(
                "Could not parse frontmatter for markdown file '{}': {}".format(
                    ting.full_path, e
                )
            )

        return metadata, "\n".join(content)

    def get_from_frontmatter(self, ting):

        string_content = getattr(ting, self.source_attr_name)
        lines = string_content.strip().split("\n")

        meta = []
        content = []

        metadata_start = -1
        metadata_finish = -1

        for ln, l in enumerate(lines):

            if metadata_finish < 0:
                if metadata_start < 0:
                    if l.strip() == self.frontmatter_separator:
                        metadata_start = ln + 1
                    else:
                        metadata_start = 0
                        metadata_finish = 0
                        break
                    continue

                if metadata_start >= 0:
                    if l.strip() == self.frontmatter_separator:
                        metadata_finish = ln - 1
                        continue

                    meta.append(l)
                    continue

            else:
                content.append(l)

        if not meta:
            frontmatter = {}
            content = lines
        else:
            try:
                frontmatter = yaml.load("\n".join(meta))
            except (Exception) as e:
                log.warning(
                    "Could not parse frontmatter for markdown file '{}': {}".format(
                        ting.full_path, e
                    )
                )
                raise e

        return frontmatter, "\n".join(content)


class HtmlFormatTingAttribute(TingAttribute):
    def __init__(self):

        extensions = [
            "codehilite",
            "admonition",
            "pymdownx.extra",
            "pymdownx.details",
            "tables",
            "attr_list",
            "toc",
            "def_list",
        ]
        extension_configs = {
            "codehilite": {"css_class": "codehilite"},
            # "outline": {
            #     "wrapper_cls": "doc-section"
            # }
        }

        self.markdown_renderer = Markdown(
            extensions=extensions, extension_configs=extension_configs
        )

    def requires(self):

        return ["markdown_content"]

    def provides(self):

        return ["html_format"]

    def get_attribute(self, ting, attribute_name=None):

        markdown = ting.markdown_content

        html = self.markdown_renderer.convert(markdown)
        return html


# class MetaTingSetAttribute(TingAttribute):
#
#     def __init__(self, meta_tingset, attr_name="meta_parent"):
#         self.meta_tingset = meta_tingset
#         self.attr_name = attr_name
#
#     def requires(self):
#
#         return []
#
#     def provides(self):
#
#         return [self.attr_name]
#
#     def get_attribute(self, ting, attribute_name=None):
#
#         return self.meta_tingset
class ArgsAttribute(TingAttribute):
    def __init__(
        self,
        target_attr_name="args",
        source_attr_name="meta",
        index_attr_name=None,
        import_key="_import",
        default_arg=None,
        validate_list_attr=None,
        filtered_attr_name=None,
    ):
        """
        Provide a dictionary that uses the argument name as key, and a dictionary containing the argument schema and documentation
        as a value.

        Args:
            target_attr_name (str): the target attribute name
            source_attr_name (str): the source attribute name, needs to be a Mapping
            import_key (str): the key that indicates an import
            default_arg (dict): default argument to use, if not provided this object will throw an error if no arg exists for a key
            index_attr_name (Mapping): the lookup index, in case the source value dict contains the import_key
            validate_list_attr (str): an optional attribute name, if provided, the argument list will be checked and fail if any argument is missing,
            filtered_attr_name (str): if provided and the validate_list_attr option is enabled, an attribute with this name will be created that contains the filtered list
        """

        self.target_attr_name = target_attr_name
        self.parent_attr_name = source_attr_name
        self.index_attr_name = index_attr_name
        self.import_key = import_key
        self.default_arg = default_arg
        self.validate_list_attr = validate_list_attr
        self.filtered_attr_name = filtered_attr_name

    def requires(self):

        return [self.source_attr_name]

    def requires_optional(self):

        if self.index_attr_name:
            return [self.index_attr_name]
        return []

    def provides(self):

        if self.validate_list_attr is not None and self.filtered_attr_name is not None:
            return [self.target_attr_name, self.filtered_attr_name]
        else:
            return [self.target_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        parent = getattr(ting, self.parent_attr_name)

        if isinstance(parent, Mapping):
            result = parent.get(self.target_attr_name, {})
        elif hasattr(parent, self.target_attr_name):
            result = getattr(ting, self.target_attr_name)

        _import = result.pop(self.import_key, None)

        if _import is not None:

            if not self.index_attr_name:
                raise Exception(
                    "No index provided, can't import args from: {}".format(_import)
                )

            index = getattr(ting, self.index_attr_name)
            if isinstance(_import, string_types):
                _import = [_import]

            for i in _import:

                if "::" in i:
                    other_name, arg_name = i.split("::", 1)
                else:
                    other_name = i
                    arg_name = None

                other_args = index.get(other_name, None)
                if other_args is None:
                    raise Exception(
                        "Could not find item '{}' for arg import in '{}'".format(
                            other_name, ting.id
                        )
                    )

                other_args = other_args.args

                if arg_name is not None:
                    if arg_name not in other_args.keys():
                        raise Exception(
                            "item '{}' does not have arg '{}' for import into '{}'".format(
                                other_name, arg_name, ting.id
                            )
                        )
                    other_args = {arg_name: other_args[arg_name]}

                result = dict_merge(other_args, result, copy_dct=True)

        # output(result, output_type="yaml")

        if self.validate_list_attr is not None:
            filtered = {}
            keys = getattr(ting, self.validate_list_attr)
            for key in keys:
                if key not in result.keys():
                    if self.default_arg is None:
                        raise Exception(
                            "No argument found for key '{}' in: {}".format(key, ting.id)
                        )
                    else:
                        filtered[key] = copy.deepcopy(self.default_arg)
                else:
                    filtered[key] = result[key]

            if self.filtered_attr_name is not None:
                r = {self.target_attr_name: result, self.filtered_attr_name: filtered}
                return MultiCacheResult(**r)

        return result

    # def provides(self):
    #
    #     return ["args", "args_raw"]


class TemplateKeysAttribute(TingAttribute):
    def __init__(
        self, source_attr_name, target_attr_name="template_keys", jinja_env=None
    ):

        self.source_attr_name = source_attr_name
        self.target_attr_name = target_attr_name
        self.jinja_env = jinja_env

    def requires(self):
        return [self.source_attr_name]

    def provides(self):
        return [self.target_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        source_attr = getattr(ting, self.source_attr_name)
        template_keys = get_template_keys(source_attr, jinja_env=self.jinja_env)

        return template_keys


class Arg(object):
    @classmethod
    def from_keys(cls, keys, args, default_schema=None):
        result = {}
        for key in keys:
            arg_dict = args.get(key, {})
            # arg_dict = args.get(key, None)
            arg = Arg(key, arg_dict, default_schema=default_schema)
            result[key] = arg

        return result

    def __init__(
        self,
        key,
        arg_dict,
        default_schema=None,
        allow_no_schema=True,
        is_auto_arg=False,
    ):

        if not allow_no_schema and arg_dict is None:
            raise Exception("No schema provided for key: {}".format(key))

        self._id = uuid.uuid4()
        import traceback

        self._traceback = traceback.extract_stack()

        self._key = key
        self._arg_dict = arg_dict
        self.default_schema = default_schema

        self.is_auto_arg = is_auto_arg

        if default_schema:
            temp = dict_merge(default_schema, arg_dict, copy_dct=True)
        else:
            temp = copy.copy(arg_dict)

        doc_dict = temp.pop("doc", None)
        self._cli = temp.pop("cli", {})
        self._secret = temp.pop("secret", False)
        aliases = temp.pop("aliases", None)
        if not aliases:
            aliases = [self._key]
        if isinstance(aliases, string_types):
            aliases = [aliases]
        self._aliases = aliases
        self._doc = Doc(doc_dict=doc_dict)
        self._schema = temp
        self._process_path = []
        self._child_args = []
        self._var_template = None

    def __str__(self):

        return self.__repr__()

    def __repr__(self):

        return "[Arg: key={}, short_help={}, var_template={}, childs={}]".format(
            self.key,
            self.doc.get_short_help(use_help=True),
            self._var_template,
            self._child_args,
        )

    def pretty_print_dict(self, include_arg_key=False, full_details=False):

        arg = CommentedMap()
        if include_arg_key:
            arg["key"] = self._key

        arg["doc"] = CommentedMap()
        arg["doc"]["short_help"] = self._doc.get_short_help(
            list_item_format=False, use_help=False
        )
        arg["doc"]["help"] = self._doc.get_help(use_short_help=False, default="n/a")
        if self._doc.get_long_help():
            arg["doc"]["long_help"] = self._doc.get_long_help()
        if self._doc.get_further_reading():
            arg["doc"]["further_reading"] = self._doc.get_further_reading()

        if self._secret:
            arg["secret"] = True

        if not full_details:
            arg["type"] = self._schema.get("type", "n/a")
            arg["required"] = self._schema.get("required", True)
            arg["empty"] = self._schema.get("empty", False)
        else:
            IMPORTANT = ["type", "required", "empty"]
            for k in IMPORTANT:
                value = self._schema.get(k, "n/a")
                arg[k] = value
            for key in sorted(self._schema.keys()):
                if key not in IMPORTANT:
                    arg[key] = self._schema[key]
            arg["cli"] = self._cli

        return arg

    @property
    def aliases(self):
        return self._aliases

    @property
    def var_template(self):
        return self._var_template

    @var_template.setter
    def var_template(self, var_template):
        self._var_template = var_template

    @property
    def child_args(self):
        return self._child_args

    def add_child(self, child):

        if child.secret:
            self._secret = True

        self._child_args.append(child)

    @property
    def required(self):
        if self.default is not None:
            return False
        else:
            return self._schema["required"]

    @property
    def secret(self):

        if self._secret is True:
            return True

    @property
    def key(self):
        return self._key

    @property
    def doc(self):
        return self._doc

    @property
    def schema(self):
        return self._schema

    @property
    def cli(self):
        return self._cli

    @property
    def type(self):
        return self.schema.get("type", "string")

    @property
    def empty(self):
        return self.schema["empty"]

    @property
    def default(self):
        return self.schema.get("default", None)

    @property
    def coerce(self):
        return self.schema.get("coerce", None)


class RequiredArgsAttribute(TingAttribute):
    def __init__(
        self,
        target_attr_name="required_args",
        args_attr_name="args",
        template_keys_attr_name="template_keys",
    ):

        self.target_attr_name = target_attr_name
        self.args_attr_name = args_attr_name
        self.template_keys_attr_name = template_keys_attr_name

    def provides(self):

        return [self.target_attr_name]

    def requires(self):

        return [self.args_attr_name, self.template_keys_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        pass


class CliArgsAttribute(TingAttribute):

    CLICK_CEREBUS_ARG_MAP = {
        "string": str,
        "float": float,
        "integer": int,
        "boolean": bool,
        "dict": VarsTypeSimple(),
        "password": str,
        # "list": list
    }

    DEFAULT_CLI_SCHEMA = {"show_default": True, "param_type": "option"}

    def __init__(
        self,
        target_attr_name="cli_args",
        var_names_attr_name="template_keys",
        args_attr_name="args",
        default_arg=None,
    ):

        self.target_attr_name = target_attr_name
        self.var_names_attr_name = var_names_attr_name
        self.args_attr_name = args_attr_name
        self.default_arg = default_arg

    def provides(self):

        return [self.target_attr_name]

    def requires(self):

        return [self.var_names_attr_name, self.args_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        # TODO: validate

        required_vars = getattr(ting, self.var_names_attr_name)
        args = getattr(ting, self.args_attr_name)

        result = []
        for var in required_vars:
            arg = args.get(var, None)
            if arg is None:
                if self.default_arg is None:
                    raise Exception("No argument definition for: {}".format(arg))
                else:
                    arg = copy.deepcopy(self.default_arg)

            parameter = self.create_parameter(var, arg)
            if parameter is not None:
                result.append(parameter)
            else:
                continue
            #     raise Exception("Can't assemble cli parameter for var: {}".format(var))

        return result

    def create_parameter(self, var, arg):

        if not arg.get("cli", {}).get("enabled", True):
            return None

        option_properties = dict_merge(
            CliArgsAttribute.DEFAULT_CLI_SCHEMA, arg.get("cli", {}), copy_dct=True
        )

        param_type = option_properties.pop("param_type")

        option_properties["required"] = arg.get("required", True)
        if arg.get("default", None) is not None:
            option_properties["default"] = arg["default"]

        if "param_decls" not in option_properties.keys():
            if param_type == "option":
                decls = []
                for a in arg.get("aliases", [var]):
                    if len(a) == 1:
                        decls.append("-{}".format(a))
                    else:
                        a = a.replace("_", "-")
                        decls.append("--{}".format(a))
                option_properties["param_decls"] = decls
            else:
                option_properties["param_decls"] = [var]

        if "metavar" not in option_properties.keys():
            option_properties["metavar"] = var.upper()

        # setting type
        cerberus_type = arg.get("type", None)

        if cerberus_type is not None:

            if not isinstance(cerberus_type, string_types) and isinstance(
                cerberus_type, Sequence
            ):
                log.debug("Not converting multiple types for argument: {}".format(var))
            else:

                replacement = CliArgsAttribute.CLICK_CEREBUS_ARG_MAP.get(
                    cerberus_type, None
                )
                if replacement is not None:
                    if replacement == bool:
                        if "is_flag" not in option_properties.keys():
                            option_properties["is_flag"] = True
                            # we don't add the type here, otherwise click fails for whatever reason
                    else:
                        option_properties["type"] = replacement

                elif cerberus_type == "list":
                    schema_type = arg.get("type", "string")
                    replacement = CliArgsAttribute.CLICK_CEREBUS_ARG_MAP.get(
                        schema_type, click.STRING
                    )
                    option_properties["type"] = replacement
                    if param_type == "option":
                        option_properties["multiple"] = True
                    else:
                        option_properties["nargs"] = -1
                else:
                    raise Exception(
                        "Type '{}' not implemented yet.".format(cerberus_type)
                    )

        option_properties.pop("enabled", None)
        option_properties.pop("doc", None)

        if param_type == "option":
            doc = Doc(arg.get("doc", {}))
            option_properties["help"] = doc.get_short_help()

            p = click.Option(**option_properties)
        else:
            option_properties.pop("show_default", None)
            if (
                "nargs" in option_properties.keys()
                and "default" in option_properties.keys()
            ):
                option_properties.pop("nargs")
            p = click.Argument(**option_properties)

        return p


class DocAttribute(ValueAttribute):
    def __init__(self, target_attr_name="doc", source_attr_name="_metadata_raw"):

        super(DocAttribute, self).__init__(
            target_attr_name=target_attr_name, source_attr_name=source_attr_name
        )

    def get_attribute(self, ting, attribute_name=None):

        result = ValueAttribute.get_attribute(self, ting, attribute_name=attribute_name)

        doc = Doc(result)
        return doc


class DictMergeAttribute(TingAttribute):
    def __init__(self, target_attr_name, source_attr_names):

        self.target_attr_name = target_attr_name
        self.attr_names = source_attr_names

    def requires(self):

        return self.attr_names

    def provides(self):

        return [self.target_attr_name]

    def get_attribute(self, ting, attribute_name=None):

        result = {}

        for attr_name in self.attr_names:

            d = getattr(ting, attr_name)
            dict_merge(result, d, copy_dct=False)

        return result


class WrapTingAttribute(TingAttribute):
    def __init__(self, wrapped_ting_attr_name, attr_names):

        self.wrapped_ting_attr_name = wrapped_ting_attr_name
        self.attr_names = list(attr_names)

    def provides(self):

        return self.attr_names

    def requires(self):

        return []

    def no_cache(self):

        return self.attr_names

    def get_attribute(self, ting, attribute_name=None):

        wrapped_ting = getattr(ting, self.wrapped_ting_attr_name)
        result = getattr(wrapped_ting, attribute_name)
        if callable(result):
            return result()
        else:
            return result
