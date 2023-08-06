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

from vmware.vapi.client.dcli.internal_commands.options import Options


class Style(object):
    """
    Provides commands for handling styling optons in dcli
    """
    def __init__(self, dcli_context):
        self.dcli_context = dcli_context
        self.default_options = Options(self.dcli_context)

    def list(self):
        """
        Gets a list of all set styling options

        :rtype: :class:`dict`
        :return: returns dict of styling options set for each module
        """
        return {'DCLI_COLORS_ENABLED': self.default_options.try_get('DCLI_COLORS_ENABLED', is_global_option=True),
                'DCLI_COLORED_INPUT': self.default_options.try_get('DCLI_COLORED_INPUT', is_global_option=True),
                'DCLI_COLORED_OUTPUT': self.default_options.try_get('DCLI_COLORED_OUTPUT', is_global_option=True),
                'DCLI_COLOR_THEME': self.default_options.try_get('DCLI_COLOR_THEME', is_global_option=True)}
