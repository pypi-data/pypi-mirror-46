"""
This module provides concrete json-rpc provider of the abstract metadata
provider class
"""

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2017-2019 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import logging
import six

from com.vmware.vapi.std.introspection_client import Operation as \
    IntrospectionOperation
from com.vmware.vapi.metadata.cli_client import (Command, Namespace)
from com.vmware.vapi.metadata.authentication_client import \
    (Package as AuthenticationPackage, Service as AuthenticationService, AuthenticationInfo)
from com.vmware.vapi.metadata.authentication.service_client import Operation \
    as AuthenticationOperation
from com.vmware.vapi.metadata.metamodel_client import (
    Package, Service, Enumeration, Structure)
from com.vmware.vapi.metadata.metamodel.service_client import Operation as \
    MetamodelOperation
from com.vmware.vapi.std.errors_client import NotFound, OperationNotFound
from vmware.vapi.client.dcli.options import ArgumentChoice
from vmware.vapi.client.dcli.metadata.abstract_metadata_provider import \
    AbstractMetadataProvider
from vmware.vapi.data.serializers.introspection import \
    convert_data_value_to_data_def
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory
from vmware.vapi.client.dcli.metadata import converter
from vmware.vapi.client.dcli.metadata.input_definition_provider import InputDefinitionProvider
from vmware.vapi.client.dcli.metadata.metadata_info import NamespaceInfo, NamespaceIdentityInfo

logger = logging.getLogger(__name__)


def memoize(function):
    """
    Decorator to memorize function's output based on
    function's input. It would return cached value on subsequent calls

    :param function: decorated function
    :type function: :class:`function`
    :return: result of command execution or already cached value
    :rtype: :class:`object`
    """
    memo = {}

    def wrapper(*args):
        """
        Decorator wrapper
        """
        key_args = []
        for arg in args:
            if isinstance(arg, dict):
                # we need to frozenset dicts as they are not
                # hashable thus can not be dict key
                key_args.append(frozenset(six.iteritems(arg)))
            else:
                key_args.append(arg)
        # key args must be tuple as list is not hashable neither
        key_args = tuple(key_args)
        if key_args in memo:
            return memo[key_args]
        else:
            rv = function(*args)
            memo[key_args] = rv
        return rv
    return wrapper


class ServiceMetadataProvider(AbstractMetadataProvider):
    """
    Implementation of the :class:`vmware.vapi.client.dcli.metadata
    .abstract_metadata_provider.AbstractMetadataProvider`
    which takes metadata information from the cli metadata and metamodel vapi
    services
    """

    def __init__(self, connector, use_metamodel_only=False):
        self.use_metamodel_only = use_metamodel_only
        self.stub_config = StubConfigurationFactory.new_std_configuration(
            connector)

        # cli metadata stubs
        self.cmd_instance_stub = Command(self.stub_config)
        self.ns_instance_stub = Namespace(self.stub_config)

        # introspection stubs
        self.introspection_operation_stub = \
            IntrospectionOperation(self.stub_config)

        # metamodel stubs
        self.package_stub = Package(self.stub_config)
        self.service_stub = Service(self.stub_config)
        self.structure_stub = Structure(self.stub_config)
        self.enumeration_stub = Enumeration(self.stub_config)
        self.metamodel_operation_stub = MetamodelOperation(self.stub_config)

        # authentication stubs
        self.authentication_package_stub = AuthenticationPackage(self.stub_config)
        self.authentication_service_stub = AuthenticationService(self.stub_config)
        self.authentication_operation_stub = \
            AuthenticationOperation(self.stub_config)

    @memoize
    def get_commands(self, namespace_path=None):
        """
        Gets list of commands for the specified namespace path

        :param namespace_path: namespace path to retrieve commands from
        :type namespace_path: :class:`str`
        :return: list of commands
        :rtype: :class:`list` of
            :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandIdentityInfo`
        """
        if self.use_metamodel_only:
            commands = []
            for package_id in self.get_packages():
                package_info = self.get_package_info(package_id)
                package_cli_name = package_info.name.lower().replace('_', '')
                if namespace_path:
                    if not namespace_path.startswith(package_cli_name):
                        continue
                for service_name, service_info in six.iteritems(package_info.services):
                    operation_path = service_name.lower().replace('_', '')
                    service_cli_name = service_name.lower().replace('_', '')
                    if namespace_path and not namespace_path.startswith(service_cli_name):
                        continue
                    for _, operation_info in six.iteritems(service_info.operations):
                        operation_name = operation_info.name.lower().replace('_', '')
                        commands.append(self.get_cli_command_identity_from_metamodel_operation(operation_path, operation_name, operation_info))
            return commands

        return [converter.convert_command_identity_to_dcli_data_object(
            cmd_identity)
                for cmd_identity in self.cmd_instance_stub.list(namespace_path)]

    @memoize
    def get_command_info(self, namespace_path, command_name):
        """
        Gets command metadata info by specified command name and namespace path

        :param namespace_path: namespace path to the command
        :type namespace_path: :class:`str`
        :param command_name: command name
        :type command_name: :class:`str`
        :return: command metdata info object
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.CommandInfo`
        """
        if self.use_metamodel_only:
            result = None
            for package_id in self.get_packages():
                package_info = self.get_package_info(package_id)
                package_cli_name = package_info.name.lower().replace('_', '')
                if namespace_path:
                    if not namespace_path.startswith(package_cli_name):
                        continue
                for service_name, service_info in six.iteritems(package_info.services):
                    service_cli_name = service_name.lower().replace('_', '')
                    if namespace_path and not namespace_path.startswith(service_cli_name):
                        continue
                    for _, operation_info in six.iteritems(service_info.operations):
                        operation_name = operation_info.name.lower().replace('_', '')
                        if operation_name != command_name:
                            continue
                        result = self.get_cli_command_from_operation_info(operation_info, service_name)
                        break
                    if result:
                        break
                if result:
                    break
            if not result:
                raise NotFound("Command '{}' not found on namespace '{}'".format(command_name, namespace_path))
        else:
            cmd_id = Command.Identity(path=namespace_path, name=command_name)
            cli_metadata_cmd = self.cmd_instance_stub.get(identity=cmd_id)
            result = converter.convert_cli_command_to_dcli_data_object(
                cli_metadata_cmd)

        # fill in input definition from introspection service
        try:
            result.input_definition = self.get_command_input_definition(
                result.service_id, result.operation_id)
        except NotFound:
            logger.error("Introspection information was not found for "
                         "operation '%s' in service '%s'", command_name, namespace_path)
            result.input_definition = None

        for option in result.options:
            # Handle enumeration case. Only in case of enum types
            # we store fully qualified names, for all others its type name
            if option.type.find('.') != -1:
                try:
                    enum_info = self.get_enumeration_info(option.type)
                    option.choices = [ArgumentChoice(enum_val, enum_val, '') for enum_val in enum_info.values] if enum_info else []
                except OperationNotFound:
                    pass
                except NotFound:
                    pass

        return result

    @memoize
    def get_namespaces(self):
        """
        Gets the list of namespaces

        :return: list of namespace identity objects
        :rtype: :class:`list` of type
            :class:`vmware.vapi.client.dcli.metadata.metadata_info.NamespaceIdentityInfo`
        """
        if self.use_metamodel_only:
            namespaces = []
            for package_id in self.get_packages():
                package_info = self.get_package_info(package_id)
                package_cli_name = package_info.name.lower().replace('_', '')
                ns_path, _, ns_name = package_cli_name.rpartition('.')
                ns = NamespaceIdentityInfo(ns_path, ns_name, package_info.description)
                namespaces.append(ns)
                prev_tokens = ''
                for token in package_cli_name.split('.'):
                    ns = NamespaceIdentityInfo(prev_tokens, token, '')
                    if ns not in namespaces:
                        namespaces.append(ns)
                    prev_tokens += '.{}'.format(token) if prev_tokens else token
                for service_name, service_info in six.iteritems(package_info.services):
                    service_cli_name = service_name.lower().replace('_', '')
                    ns_path, _, ns_name = service_cli_name.rpartition('.')
                    ns = NamespaceIdentityInfo(ns_path, ns_name, service_info.description)
                    namespaces.append(ns)
            return namespaces

        return [converter.convert_namespace_identity_to_dcli_data_object(
            ns_identity)
                for ns_identity in self.ns_instance_stub.list()]

    @memoize
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
        if self.use_metamodel_only:
            namespace_full_path = '{}.{}'.format(namespace_path, namespace_name) if namespace_path else namespace_name
            ns_identity = None
            if namespace_full_path == '':
                ns_identity = NamespaceIdentityInfo(namespace_path,
                                                    namespace_name,
                                                    '')
            if not ns_identity:
                for package_id in self.get_packages():
                    package_info = self.get_package_info(package_id)
                    package_cli_name = package_info.name.lower().replace('_', '')
                    if package_cli_name.startswith(namespace_full_path) \
                            and package_cli_name.partition(namespace_full_path)[-1].startswith('.'):
                        ns_identity = NamespaceIdentityInfo(namespace_path,
                                                            namespace_name,
                                                            '')
                        continue
                    elif package_cli_name == namespace_full_path:
                        ns_identity = NamespaceIdentityInfo(namespace_path,
                                                            namespace_name,
                                                            package_info.description)
                        break
                    for service_name, service_info in six.iteritems(package_info.services):
                        service_cli_name = service_name.lower().replace('_', '')
                        if service_cli_name == namespace_full_path:
                            ns_identity = NamespaceIdentityInfo(namespace_path, namespace_name, service_info.description)
                            break
                    else:
                        continue
                    break
                if not ns_identity:
                    raise NotFound("Namespace '{}' not found".format(namespace_full_path))

            result_ns = NamespaceInfo()
            result_ns.identity = ns_identity
            result_ns.description = ns_identity.short_description
            result_ns.children = []

            for package_id in self.get_packages():
                package_info = self.get_package_info(package_id)
                package_cli_name = package_info.name.lower().replace('_', '')
                package_path, _, package_name = package_cli_name.rpartition('.')
                if package_path == namespace_full_path:
                    child_ns = NamespaceIdentityInfo(package_path, package_name, package_info.description)
                    if child_ns not in result_ns.children:
                        result_ns.children.append(child_ns)
                elif package_path.startswith(namespace_full_path):
                    if namespace_full_path:
                        child_namespace_name = package_path.partition(namespace_full_path)[-1].strip('.').split('.')[0]
                    else:
                        child_namespace_name = package_path.split('.')[0]
                    child_ns = NamespaceIdentityInfo(namespace_full_path,
                                                     child_namespace_name,
                                                     '')
                    if child_ns not in result_ns.children:
                        result_ns.children.append(child_ns)
                for service_name, service_info in six.iteritems(package_info.services):
                    service_cli_name = service_name.lower().replace('_', '')
                    if service_cli_name.rpartition('.')[0] == namespace_full_path:
                        child_ns = NamespaceIdentityInfo(namespace_full_path, service_cli_name.rpartition('.')[-1], service_info.description)
                        result_ns.children.append(child_ns)

            return result_ns
        else:
            ns_id = Namespace.Identity(path=namespace_path, name=namespace_name)
            cli_metadata_ns = self.ns_instance_stub.get(identity=ns_id)
            result = converter.convert_cli_namespace_to_dcli_data_object(
                cli_metadata_ns)
            return result

    @memoize
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
        if self.use_metamodel_only:
            return InputDefinitionProvider(self)\
                .get_method_input_definition(service_path, operation_name)

        method_info = self.introspection_operation_stub.get(
            service_id=service_path,
            operation_id=operation_name)
        return convert_data_value_to_data_def(
            method_info.input_definition.get_struct_value())

    @memoize
    def get_packages(self):
        """
        Gets list of package ids

        :return: list of package ids
        :rtype: :class:`list` of :class:`str`
        """
        return self.package_stub.list()

    @memoize
    def get_package_info(self, package_id):
        """
        Gets metadata for package specified by package_id

        :param package_id: package id
        :type package_id: :class:`str`
        :return: Package info object found by specified package id
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.PackageInfo`
        """
        metamodel_package = self.package_stub.get(package_id=package_id)
        return converter.convert_package_from_metamodel_to_dcli_data_object(metamodel_package)

    @memoize
    def get_service_info(self, service_path):
        """
        Gets metadata for service specified by service path

        :param service_path: service path
        :type service_path: :class:`str`
        :return: Service info object found by specified service path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.ServiceInfo`
        """
        metamodel_service_info = self.service_stub.get(service_path)
        return converter.convert_service_from_metamodel_to_dcli_data_object(
            metamodel_service_info)

    @memoize
    def get_structure_info(self, structure_path):
        """
        Gets metadata for structure specified by structure path

        :param structure_path: structure path
        :type structure_path: :class:`str`
        :return: Structure info object found by specified structure path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.StructureInfo`
        """
        metamodel_struct_info = self.structure_stub.get(structure_path)
        return converter.convert_struct_from_metamodel_to_dcli_data_object(
            metamodel_struct_info)

    @memoize
    def get_enumeration_info(self, enumeration_path):
        """
        Gets metadata for enumeration specified by enumeration path

        :param enumeration_path: enumeration path
        :type enumeration_path: :class:`str`
        :return: Enumeration info object specified by enumeration path
        :rtype: :class:`vmware.vapi.client.dcli.metadata.metadata_info.EnumerationInfo
        """
        metamodel_enum_info = self.enumeration_stub.get(enumeration_path)
        return converter.convert_enum_from_metamodel_to_dcli_data_object(
            metamodel_enum_info)

    @memoize
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
        metamodel_operation_info = self.metamodel_operation_stub.get(
            operation_path, operation_name)
        return \
            converter.convert_operation_from_metamodel_to_dcli_data_object(
                metamodel_operation_info)

    @memoize
    def get_authentication_schemes(self, operation_path, operation_name):
        """
        Gets authentication schema for an operation specified by operation
        path and operation name

        :param operation_path: operation path
        :type operation_path: :class:`str`
        :param operation_name: operation name
        :type operation_name: :class:`str`
        :return: authentication schema for a specified operation
        :rtype: :class:`dict` of :class:`str` and :class:`list` of :class:`str`
        """
        auth_schemas = {}
        self._get_authentication_schemes_internal(auth_schemas,
                                                  operation_path,
                                                  operation_name,
                                                  False)
        return auth_schemas

    def _get_authentication_schemes_internal(self,
                                             auth_schemes,
                                             path,
                                             cmd,
                                             is_session_aware):
        """
        Method to get valid authentication schemes for a given vAPI command

        :type  auth_schemes: :class:`map`
        :param auth_schemes: Authentication scheme and scheme type
        :type  path: :class:`str`
        :param path: vAPI command path
        :type  cmd: :class:`str`
        :param cmd: vAPI command name
        :type  is_session_aware: :class:`bool`
        :param is_session_aware: Is authentication scheme type session aware
        """
        schemes = []
        try:
            operation_info = \
                self.authentication_operation_stub.get(path, cmd)
            schemes = operation_info.schemes
        except NotFound:
            # if this call came through session aware try login method
            # instead of create
            # XXX remove this code once everyone moves over to create/delete
            # methods
            if is_session_aware and cmd == 'create':
                self._get_authentication_schemes_internal(auth_schemes, path, 'login', True)
                return
        except OperationNotFound:
            return

        if not schemes:
            try:
                service_info = \
                    self.authentication_service_stub.get(path)
                schemes = service_info.schemes
            except NotFound:
                pass

            while not schemes and path.find('.') != -1:
                pkg_name = path.rsplit('.', 1)[0]
                try:
                    package_info = \
                        self.authentication_package_stub.get(pkg_name)
                    schemes = package_info.schemes
                    path = pkg_name
                except NotFound:
                    path = pkg_name

        for scheme in schemes:
            if scheme.scheme_type == AuthenticationInfo.SchemeType.SESSIONLESS:
                # if the call came from SessionAware scheme type store
                # session manager path
                auth_schemes.setdefault(scheme.scheme, [])\
                    .append(path if is_session_aware else None)
            elif scheme.scheme_type == \
                    AuthenticationInfo.SchemeType.SESSION_AWARE:
                # In case of SessionAware we need to find the authentication
                # scheme of the login method of the session manager
                self._get_authentication_schemes_internal(auth_schemes,
                                                          scheme.session_manager, 'create', True)
