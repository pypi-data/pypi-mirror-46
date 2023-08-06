"""
This module handles dcli default options logic
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2019 VMware, Inc.  All rights reserved.'
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

from vmware.vapi.client.dcli.internal_commands.options import Options

OPTION_NAME = 'DCLI_COLORED_OUTPUT'


class Output(object):
    """
    Handles dcli output styling operations
    """
    def __init__(self, dcli_context=None):
        self.dcli_context = dcli_context
        self.default_options = Options(self.dcli_context)

    def enable(self):
        """
        Enables output colorization
        """
        self.default_options.set(OPTION_NAME,
                                 True,
                                 module='dcli',
                                 is_global_option=True)

    def disable(self):
        """
        Disable output colorization
        """
        self.default_options.set(OPTION_NAME,
                                 False,
                                 module='dcli',
                                 is_global_option=True)
