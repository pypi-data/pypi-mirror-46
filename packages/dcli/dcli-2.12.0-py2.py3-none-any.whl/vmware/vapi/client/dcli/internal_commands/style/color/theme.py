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

OPTION_NAME = 'DCLI_COLOR_THEME'


class Theme(object):
    """
    Handles dcli theme operations
    """
    def __init__(self, dcli_context=None):
        self.dcli_context = dcli_context
        self.default_options = Options(self.dcli_context)

    def get(self):  # pylint: disable=W0611,R0201
        """
        Get color theme set
        """
        return self.default_options.try_get(OPTION_NAME,
                                            module='dcli',
                                            is_global_option=True)

    def set(self, theme):
        """
        Sets dcli color theme
        """
        self.default_options.set(OPTION_NAME,
                                 theme.lower(),
                                 module='dcli',
                                 is_global_option=True)
