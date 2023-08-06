# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
from attrs_mate import attr, AttrsClass
from pathlib_mate import PathCls as Path
from weakref import WeakValueDictionary


@attr.s
class Boto3Backed(AttrsClass):
    aws_profile = attr.ib()  # type: str

    _boto3_session_cache = WeakValueDictionary()
    _s3_resource_cache = WeakValueDictionary()
    _s3_client_cache = WeakValueDictionary()

    @property
    def boto3_session(self):
        if self.aws_profile not in self._boto3_session_cache:
            session = boto3.session.Session(profile_name=self.aws_profile)
            self._boto3_session_cache[self.aws_profile] = session
        return self._boto3_session_cache[self.aws_profile]

    @property
    def s3_resource(self):
        if self.aws_profile not in self._s3_resource_cache:
            s3_resource = self.boto3_session.resource("s3")
            self._s3_resource_cache[self.aws_profile] = s3_resource
        return self._s3_resource_cache[self.aws_profile]

    @property
    def s3_client(self):
        if self.aws_profile not in self._s3_client_cache:
            s3_client = self.boto3_session.client("s3")
            self._s3_client_cache[self.aws_profile] = s3_client
        return self._s3_client_cache[self.aws_profile]


@attr.s
class S3FileObject(Boto3Backed):
    bucket_name = attr.ib()  # type: str
    key = attr.ib()  # type: str

    aws_profile = attr.ib(default="default")  # type: str
    path = attr.ib(default=None)  # type: str

    _bucket = attr.ib(default=None)
    _object = attr.ib(default=None)

    @property
    def bucket(self):
        """
        access s3 Bucket instance.

        API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucket
        """
        if self._bucket is None:
            self._bucket = self.s3_resource.Bucket(self.bucket_name)
        return self._bucket

    @property
    def object(self):
        """
        access s3 Object instance.

        API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
        """
        if self._object is None:
            self._object = self.bucket.Object(self.key)
        return self._object

    @property
    def path_obj(self):
        """
        access the Path object.

        API: https://pathlib-mate.readthedocs.io/
        """
        return Path(self.path)

    def exists_on_s3(self):
        """
        Test if this s3 object exists on s3.

        :rtype: bool
        """
        try:
            _ = self.object.e_tag
            return True
        except ClientError:
            return False
        except Exception as e:
            raise e

    def exists_on_local(self):
        """
        Test if this local file object exists on local machine.

        :rtype: bool
        """
        return self.path_obj.exists()

    def copy_to_s3(self):
        """
        Copy this file from local to s3.
        """
        if not self.exists_on_local():
            raise IOError("No such file: '%s'" % self.path_obj)
        return self.object.upload_file(self.path_obj.abspath)

    def copy_to_local(self):
        """
        Copy this file from s3 to local.
        """
        return self.object.download_file(self.path_obj.abspath)
