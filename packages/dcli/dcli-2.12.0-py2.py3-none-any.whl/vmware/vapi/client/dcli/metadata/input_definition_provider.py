"""
This module provides provider for retrieveing command input definition
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2017-2019 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import logging

from vmware.vapi.data.definition import (
    DynamicStructDefinition, IntegerDefinition, VoidDefinition,
    BooleanDefinition, StringDefinition, SecretDefinition, StructDefinition,
    StructRefDefinition, OptionalDefinition, ListDefinition,
    OpaqueDefinition, DoubleDefinition,
    BlobDefinition)
from vmware.vapi.client.dcli.util import ServerTypes
from vmware.vapi.client.dcli.exceptions import handle_error
from com.vmware.vapi.metadata.metamodel_client import Enumeration
from com.vmware.vapi.std.errors_client import NotFound

logger = logging.getLogger(__name__)


class InputDefinitionProvider(object):
    """
    Helper class for building method definitions from metamodel information
    """
    builtin_type_map = {
        'binary': BlobDefinition,
        'boolean': BooleanDefinition,
        'date_time': StringDefinition,
        'double': DoubleDefinition,
        'id': StringDefinition,
        'long': IntegerDefinition,
        'opaque': OpaqueDefinition,
        'secret': SecretDefinition,
        'string': StringDefinition,
        'dynamic_structure': DynamicStructDefinition,
        'uri': StringDefinition,
        'void': VoidDefinition,
    }

    def __init__(self, metadata_provider):
        self.metadata_provider = metadata_provider

    def get_method_input_definition(self, service_name, operation_name):
        """
        Returns method input definition for specified operation

        :param service_name: name of the service the operation resides in
        :type service_name: :class:`str`
        :param operation_name: name of the operation, part of the service
        specified in the constructor
        :type operation_name: :class:`str`

        :return: method definition of the specified operation
        :rtype: :class:`vmware.vapi.core.MethodDefinition`
        """
        try:
            op_info = self.metadata_provider.get_operation_info(service_name, operation_name)
        except KeyError:
            raise NotFound()  # pylint: disable=W0710

        return self._get_method_input_def(op_info)

    def _get_method_input_def(self, op_info):
        """
        Returns method input definition object

        :param op_info: metamodel operation info object
        :type op_info: :class:`com.vmware.vapi.metadata.metamodel_client
        .OperationInfo`

        :return: method definition of the specified operation
        :rtype: :class:`vmware.vapi.core.MethodDefinition`
        """
        param_list = []
        for field_info in op_info.params:
            param_list.append((field_info.name, self._get_type_info(
                field_info.type)))
        return StructDefinition('operation-input', param_list)

    def _get_structure_info(self, struct_name, struct_info, visited_structs):
        """
        Returns structure definition object

        :param struct_name: full structure name
        :type struct_name: :class:`str`
        :param struct_info: metamodel structure info object
        :type struct_info: :class:`com.vmware.vapi.metadata.metamodel_client
        .StructureInfo`
        :param visited_structs: list of already visited structures.
        Needed to handle recursive references.
        :type visited_structs: :class:`list` of :class:`str`

        :return: Structure definition for the specified structure
        :rtype: :class:`vmware.vapi.data.definition.StructDefinition`
        """
        visited_structs.append(struct_name)
        fields = []
        for field_info in struct_info.fields:
            field_name = None
            if hasattr(self.metadata_provider, 'server_type') \
                    and self.metadata_provider.server_type in (ServerTypes.VMC,
                                                               ServerTypes.NSX):
                try:
                    field_name = field_info.serialization_name
                except Exception:
                    raise Exception('Unable to get serialization name for %s '
                                    'field' % field_info.name)
            else:
                field_name = field_info.name

            if field_name is None:
                raise ValueError("Couldn't find the serialization name for "
                                 'field %s' % field_info.name)

            fields.append((field_name, self._get_type_info(
                field_info.type, visited_structs)))
        visited_structs.pop()
        return StructDefinition(name=struct_name, fields=fields)

    def _get_type_info(self, type_info, visited_structs=None):
        """
        Returns type definition object

        :param type_info: metamodel type info object
        :type type_info: :class:`com.vmware.vapi.metadata.metamodel_client.Type`
        :param visited_structs: list of already visited structures.
        Needed to handle recursive references.
        :type visited_structs: :class:`list` of :class:`str`

        :return: Type definition of the specified type
        :rtype: :class:`vmware.vapi.data.definition.DataDefinition`
        """
        if visited_structs is None:
            visited_structs = []
        if type_info.category == 'BUILTIN':
            return InputDefinitionProvider.builtin_type_map[
                type_info.builtin_type]()
        elif type_info.category == 'GENERIC':
            return self._get_generic_type_info(
                type_info.generic_instantiation, visited_structs)
        # Userdefined type
        return self._get_user_defined_type_info(type_info, visited_structs)

    def _get_generic_type_info(self, generic_instantiation, visited_structs):
        """
        Returns generic definition object

        :param generic_instantiation: metamodel generic info object
        :type generic_instantiation:
        :class:`com.vmware.vapi.metadata.metamodel_client.GenericInstantiation`
        :param visited_structs: list of already visited structures.
        Needed to handle recursive references.
        :type visited_structs: :class:`list` of :class:`str`

        :return: input definition for the specified generic
        :rtype: :class:`vmware.vapi.data.definition.DataDefinition`
        """
        if generic_instantiation.generic_type in ['list', 'set']:
            return ListDefinition(self._get_type_info(
                generic_instantiation.element_type, visited_structs))
        elif generic_instantiation.generic_type == 'optional':
            return OptionalDefinition(self._get_type_info(
                generic_instantiation.element_type, visited_structs))

        # Map type
        key_def = self._get_type_info(generic_instantiation.map_key_type,
                                      visited_structs)
        value_def = self._get_type_info(
            generic_instantiation.map_value_type, visited_structs)
        fields = [('key', key_def),
                  ('value', value_def)]
        # generate correct name for the struct

        return ListDefinition(StructDefinition(name='map_entry',
                                               fields=fields))

    def _get_user_defined_type_info(self, type_info, visited_structs):
        """
        Returns user definition object

        :param type_info: metamodel type info object
        :type type_info: :class:`com.vmware.vapi.metadata.metamodel_client.Type`
        :param visited_structs: list of already visited structures.
        Needed to handle recursive references.
        :type visited_structs: :class:`list` of :class:`str`

        :return: input definition for the specified user defined type
        :rtype: :class:`vmware.vapi.data.definition.DataDefinition`
        """
        if type_info.user_defined_type.resource_type == \
                Enumeration.RESOURCE_TYPE:
            return StringDefinition()

        # Structure reference
        struct_full_name = type_info.user_defined_type.resource_id
        if struct_full_name in visited_structs:
            return StructRefDefinition(struct_full_name)

        try:
            struct_info = \
                self.metadata_provider.get_structure_info(struct_full_name)
        except NotFound as e:
            handle_error("Input definition error: Structure info for "
                         "'%s' was not found" % struct_full_name, exception=e)
            raise e  # pylint: disable=W0710
        return self._get_structure_info(struct_full_name,
                                        struct_info, visited_structs)
