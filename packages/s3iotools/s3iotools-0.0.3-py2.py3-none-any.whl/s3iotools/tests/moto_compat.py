# -*- coding: utf-8 -*-

"""
moto3 requires a ~/.aws/credentials file exists, so we create a fake one dynamically.
"""

import os

src = os.path.join(os.path.dirname(__file__), "credentials")
dst = os.path.join(os.path.expanduser("~"), ".aws", "credentials")
dst_dir = os.path.dirname(dst)

if not os.path.exists(dst_dir):
    os.mkdir(dst_dir)
if not os.path.exists(dst):
    with open(src, "rb") as f1:
        with open(dst, "wb") as f2:
            s = f1.read().decode("utf-8").format(field1="aws_access_key_id", field2="aws_secret_access_key")
            f2.write(s.encode("utf-8"))
