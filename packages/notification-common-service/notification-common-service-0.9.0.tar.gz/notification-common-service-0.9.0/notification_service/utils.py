# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import collections


def from_ARN_to_region_name(arn):
    return arn.split(':')[3]


def update_sub_dict(d, u):
    """Update a dict from another dict, and include their sub dict."""
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            d[k] = update_sub_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d
