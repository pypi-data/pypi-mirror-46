"""
This module handles dcli styling options
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2019 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import logging
from vmware.vapi.client.dcli.internal_commands.options import Options

logger = logging.getLogger(__name__)

OPTION_NAME = 'DCLI_COLORS_ENABLED'


class Color(object):
    def __init__(self, dcli_context=None):
        self.dcli_context = dcli_context
        self.default_options = Options(self.dcli_context)

    def enable(self):
        """
        Enables dcli colorization in both input and output
        """
        self.default_options.set(OPTION_NAME,
                                 True,
                                 module='dcli',
                                 is_global_option=True)

    def disable(self):
        """
        Disables dcli colorization in both input and output
        """
        self.default_options.set(OPTION_NAME,
                                 False,
                                 module='dcli',
                                 is_global_option=True)
