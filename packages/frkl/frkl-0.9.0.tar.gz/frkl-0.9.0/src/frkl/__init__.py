# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

# flake8: noqa

from .defaults import DEFAULT_FRKL_JINJA_ENVIRONMENT
from .frkl import (
    Frkl,
    load_object_from_url_or_path,
    load_string_from_url_or_path,
    load_templated_string_from_url_chain,
)
from .frklist import Frklist, FrklistContext
from .helpers import content_from_url, dict_from_url, download_cached_file, get_full_url
from .processors import (
    EnsurePythonObjectProcessor,
    EnsureUrlProcessor,
    FrklProcessor,
    LoadMoreConfigsProcessor,
    UrlAbbrevProcessor,
)
from .utils import VarsType

__author__ = """Markus Binsteiner"""
__email__ = "makkus@posteo.de"

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
