# -*- coding: utf-8 -*-

from cerberus import SchemaError, Validator
from frutils import readable_yaml
from passlib.handlers.sha2_crypt import sha512_crypt

from frutils.exceptions import FrklException

TING_DEFAULT_ARG_SCHEMA = {"required": True, "empty": False}


class TingValidator(Validator):
    def __init__(self, *args, **kwargs):
        try:
            super(TingValidator, self).__init__(*args, **kwargs)
        except (SchemaError) as se:
            a = se.args

            raise FrklException(
                msg="Can't determine schema validity.",
                reason="Invalid cerebus schema provided:\n\n+{}".format(
                    readable_yaml(a)
                ),
                solution="Please check the cerebus documentation for more information.",
                references={
                    "Cerebus documentation": "http://docs.python-cerberus.org/en/stable/validation-rules.html"
                },
            )

    def _normalize_coerce_sha512_crypt(self, value):

        if not value:
            return None

        hashed_pass = sha512_crypt.using(rounds=5000).hash(value)
        return hashed_pass

    # def _validate_matches_ting_attribute_class_name(self, is_ting_attribute, field, value):
    #
    #     match = None
    #     for n in TingAttribute.__subclasses__():
    #         if value.lower() == n.lower() or "{}attribute".format(value).lower() == n.lower():
    #             match = n
    #             break
    #
    #     if is_ting_attribute and match is None:
    #         self._error(field, "does not match any available TingAttribute class name")
    #     elif not is_ting_attribute and match is not None:
    #         self._error(field, "does match an available TingAttribute class name: {}".format)

    # def _normalize_coerce_ting_attribute_class_name(self, value):
    #     for n in TingAttribute.__subclasses__():
    #         n = n.__name__
    #         if value.lower() == n.lower() or "{}attribute".format(value).lower() == n.lower():
    #             return n
