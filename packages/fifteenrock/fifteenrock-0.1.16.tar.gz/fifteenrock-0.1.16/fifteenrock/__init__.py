# -*- coding: utf-8 -*-

"""Top-level package for fifteenrock."""

__author__ = """Rajiv Abraham"""
__email__ = 'rajiv.abraham@15rock.com'
__version__ = '0.1.0'

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from .core import get_database_client, deploy
from .fr_notebook import deploy_notebook
