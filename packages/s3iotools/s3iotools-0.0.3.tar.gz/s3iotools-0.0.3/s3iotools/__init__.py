# -*- coding: utf-8 -*-

from ._version import __version__

__short_description__ = "Make S3 file object read/write easier, support raw file, csv, parquet, pandas.DataFrame."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .io.file_object import S3FileObject
except ImportError: # pragma: no cover
    pass

try:
    from .io.dataframe import S3Dataframe
except ImportError: # pragma: no cover
    pass

try:
    from .utils.s3_obj_filter import select_from, Filters, filter_constructor
except ImportError: # pragma: no cover
    pass

try:
    from .utils.s3_url_builder import s3_url_builder
except ImportError: # pragma: no cover
    pass
