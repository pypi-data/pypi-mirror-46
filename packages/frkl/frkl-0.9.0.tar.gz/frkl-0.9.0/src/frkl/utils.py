# -*- coding: utf-8 -*-
import json
import logging
from collections import Mapping

import click
from frutils import StringYAML, dict_merge, is_url_or_abbrev
from frutils.defaults import *  # noqa: F403
from ruamel.yaml.comments import CommentedSeq
from six import string_types

from .callbacks import (
    EnsurePythonObjectProcessor,
    EnsureUrlProcessor,
    SetResultCallback,
)
from .frkl import Frkl
from .processors import ParentPathProcessor, UrlAbbrevProcessor

log = logging.getLogger("frkl")

yaml = StringYAML()


def expand_string_to_git_details(value, default_abbrevs):

    branch = None
    opt_split_string = "::"
    if opt_split_string in value:
        tokens = value.split(opt_split_string)
        opt = tokens[1:-1]
        if not opt:
            raise Exception(
                "Not a valid url, needs at least 2 split strings ('{}')".format(
                    opt_split_string
                )
            )
        if len(opt) != 1:
            raise Exception("Not a valid url, can only have 1 branch: {}".format(value))
        branch = opt[0]

    result = expand_string_to_git_repo(value, default_abbrevs)
    result = {"url": result}

    if branch:
        result["branch"] = branch

    return result


def expand_string_to_git_repo(value, default_abbrevs):
    if isinstance(value, string_types):
        is_string = True
    elif isinstance(value, (list, tuple)):
        is_string = False
    else:
        raise Exception(
            "Not a supported type (only string or list are accepted): {}".format(value)
        )

    try:
        init_params = {"abbrevs": default_abbrevs, "add_default_abbrevs": False}
        frkl_obj = Frkl(value, [UrlAbbrevProcessor(**init_params)])
        result = frkl_obj.process()
        if is_string:
            return result[0]
        else:
            return result
    except (Exception) as e:
        raise Exception("'{}' is not a valid repo url: {}".format(value, e))


def get_url_parents(urls, abbrevs=False, return_list=False):
    """Helper methods to calculate the parents of the provided urls.

    Args:
        urls (list): the list of urls
        abbrevs (bool, dict): if False, urls won't be expanded if they are abbreviated, otherwise if a abbrev dict is provided, they will be
        return_list (bool): whether to return the result as set (False) or list (True)
    """

    if abbrevs is False or abbrevs is None:
        chain = [ParentPathProcessor()]
    else:
        if abbrevs is True:
            abbrevs = DEFAULT_URL_ABBREVIATIONS_FILE
        chain = [
            UrlAbbrevProcessor(
                init_params={"abbrevs": abbrevs, "add_default_abbrevs": False}
            ),
            ParentPathProcessor(),
        ]
    callback = SetResultCallback(init_params={"return_list": return_list})

    frkl_obj = Frkl(urls, chain)
    result = frkl_obj.process(callback)

    return result


class VarsFileType(click.ParamType):

    name = "vars_file_type"

    def convert(self, value, param, ctx):

        chain = [
            UrlAbbrevProcessor(),
            EnsureUrlProcessor(),
            EnsurePythonObjectProcessor(),
            # LoadMoreConfigsProcessor(),
        ]

        try:
            if not isinstance(value, (list, tuple, CommentedSeq)):
                value = [value]

            frkl_obj = Frkl(value, chain)
            result = frkl_obj.process()

            if isinstance(result[0], (list, tuple)):

                result_dict = {}
                for item in result[0]:
                    dict_merge(result_dict, item, copy_dct=False)

                return result_dict
            else:
                return result[0]

        except (Exception) as e:
            self.fail("Can't read vars '{}': {}".format(value, str(e)))


class VarsType(click.ParamType):

    name = "vars_type"

    def convert(self, value, param, ctx):

        path = os.path.realpath(os.path.expanduser(value))
        value_type = "string"

        if os.path.exists(path):
            value_type = "local"
        elif is_url_or_abbrev(value):
            value_type = "remote"

        if value_type in ["remote", "local"]:
            chain = [
                UrlAbbrevProcessor(),
                EnsureUrlProcessor(),
                EnsurePythonObjectProcessor(),
                # LoadMoreConfigsProcessor(),
            ]

            try:
                if not isinstance(value, (list, tuple, CommentedSeq)):
                    value = [value]

                frkl_obj = Frkl(value, chain)
                result = frkl_obj.process()

                if isinstance(result[0], (list, tuple)):

                    result_dict = {}
                    for item in result[0]:
                        dict_merge(result_dict, item, copy_dct=False)

                    return result_dict
                else:
                    return result[0]

            except (Exception) as e:
                self.fail("Can't read vars url '{}': {}".format(value, str(e)))

        else:
            # try yaml
            log.debug("Trying yaml for value: '{}'".format(value))

            try:
                result = json.loads(value)
                if not isinstance(result, Mapping):
                    self.fail("Can't parse variable string as json: {}".format(result))
            except (Exception):
                try:
                    result = yaml.load(value)
                    if not isinstance(result, Mapping):
                        self.fail(
                            "Can't parse variable string as yaml: {}".format(result)
                        )
                except (Exception):
                    self.fail("Can't read vars string: {}".format(value))

            return result
