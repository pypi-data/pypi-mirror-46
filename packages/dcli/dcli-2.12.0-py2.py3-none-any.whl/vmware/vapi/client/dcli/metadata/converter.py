"""
This module provides conversion from metadata bindings types to
dcli specific metadta types
"""

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2016-2018 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import six

from vmware.vapi.client.dcli.metadata.metadata_info import (
    CommandIdentityInfo, CommandInfo,
    NamespaceIdentityInfo, NamespaceInfo, OptionInfo,
    OutputInfo, OutputFieldInfo, PackageInfo, ServiceInfo, StructureInfo,
    FieldInfo, TypeInfo, UserDefinedTypeInfo, GenericInstantiationInfo,
    UnionTagInfo, UnionCaseInfo, EnumerationInfo, OperationInfo, OperationResultInfo)
from vmware.vapi.client.dcli.util import CliGenericTypes, TypeInfoGenericTypes
from com.vmware.vapi.metadata.metamodel_client import (GenericInstantiation,
                                                       MetadataIdentifier)
from com.vmware.vapi.metadata.cli_client import Command

LIST_TYPE = Command.GenericType('LIST')
OPTIONAL_TYPE = Command.GenericType('OPTIONAL')
LIST_OF_OPTIONAL_TYPE = Command.GenericType('LIST_OPTIONAL')
OPTIONAL_LIST_TYPE = Command.GenericType('OPTIONAL_LIST')
NONE_TYPE = Command.GenericType('NONE')

generic_type_dict = {
    LIST_TYPE: CliGenericTypes.list_type,
    OPTIONAL_TYPE: CliGenericTypes.optional_type,
    OPTIONAL_LIST_TYPE: CliGenericTypes.optional_list_type,
    LIST_OF_OPTIONAL_TYPE: CliGenericTypes.list_of_optional_type,
    NONE_TYPE: CliGenericTypes.none_type
}

type_info_generic_types_dict = {
    GenericInstantiation.GenericType.OPTIONAL: TypeInfoGenericTypes.optional_type,
    GenericInstantiation.GenericType.LIST: TypeInfoGenericTypes.list_type,
    GenericInstantiation.GenericType.SET: TypeInfoGenericTypes.set_type,
    GenericInstantiation.GenericType.MAP: TypeInfoGenericTypes.map_type
}

UNION_CASE = "UnionCase"
UNION_TAG = "UnionTag"


def convert_command_identity_to_dcli_data_object(cmd_identity,
                                                 short_description=None):
    """
    Converts from metadata command identity to dcli command identity object

    :param cmd_identity: command identity to convert from
    :type cmd_identity: :class:`com.vmware.vapi.metadata.cli_client.Command.Identity`
    :return: dcli command identity representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandIdentityInfo`
    """
    return CommandIdentityInfo(cmd_identity.path, cmd_identity.name, short_description)


def convert_namespace_identity_to_dcli_data_object(ns_identity,
                                                   short_description=None):
    """
    Converts from metadata namespace identity to dcli namesapce identity object

    :param ns_identity: namespace identity object to convert from
    :type ns_identity: :class:`com.vmware.vapi.metadata.cli_client.Namespace.Identity`
    :return: dcli namespace identity representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.NamespaceIdentityInfo`
    """
    return NamespaceIdentityInfo(ns_identity.path, ns_identity.name, short_description)


def convert_cli_command_to_dcli_data_object(cli_command):
    """
    Converts from metadata command to dcli command object

    :param cli_command: command object to convert from
    :type cli_command: :class:`com.vmware.vapi.metadata.cli_client.Command`
    :return: dcli command representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandInfo`
    """
    result = CommandInfo()
    result.identity = CommandIdentityInfo(cli_command.identity.path,
                                          cli_command.identity.name,
                                          cli_command.description)

    result.description = cli_command.description
    if cli_command.formatter is not None:
        result.formatter = cli_command.formatter.lower()
    result.service_id = cli_command.service_id
    result.operation_id = cli_command.operation_id

    if cli_command.options is not None:
        result.options = []
    for option in cli_command.options:
        result_option = OptionInfo()
        result_option.long_option = option.long_option
        result_option.short_option = option.short_option
        result_option.field_name = option.field_name
        result_option.description = option.description
        result_option.type = option.type
        result_option.generic = generic_type_dict[option.generic]

        result.options.append(result_option)

    if cli_command.output_field_list is not None:
        result.output_field_list = []
    for output_field in cli_command.output_field_list:
        result_output_field = OutputInfo()
        result_output_field.structure_id = output_field.structure_id

        if output_field.output_fields is not None:
            result_output_field.output_fields = []
        for output_field_info in output_field.output_fields:
            result_output_field_info = OutputFieldInfo()
            result_output_field_info.field_name = \
                output_field_info.field_name
            result_output_field_info.display_name = \
                output_field_info.display_name

            result_output_field.output_fields.append(
                result_output_field_info)

        result.output_field_list.append(result_output_field)

    return result


def convert_cli_namespace_to_dcli_data_object(cli_namespace):
    """
    Converts from metadata namespace to dcli namesapce object

    :param cli_namespace: namespace object to convert from
    :type cli_namespace: :class:`com.vmware.vapi.metadata.cli_client.Namespace`
    :return: dcli namespace representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.NamespaceInfo`
    """
    result = NamespaceInfo()
    result.identity = NamespaceIdentityInfo(
        cli_namespace.identity.path,
        cli_namespace.identity.name,
        cli_namespace.description)
    result.description = cli_namespace.description
    if cli_namespace.children is not None:
        result.children = []
    for child in cli_namespace.children:
        result_child = NamespaceIdentityInfo(child.path, child.name)
        result.children.append(result_child)

    return result


def convert_package_from_metamodel_to_dcli_data_object(metamodel_package):
    """
    Convert metamodel package to dcli package object

    :param metamodel_package: metamodel package object to convert from
    :type metamodel_package: :class:`com.vmware.vapi.metadata.metamodel_client.PackageInfo`
    :return: dcli package representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.PackageInfo`
    """
    result = PackageInfo()
    result.name = metamodel_package.name
    result.description = get_description(metamodel_package.documentation)
    result.structures = {}
    for structure, info in six.iteritems(metamodel_package.structures):
        result.structures[structure] = convert_struct_from_metamodel_to_dcli_data_object(info)
    result.enumerations = {}
    for enumeration, info in six.iteritems(metamodel_package.enumerations):
        result.enumerations[enumeration] = convert_enum_from_metamodel_to_dcli_data_object(info)
    result.services = {}
    for service, info in six.iteritems(metamodel_package.services):
        result.services[service] = convert_service_from_metamodel_to_dcli_data_object(info)
    return result


def convert_service_from_metamodel_to_dcli_data_object(metamodel_service):
    """
    Convert metamodel service to dcli service object

    :param metamodel_service: metamodel service object to convert from
    :type metamodel_service: :class:`com.vmware.vapi.metadata.metamodel_client.ServiceInfo`
    :return: dcli service representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.ServiceInfo`
    """
    result = ServiceInfo()
    result.name = metamodel_service.name
    result.description = get_description(metamodel_service.documentation)
    result.operations = {}
    for operation, info in six.iteritems(metamodel_service.operations):
        result.operations[operation] = convert_operation_from_metamodel_to_dcli_data_object(info)
    result.structures = {}
    for structure, info in six.iteritems(metamodel_service.structures):
        result.structures[structure] = convert_struct_from_metamodel_to_dcli_data_object(info)
    result.enumerations = {}
    for enumeration, info in six.iteritems(metamodel_service.enumerations):
        result.enumerations[enumeration] = convert_enum_from_metamodel_to_dcli_data_object(info)

    if 'DynamicContract' in metamodel_service.metadata \
            and hasattr(metamodel_service.metadata['DynamicContract'], 'elements') \
            and 'service' in metamodel_service.metadata['DynamicContract'].elements \
            and hasattr(metamodel_service.metadata['DynamicContract'].elements['service'], 'string_value'):
        result.dynamic_contract_service = metamodel_service.metadata['DynamicContract'].elements['service'].string_value

    return result


def convert_struct_from_metamodel_to_dcli_data_object(metamodel_struct):
    """
    Convert metamodel structure to dcli structure object

    :param metamodel_struct: metamodel structure object to convert from
    :type metamodel_struct: :class:`com.vmware.vapi.metadata.metamodel_client.StructureInfo`
    :return: dcli structure representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.StructureInfo`
    """
    result = StructureInfo()
    result.name = metamodel_struct.name
    result.fields = _get_fields_info_from_metamodel(metamodel_struct.fields)

    return result


def _get_fields_info_from_metamodel(metamodel_fields):
    """
    Returns collection of metadata_info.FieldInfo objects converted from
    metamodel's FieldInfo objects

    :param metamodel_fields: metamodel collection of object to take information from
    :type metamodel_fields: :class:`list` of :class:`com.vmware.vapi.metadata.metamodel_client.FieldInfo`
    :return: dcli collection representation of the metamodel collection
    :rtype: :class:`list` of :class:`vmware.vapi.client.dcli.metadata.metadata_info.FieldInfo`
    """
    if metamodel_fields is not None:
        result_fields = []
    else:
        return None

    for field in metamodel_fields:
        result_field = FieldInfo()
        result_field.name = field.name
        result_field.type = TypeInfo()
        result_field.description = get_description(field.documentation)
        _fill_type_info_from_metamodel(field.type, result_field.type)
        _fill_unions_info_from_metamodel(field, result_field)

        if hasattr(field, 'metadata'):
            if MetadataIdentifier.HAS_FIELDS_OF in field.metadata \
                    and hasattr(field.metadata[MetadataIdentifier.HAS_FIELDS_OF],
                                'elements') \
                    and 'value' in field.metadata[
                        MetadataIdentifier.HAS_FIELDS_OF].elements:
                result_field.has_fields_of_struct_name = \
                    field.metadata[
                        MetadataIdentifier.HAS_FIELDS_OF].elements['value'].string_value
            if 'Discriminator' in field.metadata:
                result_field.is_discriminator = True
            if 'SerializationName' in field.metadata:
                result_field.serialization_name = field.metadata['SerializationName'].elements['value'].string_value
            if 'DynamicContract' in field.metadata \
                    and hasattr(field.metadata['DynamicContract'], 'elements') \
                    and 'service' in field.metadata['DynamicContract'].elements \
                    and hasattr(field.metadata['DynamicContract'].elements['service'], 'string_value'):
                result_field.dynamic_contract_service = field.metadata['DynamicContract'].elements['service'].string_value

        result_fields.append(result_field)
    return result_fields


def _fill_type_info_from_metamodel(metamodel_type, result_type):
    """
    Fills in type information to dcli type object from metamodel type object

    :param metamodel_field: metamodel object to take information from
    :type metamodel_field: :class:`com.vmware.vapi.metadata.metamodel_client.StructureInfo.Type`
    :param result_type: dcli type object to fill up
    :type result_type: :class:`vmware.vapi.client.dcli.metadata.metadata_info.TypeInfo`
    """
    result_type.category = metamodel_type.category.upper()
    if result_type.category == 'BUILTIN':
        result_type.builtin_type = metamodel_type.builtin_type.lower()
    elif result_type.category == 'USER_DEFINED':
        result_type.user_defined_type = UserDefinedTypeInfo()
        result_type.user_defined_type.resource_type = \
            metamodel_type.user_defined_type.resource_type
        result_type.user_defined_type.resource_id = \
            metamodel_type.user_defined_type.resource_id
    else:  # category is GENERIC
        result_type.generic_instantiation = \
            GenericInstantiationInfo()
        result_type.generic_instantiation.generic_type = \
            type_info_generic_types_dict[metamodel_type.generic_instantiation.generic_type]
        if result_type.generic_instantiation.generic_type in \
                ['optional', 'list', 'set']:
            generic_inner_type = TypeInfo()
            _fill_type_info_from_metamodel(
                metamodel_type.generic_instantiation.element_type,
                generic_inner_type)
            result_type.generic_instantiation.element_type = \
                generic_inner_type
        else:
            map_key_type = TypeInfo()
            map_value_type = TypeInfo()
            _fill_type_info_from_metamodel(
                metamodel_type.generic_instantiation.map_key_type,
                map_key_type
            )
            _fill_type_info_from_metamodel(
                metamodel_type.generic_instantiation.map_value_type,
                map_value_type
            )
            result_type.generic_instantiation.map_key_type = map_key_type
            result_type.generic_instantiation.map_value_type = map_value_type


def _fill_unions_info_from_metamodel(metamodel_field, result_field):
    """
    Fills in unions information to dcli field object from metamodel field object

    :param metamodel_field:  metamodel object to take information from
    :type metamodel_field: :class:`com.vmware.vapi.metadata.metamodel_client.FieldInfo`
    :param result_field: dcli field object to fill up
    :type result_field: :class:`vmware.vapi.client.dcli.metadata.metadata_info.FieldInfo`
    """
    if hasattr(metamodel_field, 'metadata') and \
            UNION_TAG in metamodel_field.metadata and \
            hasattr(metamodel_field.metadata[UNION_TAG], 'elements') and \
            'value' in metamodel_field.metadata[UNION_TAG].elements:
        result_field.union_tag = UnionTagInfo()
        result_field.union_tag.name = \
            metamodel_field.metadata[UNION_TAG].elements['value'].string_value
    elif hasattr(metamodel_field, 'metadata') and \
            UNION_CASE in metamodel_field.metadata and \
            hasattr(metamodel_field.metadata[UNION_CASE], 'elements') and \
            'value' in metamodel_field.metadata[UNION_CASE].elements:
        result_field.union_case = UnionCaseInfo()
        result_field.union_case.tag_name = \
            metamodel_field.metadata[UNION_CASE].elements['tag'].string_value
        result_field.union_case.list_value = \
            metamodel_field.metadata[UNION_CASE].elements['value'].list_value


def convert_enum_from_metamodel_to_dcli_data_object(metamodel_enum):
    """
    Convert metamodel enumeration to dcli enumeration object

    :param metamodel_enum: metamodel enumeration object to convert from
    :type metamodel_enum: :class:`com.vmware.vapi.metadata.metamodel_client.EnumerationInfo`
    :return: dcli enumeration representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.EnumerationInfo`
    """
    enum_info = EnumerationInfo()
    enum_info.name = metamodel_enum.name
    enum_info.values = [value.value for value in metamodel_enum.values]
    return enum_info


def convert_operation_from_metamodel_to_dcli_data_object(metamodel_operation):
    """
    Convert metamodel operation to dcli operation object

    :param metamodel_operation: metamodel operation object to convert from
    :type metamodel_operation: :class:`com.vmware.vapi.metadata.metamodel_client.OperationInfo`
    :return: dcli operation representation of the object
    :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.OperationInfo`
    """
    result = OperationInfo()
    result.name = metamodel_operation.name
    result.description = get_description(metamodel_operation.documentation)
    result.params = _get_fields_info_from_metamodel(metamodel_operation.params)

    result.output = OperationResultInfo()
    result.output.type = TypeInfo()
    _fill_type_info_from_metamodel(metamodel_operation.output.type, result.output.type)

    return result


def get_description(documentation):
    """
    From given metamodel documentation produces cli description

    :param documentation: metamodel documentation
    :type documentation: :class:`str`
    :return: cli description
    :rtype: :class:`str`
    """
    lines = documentation.split('. ')
    lines = lines[0].split('\n')
    return lines[0]
