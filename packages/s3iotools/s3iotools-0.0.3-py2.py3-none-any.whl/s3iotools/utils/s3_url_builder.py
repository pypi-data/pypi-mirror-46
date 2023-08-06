# -*- coding: utf-8 -*-

"""
There are two simple rules for s3 object key:

- should not start with slash "/"
- should not end with slash "/"

sometime we made mistake on this, this helper function ensure that common mistake
will not happened in building s3 URI.
"""

class S3UrlBuilder(object):
    """
    Build AWS S3 relative url.
    """
    URL_TPL = "https://s3.amazonaws.com/{bucket_name}/{key}"
    """
    A public url that targeting to a s3 object. 
    """

    S3_URI_TPL = "s3://{bucket_name}/{key}"
    """
    A url that targeting to a s3 object but will be consumed by 
    :meth:`pd.read_csv` function.
    """

    def ensure_not_startswith_slash(self, key):
        """
        S3 Key has to obey these rules:

        - cannot startswith ``/``.
        - if it is an directory object, it has to endswith ``/``.
        - if it is an file object, it can't endswith ``/``.
        """
        if key.startswith("/"):
            key = key[1:]
        return key

    def build_url_by_key(self, bucket_name, key):
        """
        Build the url to access the s3 object from browser.

        :param bucket_name: str, bucket name.
        :param key: str, posix styled path.
        :return: str.
        """
        key = self.ensure_not_startswith_slash(key)
        return self.URL_TPL.format(bucket_name=bucket_name, key=key)

    def build_s3_uri_by_key(self, bucket_name, key):
        """
        Build the universal resource identifier consumed by ``pandas.read_csv``.

        :param bucket_name: str, bucket name.
        :param key: str, posix styled path.
        :return: str.
        """
        key = self.ensure_not_startswith_slash(key)
        return self.S3_URI_TPL.format(bucket_name=bucket_name, key=key)

    def build_key_by_parts(self, *parts):
        l = list()
        for part in parts:
            for i in part.split("/"):
                if i.strip():
                    l.append(i)
        return "/".join(l)


s3_url_builder = S3UrlBuilder()
