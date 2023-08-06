# -*- coding: utf-8 -*-


"""
filter :class:`s3.Object` or :class:`s3.ObjectSummary`.

s3 object has following attributes can be used for filtering:

- Object.bucket_name
- Object.key
- Object.e_tag
- Object.last_modified
- Object.size

reference: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#objectsummary
"""

from botocore.exceptions import ClientError


def get_obj_size(s3_obj):
    try:  # s3.ObjectSummary
        return s3_obj.size
    except:  # s3.Object
        return s3_obj.content_length


class FiltersConstructor(object):
    """
    Construct a ``s3.Object`` filter function.

    Note:

    为什么要有 is_classmethod, is_staticmethod, is_regularmethod 这些参数?

    由于 ``select_from(objects, filters)`` 中的 filters 本质上是一个只接受一个
    s3 Object 参数的函数. 而这个函数有可能会被用在 classmethod, staticmethod,
    和普通的类 method 中. 所以如果我们要将这个 filters 函数赋值给一个类的话, 就像我们在
    :class:`Filters` 中做的一样, 就有用了.
    """

    @staticmethod
    def validate_method_type_args(is_classmethod, is_staticmethod, is_regularmethod):
        if sum([is_classmethod, is_staticmethod, is_regularmethod]) > 1:
            raise ValueError

    def by_extension(self,
                     ext,
                     case_sensitive=False,
                     is_classmethod=False,
                     is_staticmethod=False,
                     is_regularmethod=False):
        self.validate_method_type_args(
            is_classmethod, is_staticmethod, is_regularmethod)

        if case_sensitive:
            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return s3_obj.key.endswith(ext)
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return s3_obj.key.endswith(ext)
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return s3_obj.key.endswith(ext)
            else:
                def filters(s3_obj):
                    return s3_obj.key.endswith(ext)
        else:
            ext = ext.lower()

            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return s3_obj.key.lower().endswith(ext)
            else:
                def filters(s3_obj):
                    return s3_obj.key.lower().endswith(ext)
        return filters

    def by_basename(self,
                    basename,
                    case_sensitive=False,
                    is_classmethod=False,
                    is_staticmethod=False,
                    is_regularmethod=False):
        self.validate_method_type_args(
            is_classmethod, is_staticmethod, is_regularmethod)
        if case_sensitive:
            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
            else:
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1]
        else:
            basename = basename.lower()

            if is_classmethod:
                @classmethod
                def filters(cls, s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            elif is_staticmethod:
                @staticmethod
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            elif is_regularmethod:
                def filters(self, s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
            else:
                def filters(s3_obj):
                    return basename in s3_obj.key.split("/")[-1].lower()
        return filters

    def by_last_modified_after(self, a_datetime):
        def filters(s3_obj):
            return s3_obj.last_modified >= a_datetime

        return filters

    def by_last_modified_before(self, a_datetime):
        def filters(s3_obj):
            return s3_obj.last_modified <= a_datetime

        return filters

    def by_last_modified_between(self, after, before):
        def filters(s3_obj):
            return after <= s3_obj.last_modified <= before

        return filters

    def by_md5(self, md5):
        def filters(s3_obj):
            return s3_obj.e_tag == md5

        return filters

    def by_size(self, min_size_in_bytes=-1, max_size_in_bytes=999999999999):
        def filters(s3_obj):
            size = get_obj_size(s3_obj)
            return min_size_in_bytes <= size <= max_size_in_bytes

        return filters


filter_constructor = FiltersConstructor()


class _Filters(object):
    """
    Pre-defined ``s3.Object`` filters.
    """

    def exists(self, obj):
        """
        Test if this object exists.
        """
        try:
            obj.e_tag
            return True
        except ClientError:
            return False
        except:
            return False

    def not_exists(self, obj):
        """
        Test if this object exists.
        """
        return not self.exists(obj)

    csv = filter_constructor.by_extension(".csv", case_sensitive=False)
    """Test if it is a ``.csv`` file"""

    json = filter_constructor.by_extension(".json", case_sensitive=False)
    """Test if it is a ``.json`` file"""

    gzip = filter_constructor.by_extension(".gz", case_sensitive=False)
    """Test if it is a ``.gz`` file"""

    log = filter_constructor.by_extension(".log", case_sensitive=False)
    """Test if it is a ``.log`` file"""


Filters = _Filters()


def select_from(objects, filters):
    """
    Select objects from s3 objects candidate iterable by criterion defined
    in filters.

    :type objects: list
    :type filters: func

    :rtype: iterable
    
    Usage:
    
    .. code-block:: python
    
        >>> from s3iotools import select_from, Filters, filter_constructor
        >>> objects = boto3.resource("s3").Bucket("my-bucket").objects.filter(Prefix="/data")
        >>> for obj in select_from(objects, Filters.csv): # select .csv file
        ...     # do someting
        >>> from datetime import datetime
        >>> for obj in select_from(objects, filter_constructor.by_last_modified_after(datetime(2019, 1, 1))) # select file created after 2019-01-01
        ...     # do someting
    """
    for s3_obj in objects:
        if filters(s3_obj):
            yield s3_obj
