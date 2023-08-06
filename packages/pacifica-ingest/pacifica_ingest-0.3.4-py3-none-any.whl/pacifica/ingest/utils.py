#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Testable utilities for ingest."""
from __future__ import print_function
import json
import requests
import six
from .config import get_config

# pylint: disable=invalid-name
int_type = six.integer_types[-1]
# pylint: enable=invalid-name


def parse_size(size):
    """Parse size string to integer."""
    units = {
        'B': 1, 'KB': 10**3, 'MB': 10**6, 'GB': 10**9, 'TB': 10**12,
        'b': 1, 'Kb': 1024, 'Mb': 1024**2, 'Gb': 1024**3, 'Tb': 1024**4
    }
    number, unit = [string.strip() for string in size.split()]
    return int_type(float(number)*units[unit])


def create_state_response(record):
    """Create the state response body from a record."""
    return {
        'job_id': record.job_id,
        'state': record.state,
        'task': record.task,
        'task_percent': str(record.task_percent),
        'complete': bool(record.complete),
        'updated': str(record.updated),
        'created': str(record.created),
        'exception': str(record.exception)
    }


def get_unique_id(id_range, mode):
    """Return a unique job id from the id server."""
    uniqueid_url = get_config().get('uniqueid', 'url')
    url = '{0}/getid?range={1}&mode={2}'.format(
        uniqueid_url, id_range, mode)

    req = requests.get(url)
    body = req.text
    info = json.loads(body)
    unique_id = info['startIndex']

    return unique_id
