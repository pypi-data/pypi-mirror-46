
.. image:: https://readthedocs.org/projects/s3iotools/badge/?version=latest
    :target: https://s3iotools.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/s3iotools-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/s3iotools-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/s3iotools-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/s3iotools-project

.. image:: https://img.shields.io/pypi/v/s3iotools.svg
    :target: https://pypi.python.org/pypi/s3iotools

.. image:: https://img.shields.io/pypi/l/s3iotools.svg
    :target: https://pypi.python.org/pypi/s3iotools

.. image:: https://img.shields.io/pypi/pyversions/s3iotools.svg
    :target: https://pypi.python.org/pypi/s3iotools

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/s3iotools-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://s3iotools.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://s3iotools.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://s3iotools.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/s3iotools-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/s3iotools-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/s3iotools-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/s3iotools#files


Welcome to ``s3iotools`` Documentation
==============================================================================


Usage
------------------------------------------------------------------------------

Copy local file to s3 and download file object from s3 to local is easy:

.. code-block:: python

    from s3iotools import S3FileObject

    s3obj = S3FileObject(bucket="my-bucket", key="hello.txt", path="hello.txt")

    # get started, now we don't have file either on local or on s3
    if s3obj.path_obj.exists():
        s3obj.path_obj.remove()
    assert s3obj.exists_on_local() is False
    assert s3obj.exists_on_s3() is False

    s3obj.path_obj.write_text("hello world", encoding="utf-8)
    assert s3obj.exists_on_local() is True

    s3obj.copy_to_s3()
    assert s3obj.exists_on_s3() is True

    s3obj.path_obj.remove()
    assert s3obj.exists_on_local() is False

    s3obj.copy_to_local()
    assert s3obj.exists_on_local() is True


You can manipulate s3 backed ``pandas.DataFrame`` easily:

.. code-block:: python

    import boto3
    import pandas as pd
    from s3iotools import S3Dataframe

    session = boto3.Session(profile_name="xxx")
    s3 = session.resource("s3")
    bucket_name = "my-bucket"
    s3df = S3Dataframe(s3_resource=s3, bucket_name=bucket_name)
    s3df.df = pd.DataFrame(...)

    s3df.to_csv(key="data.csv")
    s3df.to_csv(key="data.csv.gz", gzip_compressed=True)

    s3df_new = S3Dataframe(s3_resource=s3, bucket_name=bucket_name, key="data.csv")
    s3df_new.read_csv()
    s3df_new.df # access data

    s3df_new = S3Dataframe(s3_resource=s3, bucket_name=bucket_name, key="data.csv.gz")
    s3df_new.read_csv(gzip_compressed=True)
    s3df_new.df # access data


json IO is similar.

.. code-block:: python

    s3df = S3Dataframe(s3_resource=s3, bucket_name=bucket_name)
    s3df.df = pd.DataFrame(...)
    s3df.to_json(key="data.json.gz", gzip_compressed=True)
    s3df_new = S3Dataframe(s3_resource=s3, bucket_name=bucket_name, key="data.json.gz")
    s3df_new.read_json(gzip_compressed=True)
    s3df_new.df # access data


parquet is a columnar storage format, which is very efficient for OLAP query. You can just put data on S3, then use AWS Athena to query parquet files. parquet IO in s3iotools is easy:

.. code-block:: python

    s3df = S3Dataframe(s3_resource=s3, bucket_name=bucket_name)
    s3df.df = pd.DataFrame(...)
    s3df.to_parquet(key="data.parquet", compression="gzip")
    s3df_new = S3Dataframe(s3_resource=s3, bucket_name=bucket_name, key="data.parquet")
    s3df_new.read_parquet()
    s3df_new.df # access data


s3iotools doesn't automatically install ``pyarrow``, you can install it with ``pip install pyarrow``.


.. _install:

Install
------------------------------------------------------------------------------

``s3iotools`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install s3iotools

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade s3iotools
