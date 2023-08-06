"""
This module handles abstract metadata related classes
"""

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2017-2019 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import abc

import six

from vmware.vapi.client.dcli.metadata.metadata_info import (
    CommandIdentityInfo, CommandInfo, OptionInfo,
    OutputInfo, OutputFieldInfo)


class AbstractMetadataProvider(object):  # pylint: disable=E0012
    """
    Abstract class used to set contract for providers which handle metadata
    information
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_commands(self, namespace_path=None):
        """
        Gets list of commands for the specified namespace_path

        :param namespace_path: namespace path to retrieve commands from
        :type namespace_path: :class:`str`
        :return: list of commands
        :rtype: :class:`list` of
            :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandIdentityInfo`
        """
        return

    @abc.abstractmethod
    def get_command_info(self, namespace_path, command_name):
        """
        Gets command metadata info by specified command name and namespace path

        :param namespace_path: namespace path to the command
        :type namespace_path: :class:`str`
        :param command_name: command name
        :type command_name: :class:`str`
        :return: coomand metdata info object
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandInfo`
        """
        return

    @abc.abstractmethod
    def get_namespaces(self):
        """
        Gets the list of namespaces

        :return: list of namespace identity objects
        :rtype: :class:`list` of type
            :class:`vmware.vapi.client.dcli.metadata.metadata_info.NamespaceIdentityInfo`
        """
        return

    @abc.abstractmethod
    def get_namespace_info(self, namespace_path, namespace_name):
        """
        Gets namesapce metadata info for specified namespace path and name

        :param namespace_path: namespace path
        :type namespace_path: :class:`str`
        :param namespace_name: namespace name
        :type namespace_name: :class:`str`
        :return: Namespace info object found by given path and name
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.NamespaceInfo`
        """
        return

    @abc.abstractmethod
    def get_command_input_definition(self, service_path, operation_name):
        """
        Gets vapi input definition for a command specified by path and name

        :param service_path: service path where the operation resides
        :type service_path: :class:`str`
        :param operation_name: operation name
        :type operation_name: :class:`str`
        :return: Input definition object for an operation specified by
        service path and operation name
        :rtype: :class:`vmware.vapi.data.definition.StructDefinition`
        """
        return

    @abc.abstractmethod
    def get_service_info(self, service_path):
        """
        Gets metadata for service specified by service path

        :param service_path: service path
        :type service_path: :class:`str`
        :return: Service info object found by specified service path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.ServiceInfo
        """
        return

    @abc.abstractmethod
    def get_structure_info(self, structure_path):
        """
        Gets metadata for structure specified by structure path

        :param structure_path: structure path
        :type structure_path: :class:`str`
        :return: Strucutre info object found by specified structure path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.StructureInfo
        """
        return

    @abc.abstractmethod
    def get_enumeration_info(self, enumeration_path):
        """
        Gets metadata for enumeration specified by enumeration path

        :param enumeration_path: enumeration path
        :type enumeration_path: :class:`str`
        :return: Enumeration info object specified by enumeration path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.EnumerationInfo
        """
        return

    @abc.abstractmethod
    def get_operation_info(self, operation_path, operation_name):
        """
        Gets metadata for operation specified by operation path and operation
        name

        :param operation_path: operation path
        :type operation_path: :class:`str`
        :param operation_name: operation name
        :type operation_name: :class:`str`
        :return: operation info object specified by operation path and
        operation name
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.OperationInfo
        """
        return

    @abc.abstractmethod
    def get_authentication_schemes(self, operation_path, operation_name):
        """
        Gets authentication schema for an operation specified by operation
        path and operation name

        :param operation_path: operation path
        operation resides
        :type operation_path: :class:`str`
        :param operation_name: operation name
        :type operation_name: :class:`str`
        :return: authentication schema for a specified operation
        :rtype: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
        """
        return

    @classmethod
    def get_cli_command_identity_from_metamodel_operation(cls, operation_path, operation_name, operation_info):
        """
        Gets dcli command identity object from given operation path, name, and OperationInfo object

        :param operation_path: operation cli path
        :type operation_path: :class:`str`
        :param operation_name: operation cli name
        :type operation_name: :class:`str`
        :param operation_info: operation info object
        :type operation_info: :class:`vmware.vapi.client.dcli.metadata.metadata_info.OperationInfo`
        :return: dcli command identity representation of the object
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandIdentityInfo`
        """
        return CommandIdentityInfo(operation_path,
                                   operation_name,
                                   operation_info.description)

    def get_cli_command_from_operation_info(self, operation, service_name):
        """
        Gets dcli command object from given dcli operation object and service name

        :param operation: operation info object
        :type operation: :class:`vmware.vapi.client.dcli.metadata.metadata_info.OperationInfo`
        :param service_name: service name the operation belongs to
        :type service_name: :class:`str`
        :return: dcli command representation of the object
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandInfo`
        """
        result = CommandInfo()
        result.identity = CommandIdentityInfo(service_name, operation.name, operation.description)
        result.identity.path = service_name.lower().replace('_', '')
        result.identity.name = operation.name.replace('_', '')
        result.identity.short_description = operation.description
        result.operation_id = operation.name
        result.service_id = service_name
        result.description = operation.description
        result.formatter = self.get_formatter(operation.output.type)

        # traverse parameters to get options
        result.options = []
        self.get_options_from_field_infos(operation.params, '', '', False, [], result.options)
        self.handle_options_long_names(result.options)

        out_fields = {}
        self.get_output_field_list(operation.output.type, out_fields, None, None, [])
        result.output_field_list = []
        for key, value in six.iteritems(out_fields):
            out_struct = OutputInfo()
            out_struct.structure_id = key
            out_struct.output_fields = value
            result.output_field_list.append(out_struct)

        return result

    def get_options_from_field_infos(self, fields, parent_field_name, parent_long_option, is_parent_optional, recursive_structs, options):
        """
        Get dcli command's options from list of provided dcli field info objects

        :param fields: list of field info objects
        :type fields: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.FieldInfo`
        :param parent_field_name: parent field name if the fields are coming from structure
        :type parent_field_name: :class:`str`
        :param parent_long_option: parent long name if the fields are coming from structure
        :type parent_long_option: :class:`str`
        :param is_parent_optional: is parent object, if any, is optional
        :type is_parent_optional: :class:`bool`
        :param recursive_structs: list of structures which are already traversed; used to catch recursive definitions
        :type recursive_structs: :class:`list` of :class:`str`
        :param options: result list of options collected from function
        :type options: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.OptionInfo`
        """
        for field in fields:
            self.get_options_from_field_info(field, field.type, parent_field_name, parent_long_option, is_parent_optional, recursive_structs, options)

    def get_options_from_field_info(self, field, field_type, parent_field_name, parent_long_option, is_parent_optional, recursive_structs, options):
        """
        Get dcli command's options from provided dcli field info object

        :param field: field info object
        :type field: :class:`vmware.vapi.client.dcli.metadata.metadata_info.FieldInfo`
        :param parent_field_name: parent field name if the fields are coming from structure
        :type parent_field_name: :class:`str`
        :param parent_long_option: parent long name if the fields are coming from structure
        :type parent_long_option: :class:`str`
        :param is_parent_optional: is parent object, if any, is optional
        :type is_parent_optional: :class:`bool`
        :param recursive_structs: list of structures which are already traversed; used to catch recursive definitions
        :type recursive_structs: :class:`list` of :class:`str`
        :param options: result list of options collected from function
        :type options: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.OptionInfo`
        """
        generic = option_type = None
        if field_type.category == 'GENERIC':
            if field_type.generic_instantiation.generic_type == 'optional':
                self.get_options_from_field_info(field,
                                                 field_type.generic_instantiation.element_type,
                                                 parent_field_name,
                                                 parent_long_option,
                                                 'optional',
                                                 recursive_structs,
                                                 options)
                return
            elif field_type.generic_instantiation.generic_type == 'map':
                generic = '' if not is_parent_optional else 'optional'
                option_type = 'complex'
            else:
                # list and set
                next_generic_type = field_type.generic_instantiation.element_type
                while next_generic_type.category == 'GENERIC':
                    if next_generic_type.generic_instantiation.generic_type == 'map':
                        break
                    next_generic_type = next_generic_type.generic_instantiation.element_type

                if next_generic_type.category != 'BUILTIN':
                    option_type = 'complex'
                else:
                    option_type = next_generic_type.builtin_type

                if is_parent_optional and next_generic_type.category == 'BUILTIN':
                    generic = 'optional_list'
                else:
                    if field_type.generic_instantiation.element_type.category == 'GENERIC' \
                            and field_type.generic_instantiation.element_type.generic_instantiation.generic_type == 'optional':
                        generic = 'list_optional'
                    elif field_type.generic_instantiation.element_type.category == 'USER_DEFINED':
                        generic = ''
                    else:
                        generic = 'list'

        elif field_type.category == 'BUILTIN':
            option_type = field_type.builtin_type.replace('_', '')  # replace needed for dynamic_structure case
            generic = '' if not is_parent_optional else 'optional'
            if option_type == 'dynamicstructure' and field.has_fields_of_struct_name:
                if field.has_fields_of_struct_name in recursive_structs:
                    return
                option_type = 'complex-hasfieldsof'
                generic = 'optional'
                hfo_structure = self.get_structure_info(field.has_fields_of_struct_name)
                recursive_structs.append(field.has_fields_of_struct_name)
                self.get_options_from_field_infos(hfo_structure.fields,
                                                  self.get_field_name(parent_field_name, field.serialization_name or field.name),
                                                  self.get_long_option_name(parent_long_option, field.name),
                                                  is_parent_optional,
                                                  recursive_structs,
                                                  options)
                recursive_structs.remove(field.has_fields_of_struct_name)
        else:
            # USER_DEFINED
            generic = '' if not is_parent_optional else 'optional'
            if field_type.user_defined_type.resource_id in recursive_structs:
                return
            if field_type.user_defined_type.resource_type == 'com.vmware.vapi.enumeration':
                option_type = field_type.user_defined_type.resource_id
                # todo: fill in options here
            else:
                ud_structure = self.get_structure_info(field_type.user_defined_type.resource_id)
                recursive_structs.append(field_type.user_defined_type.resource_id)
                self.get_options_from_field_infos(ud_structure.fields,
                                                  self.get_field_name(parent_field_name, field.serialization_name or field.name),
                                                  self.get_long_option_name(parent_long_option, field.name),
                                                  is_parent_optional,
                                                  recursive_structs,
                                                  options)
                recursive_structs.remove(field_type.user_defined_type.resource_id)
                return

        option = OptionInfo()
        option.long_option = self.get_long_option_name(parent_long_option, field.name)
        option.description = field.description
        option.field_name = self.get_field_name(parent_field_name, field.serialization_name or field.name)
        option.generic = generic
        option.type = option_type
        options.append(option)

    @classmethod
    def get_long_option_name(cls, parent_long_option, field_name):
        """
        Gets long option name from given field name and collected parent long name

        :param parent_long_option: collected parent long name
        :type parent_long_option: :class:`str`
        :param field_name: field name
        :type field_name: :class:`str`

        :return: long option name
        :rtype: :class:`str`
        """
        if parent_long_option:
            return '{}.{}'.format(parent_long_option, field_name.replace('_', '-').lower())
        return field_name.replace('_', '-').lower()

    @classmethod
    def get_field_name(cls, parent_field_name, field_name):
        """
        Gets cli field name from given field name and collected cli parent field name

        :param parent_field_name: collected parent field name
        :type parent_field_name: :class:`str`
        :param field_name: field name
        :type field_name: :class:`str`

        :return: field name
        :rtype: :class:`str`
        """
        if parent_field_name:
            return '{}.{}'.format(parent_field_name, field_name)
        return field_name

    @classmethod
    def get_formatter(cls, result_type):
        """
        Gets cli formatter type from given result type

        :param result_type: result type to deduce formatter from
        :type result_type: :class:`str`

        :return: formatter type
        :rtype: :class:`str`
        """
        if result_type.category == 'GENERIC' \
                and result_type.generic_instantiation.element_type is not None:
            tmp_type = result_type.generic_instantiation.element_type
            while tmp_type and tmp_type.category == 'GENERIC' \
                    and tmp_type.generic_instantiation.generic_type:
                tmp_type = tmp_type.generic_instantiation.element_type
            if tmp_type and tmp_type.category == 'USER_DEFINED':
                return 'table'
        if result_type.category == 'BUILTIN' \
                and result_type.builtin_type == 'void':
            return None
        return 'simple'

    @classmethod
    def handle_options_long_names(cls, options):
        """
        Takes care that there are no options with same name

        :param options: list of options to check
        :type options: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.OptionInfo`
        """
        cli_option_names = []
        for option in options:

            option_name_split = option.long_option.split('.')
            option_name = option_name_split[-1]
            if len(option_name_split) > 1:
                option_name = '-'.join(option_name_split[1:])

            index = 2
            temp_name = option_name
            while temp_name in cli_option_names:
                temp_name = '{}-{}'.format(option_name, index)
                index += 1
            option_name = temp_name

            option.long_option = option_name
            cli_option_names.append(option_name)

    def get_output_field_list(self, field_type, out_fields, parent_structure, parent_field, structs):
        """
        Get dcli command's output fields list from provided dcli field type object

        :param field_type: field type object
        :type field_type: :class:`vmware.vapi.client.dcli.metadata.metadata_info.TypeInfo`
        :param out_fields: result list of output fields collected from given field type
        :type out_fields: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.OutputInfo`
        :param parent_structure: parent structure if field_type is coming from such
        :type parent_structure: :class:`vmware.vapi.client.dcli.metadata.metadata_info.TypeInfo`
        :param parent_field: parent field if field type is coming from parent structure
        :type parent_field: :class:`str`
        :param structs: list of already visited structctures
        :type structs: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.StructureInfo`
        """
        if field_type.category == 'GENERIC':
            if field_type.generic_instantiation.generic_type in ['optional', 'list', 'set']:
                self.get_output_field_list(field_type.generic_instantiation.element_type, out_fields, parent_structure, parent_field, structs)
            else:
                # maps
                self.get_output_field_list(field_type.generic_instantiation.map_value_type, out_fields, parent_structure, parent_field, structs)
        elif field_type.category == 'USER_DEFINED':
            if field_type.user_defined_type.resource_type == 'com.vmware.vapi.structure' \
                    and field_type.user_defined_type.resource_id not in structs:
                ud_structure = self.get_structure_info(field_type.user_defined_type.resource_id)
                structs.append(field_type.user_defined_type.resource_id)
                out_fields[field_type.user_defined_type.resource_id] = []
                for field in ud_structure.fields:
                    out_field = OutputFieldInfo()
                    out_field.field_name = field.name
                    out_field.display_name = AbstractMetadataProvider.underscore_to_camel_case(field.name)
                    out_fields[field_type.user_defined_type.resource_id].append(out_field)
                    self.get_output_field_list(field.type, out_fields, field_type.user_defined_type.resource_id, field, structs)
        else:
            if field_type.builtin_type == 'dynamic_structure' \
                    and parent_field \
                    and parent_field.has_fields_of_struct_name \
                    and parent_field.has_fields_of_struct_name not in structs:
                ud_structure = self.get_structure_info(parent_field.has_fields_of_struct_name)
                structs.append(parent_field.has_fields_of_struct_name)
                out_fields[parent_field.has_fields_of_struct_name] = []
                for field in ud_structure.fields:
                    out_field = OutputFieldInfo()
                    out_field.field_name = field.name
                    out_field.display_name = AbstractMetadataProvider.underscore_to_camel_case(field.name)
                    out_fields[parent_field.has_fields_of_struct_name].append(out_field)
                    self.get_output_field_list(field.type, out_fields, parent_field.has_fields_of_struct_name, field, structs)

    @staticmethod
    def underscore_to_camel_case(field_name):
        """
        Converts underscore case fields to camel calse names

        :param field_name: field name to be converted
        :type field_name: :class:`str`

        :return: converted field name to camel case
        :rtype: :class:`str`
        """
        return ''.join(x.capitalize() or '_' for x in field_name.split('_'))
