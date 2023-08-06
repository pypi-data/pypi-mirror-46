# -*- coding: utf-8 -*-

"""
s3 IO tools.
"""

import attr
import pandas as pd
from six import string_types, StringIO, BytesIO, PY3

from ..compat import gzip_compress, gzip_decompress


@attr.s
class S3Dataframe(object):
    """
    S3 object backed pandas DataFrame.
    """
    s3_resource = attr.ib(default=None)
    bucket_name = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(string_types)
        ),
        default=None,
    )
    _bucket = attr.ib(default=None)
    key = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(string_types)
        ),
        default=None,
    )
    _object = attr.ib(default=None)
    df = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(pd.DataFrame)
        ),
        default=None,
    )

    @property
    def bucket(self):
        """
        access the ``s3.Bucket`` instance.

        Ref: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#bucket
        """
        if self._bucket is None:
            self._bucket = self.s3_resource.Bucket(self.bucket_name)
        return self._bucket

    @property
    def object(self):
        """
        access the ``s3.Object`` instance.

        Ref: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#object
        """
        if self._object is None:
            self._object = self.bucket.Object(self.key)
        return self._object

    def prepare_args(self, bucket, key, kwargs, default_kwargs):
        if bucket is None:
            bucket = self.bucket
        if key is None:
            key = self.key
        extra_kwargs = default_kwargs.copy()
        extra_kwargs.update(kwargs)
        return bucket, key, extra_kwargs

    to_csv_kwargs_default = {
        "encoding": "utf-8",
        "index": False,
    }

    def to_csv(self, bucket=None, key=None, gzip_compressed=False, **to_csv_kwargs):
        """
        Save a dataframe to a s3 object in csv format.
        It will overwrite existing one.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param gzip_compressed: bool
        :param to_csv_kwargs: key word arguments for :meth:`pandas.DataFrame.to_csv`
        :return: s3.Bucket.put_object() response
        """
        bucket, key, kwargs = self.prepare_args(
            bucket, key, to_csv_kwargs, self.to_csv_kwargs_default)

        body = self.df.to_csv(**kwargs)
        if PY3:
            body = body.encode("utf-8")
        if gzip_compressed is True:
            body = gzip_compress(body)

        response = bucket.put_object(Body=body, Key=key)
        return response

    read_csv_kwargs_default = {
        "encoding": "utf-8"
    }

    def read_csv(self, bucket=None, key=None, gzip_compressed=False, **read_csv_kwargs):
        """
        Read dataframe data from a s3 object in csv format.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param gzip_compressed: bool
        :param read_csv_kwargs: key word arguments for :meth:`pandas.read_csv`
        :return: s3.Object.get() response
        """
        bucket, key, kwargs = self.prepare_args(
            bucket, key, read_csv_kwargs, self.read_csv_kwargs_default)

        obj = bucket.Object(key)
        response = obj.get()
        body = response["Body"].read()
        if gzip_compressed:
            body = gzip_decompress(body)

        self.df = pd.read_csv(StringIO(body.decode("utf-8")), **kwargs)

        return response

    to_json_kwargs_default = {
        "force_ascii": False,
    }

    def to_json(self, bucket=None, key=None, gzip_compressed=False, **to_json_kwargs):
        """
        Save a dataframe to a s3 object in csv format.
        It will overwrite existing one.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param gzip_compressed: bool
        :param to_json_kwargs: key word arguments for :meth:`pandas.DataFrame.to_json`
        :return: s3.Bucket.put_object() response
        """
        bucket, key, kwargs = self.prepare_args(
            bucket, key, to_json_kwargs, self.to_json_kwargs_default)

        body = self.df.to_json(**kwargs)
        if PY3:
            body = body.encode("utf-8")
        if gzip_compressed is True:
            body = gzip_compress(body)

        response = bucket.put_object(Body=body, Key=key)
        return response

    read_json_kwargs_default = {
        "encoding": "utf-8"
    }

    def read_json(self, bucket=None, key=None, gzip_compressed=False, **read_json_kwargs):
        """
        Read dataframe data from a s3 object in json format.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param gzip_compressed: bool
        :param read_json_kwargs: key word arguments for :meth:`pandas.read_json`
        :return: s3.Object.get() response
        """
        bucket, key, kwargs = self.prepare_args(
            bucket, key, read_json_kwargs, self.read_json_kwargs_default)

        obj = bucket.Object(key)
        response = obj.get()
        body = response["Body"].read()
        if gzip_compressed:
            body = gzip_decompress(body)

        self.df = pd.read_json(StringIO(body.decode("utf-8")), **kwargs)

        return response

    write_table_kwargs_default = {

    }

    class ParquestCompression:
        gzip = "gzip"
        snappy = "snappy"
        brotli = "brotli"
        lz4 = "lz4"
        zstd = "zstd"
        none = None

    def to_parquet(self, bucket=None, key=None, compression=None, **write_table_kwargs):
        """
        Save a dataframe to a s3 object in parquet format.
        It will overwrite existing one.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param gzip_compressed: bool
        :param to_json_kwargs: key word arguments for :meth:`pyarrow.parquet.write_table_kwargs`
        :return: s3.Bucket.put_object() response
        """
        import pyarrow
        from pyarrow import parquet

        bucket, key, kwargs = self.prepare_args(
            bucket, key, write_table_kwargs, self.write_table_kwargs_default)

        buffer = BytesIO()
        parquet.write_table(
            pyarrow.Table.from_pandas(self.df),
            buffer,
            compression=compression,
            **write_table_kwargs
        )
        body = buffer.getvalue()
        response = bucket.put_object(Body=body, Key=key)
        return response

    read_table_kwargs_default = {}

    def read_parquet(self, bucket=None, key=None, **read_table_kwargs):
        """
        Read dataframe data from a s3 object in parquet format.

        :param bucket: :class:`s3.Bucket`, optional if self.bucket_name is defined
        :param key: str, optional if self.key is defined
        :param read_table_kwargs: key word arguments for :meth:`pyarrow.parquet.read_table`
        :return: s3.Object.get() response
        """
        from pyarrow import parquet

        bucket, key, kwargs = self.prepare_args(
            bucket, key, read_table_kwargs, self.read_table_kwargs_default)

        obj = bucket.Object(key)
        response = obj.get()

        # boto3 StreamingBody has not implemented closed attribute
        buffer = BytesIO()
        buffer.write(response["Body"].read())
        self.df = parquet.read_table(buffer, **read_table_kwargs).to_pandas()
        return response
