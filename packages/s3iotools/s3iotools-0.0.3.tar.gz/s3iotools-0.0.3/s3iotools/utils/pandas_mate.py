# -*- coding: utf-8 -*-


def itertuple(df):
    """
    High performance tuple style iterator.

    :param df: ``pandas.DataFrame`` instance.
    """
    return zip(*(l for col, l in df.iteritems()))
