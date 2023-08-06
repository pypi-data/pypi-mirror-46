"""
dcli shell
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright (c) 2015-2019 VMware, Inc.  All rights reserved. '
__license__ = 'SPDX-License-Identifier: MIT'
__docformat__ = 'epytext en'

import argparse
import os
import sys
import logging
import shlex
from collections import OrderedDict

try:
    from prompt_toolkit.history import FileHistory, InMemoryHistory
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.styles import Style
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles.pygments import style_from_pygments_cls
    from prompt_toolkit.styles import merge_styles
    from pygments.styles import get_style_by_name
    from pygments.token import Text, Comment
    have_pyprompt = True
except ImportError:
    have_pyprompt = False

import six

from vmware.vapi.client.dcli.options import CliOptions, ArgumentChoice
from vmware.vapi.client.dcli.util import (
    CliHelper, StatusCode, BoolAction, BoolAppendAction, ServerTypes,
    print_top_level_help, calculate_time, print_dcli_text, html_escape)
from vmware.vapi.client.dcli.exceptions import (
    handle_error, extract_error_msg, CommandCollision,
    CliArgumentException)

DCLI_COMMANDS = OrderedDict([
    ('clear', 'Clear the screen'),
    ('cls', 'Clear the screen'),
    ('exit', 'Exit the shell'),
    ('help', 'Print all shell commands'),
    ('ls', 'Print top level namespace help'),
    ('reload', 'Reload cache for CLI shell'),
    ('shell', 'Execute a shell command'),
    ('$?', 'Print return code for previous command')
])


DCLI_SKIP_PREFIX = 'com.vmware'

logger = logging.getLogger(__name__)

if have_pyprompt:
    def get_secure_history_string(string, completer):
        """
        Helper function which expands short command and returns it back
        with securely escaped argument input
        """
        exp_cmd = completer.expand_short_command(string)
        is_command, secret_map = completer.cli_main.get_command_secret_map(exp_cmd.split())
        if is_command and secret_map:
            exp_cmd = completer.cli_main.get_secure_command(exp_cmd.split(),
                                                            secret_map,
                                                            substitute='')
            string_arg_index = string.find('-') if string.find('-') > -1 else string.find('+')
            exp_cmd_arg_index = exp_cmd.find('-') if exp_cmd.find('-') > -1 else exp_cmd.find('+')
            if string_arg_index > -1 and exp_cmd_arg_index > 1:
                string = string[:string_arg_index] + exp_cmd[exp_cmd_arg_index:]
        return string

    class DcliFileHistory(FileHistory):
        """
        Overwrites prompt_toolkit FileHistory class to secure saved history
        """
        def __init__(self, filename, completer):  # pylint: disable=E1002
            self.completer = completer
            super(DcliFileHistory, self).__init__(filename)

        def append_string(self, string):  # pylint: disable=E1002
            """
            Append's given command string to history
            """
            string = get_secure_history_string(string, self.completer)
            super(DcliFileHistory, self).append_string(string)

    class DcliInMemoryHistory(InMemoryHistory):
        """
        Overwrites prompt_toolkit InMemoryHistory class to secure in-memroy preserved history
        """
        def __init__(self, completer):  # pylint: disable=E1002
            self.completer = completer
            super(DcliInMemoryHistory, self).__init__()

        def append_string(self, string):  # pylint: disable=E1002
            """
            Append's given command string to history
            """
            string = get_secure_history_string(string, self.completer)
            super(DcliInMemoryHistory, self).append_string(string)

    class PypromptCompleter(Completer):
        """
        Class to auto complete dcli commands and options in interactive mode
        """
        def __init__(self, cli_main):
            self.cli_main = cli_main
            self.current_cmd = None
            self.current_discriminator_value = {}
            self.cmd_args = []
            self.history = None

            self.set_prompt_history()

        def set_prompt_history(self):
            """
            Sets prompt history
            """
            if not os.path.exists(CliOptions.DCLI_HISTORY_FILE_PATH):
                self.history = DcliFileHistory(CliOptions.DCLI_HISTORY_FILE_PATH, self)
            elif not os.access(CliOptions.DCLI_HISTORY_FILE_PATH, os.R_OK):
                warning_msg = ("WARNING: No read permissions for history file '%s'.\n"
                               "Switching to in-memory history.") % (CliOptions.DCLI_HISTORY_FILE_PATH)
                logger.warning(warning_msg)
                print_dcli_text('<ansired>{}</ansired>'.format(html_escape(warning_msg)))
                self.history = DcliInMemoryHistory(self)
            elif not os.access(CliOptions.DCLI_HISTORY_FILE_PATH, os.W_OK):
                warning_msg = ("WARNING: No write permissions for history file '%s'.\n"
                               "Switching to in-memory history.") % (CliOptions.DCLI_HISTORY_FILE_PATH)
                logger.warning(warning_msg)
                print_dcli_text('<ansired>{}</ansired>'.format(html_escape(warning_msg)))
                self.history = DcliInMemoryHistory(self)
            else:
                self.history = DcliFileHistory(CliOptions.DCLI_HISTORY_FILE_PATH, self)

        @staticmethod
        def get_dcli_options(curr_key):
            """
            Method to return the dcli '+' options for auto completion

            :type   curr_key: :class:`string`
            :param  curr_key: Current typed key in interactive mode
            """
            return OrderedDict((option.name, ArgumentChoice(option.name, option.name, option.description)) for option in CliOptions.get_interactive_parser_plus_options()
                               if option.name.startswith(curr_key) and option.description != argparse.SUPPRESS)

        @staticmethod
        def sort_options(options):
            """
            Sort auto complete dcli options
            """
            sorted_options = sorted(options, key=lambda t: t[0])
            sorted_options = sorted(sorted_options, key=lambda t: t[2])
            return sorted_options

        def get_command_args(self, command, command_input=None):
            """
            Method to get input arguments struct for a command

            :type  command: :class:`string`
            :param command: vAPI command

            :rtype:  :class:`list` of :class:`ArgumentInfo`
            :return: List of ArgumentInfo object containing struct field details
            """
            self.cmd_args = []
            self.current_cmd = None
            path = command.rpartition('.')[0]
            name = command.split('.')[-1]
            cli_cmd_instance = self.cli_main.get_cmd_instance(path, name)

            if cli_cmd_instance and cli_cmd_instance.is_a_command():
                try:
                    retval, args = cli_cmd_instance.get_parser_arguments(command_input)
                except Exception:
                    retval = StatusCode.INVALID_COMMAND

                if retval == StatusCode.SUCCESS:
                    self.current_cmd = command
                    self.cmd_args = args

        def prepare_autocomplete_map(self, completer_root_key):
            """
            Alters the complete command map depending on whether
            completer_root_key contains one of the hidden namespace's name

            :type  completer_root_key: :class:`str`
            :param completer_root_key: command written on prompt so far

            :rtype:  :class:`list`
            :return: Updated command map completer
            """
            for hidden_ns in CliOptions.DCLI_HIDDEN_NAMESPACES:
                if hidden_ns['name'] and hidden_ns['name'] in completer_root_key or \
                        (not hidden_ns['name'] and hidden_ns['path'] in completer_root_key):
                    self.cli_main.cmd_map.update(self.cli_main.hidden_cmd_map)
                    break
            else:  # executed if no break or exception reached in the loop
                for key in self.cli_main.hidden_cmd_map:
                    self.cli_main.cmd_map.pop(key, None)

        def call_shell_commands(self, command):
            """
            Method to call special dcli interactive mode commands

            :type  command: :class:`str`
            :param command: dcli command

            :rtype:  :class:`StatusCode`
            :return: Status code
            """
            status = StatusCode.SUCCESS
            if command.lower() in ['clear', 'cls']:
                if os.name == 'nt':  # call cls for windows systems.
                    os.system('cls')
                else:
                    os.system('clear')
            elif command.lower() in ['ls']:
                status = self.cli_main.handle_command('', '')
            elif command == '$?':
                print_dcli_text(html_escape(status))
            elif command.lower() == 'reload':
                self.cli_metadata.cache_cli_metadata(self.cli_main.connections)
            elif command.lower() == 'help':
                print_dcli_text('<b>{}</b>'.format(html_escape('\t'.join(DCLI_COMMANDS.keys()))))
            elif command.split()[0] == 'shell':
                import signal
                import subprocess

                def _handler(_sig, _frame):
                    """
                    Interrupt handler for shell command
                    """
                    p.terminate()
                    p.communicate()

                if len(command.split()) == 1:
                    handle_error('Missing shell command that needs to be '
                                 'executed')
                    status = StatusCode.INVALID_COMMAND
                    return status

                logger.info('Invoking shell command: %s', command)
                command = command.split()[1:]
                try:
                    p = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, shell=False)
                except OSError as e:
                    error_msg = 'Command %s failed with: %s' % (' '.join(command), extract_error_msg(e))
                    handle_error(error_msg, exception=e)
                    status = StatusCode.INVALID_COMMAND
                    return status

                old_handler = signal.signal(signal.SIGINT, _handler)
                status = StatusCode.INVALID_COMMAND
                try:
                    status = p.wait()
                except OSError as e:
                    error_msg = 'Command %s terminated.' % ' '.join(command)
                    handle_error(error_msg, exception=e)
                finally:
                    signal.signal(signal.SIGINT, old_handler)

            return status

        def expand_short_command(self, command, throw=False):
            """
            Method to expand short commands
            """
            orig_command = command

            # Check if user entered 'short' version of the command
            arg_list = command.split()
            arg_index = [i for i, x in enumerate(arg_list) if x.startswith('-') or x.startswith('+')]
            index = len(arg_list) if not arg_index else arg_index[0]
            key = '.'.join(arg_list[0:index])
            dcli_commands = [cmd for cmd in self.cli_main.cmd_list if key in cmd]
            collected_collisions = []

            if not dcli_commands:
                command = orig_command
            elif len(dcli_commands) > 1:
                # Check if one of the possible command option matches the full
                # command name specified by the user.
                search_name = '.%s' % '.'.join(arg_list[0:index])
                matched_cmd = [cmd for cmd in dcli_commands if cmd.endswith(search_name)]
                if len(matched_cmd) == 1:
                    command = ' '.join(matched_cmd[0].split('.') + arg_list[index:])
                else:
                    # if more than two namespaces found for short cmd collect them to throw correct error later
                    if len(matched_cmd) > 1:
                        collected_collisions = collected_collisions + matched_cmd
                    dcli_commands = [ns for ns in self.cli_main.ns_list if ns.endswith(search_name)]
                    if dcli_commands and len(dcli_commands) == 1:
                        command = ' '.join(dcli_commands[0].split('.') + arg_list[index:])
                    elif dcli_commands and len(dcli_commands) > 1:  # more than two commands found for short cmd
                        collected_collisions = collected_collisions + dcli_commands
                    else:
                        command = orig_command
            else:
                if dcli_commands[0].endswith(key):  # case if the short cmd expands to vapi command
                    command = ' '.join(dcli_commands[0].split('.') + arg_list[index:])
                else:  # case if short cmd expands to vapi namepsace
                    namespace_cmd_idx_end = dcli_commands[0].index(key) + len(key)
                    namespace_cmd = dcli_commands[0][0:namespace_cmd_idx_end]
                    command = ' '.join(namespace_cmd.split('.') + arg_list[index:])

            if throw and collected_collisions:
                converted_collected_collisions = [command.replace('.', ' ') for command in collected_collisions]
                error_msg = "The command you are trying to execute is " \
                            "ambiguous. You can execute one of the " \
                            "following commands:\n"
                error_msg += '\n'.join(converted_collected_collisions)
                exception = CommandCollision(converted_collected_collisions,
                                             error_msg)
                handle_error(error_msg, prefix_message='')
                raise exception
            return command

        def get_completions(self, document, _):
            """
            Return possible auto completion value and handle errors to does not cause crash
            """
            try:
                # can not use 'yield from' since it's illegal statement on python 2.7
                for item in self.get_unhandled_completions(document):
                    yield item
            except Exception as e:
                handle_error('Auto complete error occured: {}'.format(str(e)), print_error=False, exception=e)
                msg = 'Error: Cannot autocomplete command.'
                if six.PY2:
                    msg = msg.decode()
                yield Completion('', display=msg)

        def complete_pyprompt_command_options(self, tokens, root_key, curr_key):
            """
            Method to get matches for vAPI command options and values

            :type  tokens: :class:`string`
            :param tokens: Complete tokens string entered on interactive shell
            :type  root_key: :class:`string`
            :param root_key: Root key
            :type  curr_key: :class:`string`
            :param curr_key: Current key
            """
            match_dict = OrderedDict()
            choices = []
            # This is probably a vAPI command, try to get command options.
            key = root_key.split('--')[0].rstrip('.')
            key = key.split('+')[0].rstrip('.')
            exp_cmd = self.expand_short_command(key)
            command = '.'.join(exp_cmd.split())

            split_tokens = tokens.rsplit()

            # if the command changed from the last command read args again
            args_values = CliHelper.get_args_values(tokens) if tokens else None
            if command != self.current_cmd \
                    or self.cmd_args is None:
                self.get_command_args(command, command_input=tokens)
            elif ([True
                   for arg in self.cmd_args
                   if arg.is_discriminator
                   and arg.name in args_values
                   and (arg.name not in self.current_discriminator_value
                        or self.current_discriminator_value[arg.name] != args_values[arg.name])]):
                self.get_command_args(command, command_input=tokens)

                discriminator_args = [arg.name for arg in self.cmd_args if arg.is_discriminator]
                for arg in discriminator_args:
                    discriminator_value = args_values[arg] if arg in args_values else None
                    self.current_discriminator_value[arg] = discriminator_value

            # [(arg.name, arg.is_discriminator) for arg in self.cmd_args]

            prev_token = split_tokens[-2] if curr_key else split_tokens[-1]
            prev_arg = [arg for arg in self.cmd_args if arg.name == prev_token]

            # if the previous option is a valid option and is not a flag/secret
            # option then complete the option value if possible
            if (prev_arg and prev_arg[0].nargs != '?'
                    or prev_token in ['+formatter', '+loglevel']):

                if (prev_arg and (prev_arg[0].arg_action == BoolAction
                                  or prev_arg[0].arg_action == BoolAppendAction)):
                    choices = [ArgumentChoice('true', 'true', ''), ArgumentChoice('false', 'false', '')]
                elif prev_arg:
                    choices = prev_arg[0].choices
                elif prev_token == '+formatter':
                    choices = [ArgumentChoice(formatter[0], formatter[0], formatter[1]) for formatter in CliOptions.FORMATTERS]
                elif prev_token == '+loglevel':
                    choices = [ArgumentChoice(log_level, log_level, '') for log_level in CliOptions.LOGLEVELS]

                if choices:
                    choices = sorted(choices, key=lambda x: x.display)
                    if curr_key:
                        match_dict = OrderedDict([(choice.value, choice) for choice in choices
                                                  if choice.value.startswith(curr_key)])
                    else:
                        match_dict = OrderedDict([(choice.value, choice) for choice in choices])
            else:
                # If it's not an option value then give find the list of possible options
                # for this command - after removing already entered options on prompt
                # and those who depend on other option(s) which are not yet entered
                temp_list = []
                if command != self.current_cmd:
                    if curr_key:
                        temp_list = [(arg.name, arg.description, not arg.required) for arg in self.cmd_args
                                     if arg.name.startswith(curr_key)]
                    else:
                        temp_list = [(arg.name, arg.description, not arg.required) for arg in self.cmd_args]
                else:
                    args_values = CliHelper.get_args_values(tokens)
                    if curr_key:
                        temp_list = [(arg.name, arg.description, not arg.required) for arg in self.cmd_args
                                     if (PypromptCompleter.should_show_option(arg, tokens, args_values)
                                         and arg.name.startswith(curr_key))]
                    else:
                        temp_list = [(arg.name, arg.description, not arg.required) for arg in self.cmd_args
                                     if PypromptCompleter.should_show_option(arg, tokens, args_values)]

                # Return sorted list of command matches
                match_dict = OrderedDict((option[0], ArgumentChoice(option[0], option[0], option[1])) for option in PypromptCompleter.sort_options(temp_list))

            return match_dict

        @staticmethod
        def should_show_option(arg, tokens, args_values):
            """
            Verifies whether to show specific option based
            on its depends_on property
            """
            result = True
            if arg.depends_on:
                result = bool(
                    arg.depends_on[0] in args_values
                    and (not arg.depends_on[1]
                         or args_values[arg.depends_on[0]] in arg.depends_on[1])
                )

            if result and \
                    (tokens.find(' {} '.format(arg.name)) == -1
                     or arg.arg_action in ('append', BoolAppendAction)):
                return True
            return False

        def get_unhandled_completions(self, document):
            """
            Return possible auto completion value
            """
            location = 0
            match_dict = OrderedDict()
            tokens = document.text_before_cursor
            search_text = tokens.replace(' ', '.')
            begin, _ = document.find_boundaries_of_current_word(WORD=True)

            # This is not the first word on the prompt
            if search_text.find('.') != -1:  # pylint: disable=too-many-nested-blocks
                word_index = len(
                    search_text) + begin  # begin gives negative index from current position

                # Get the previous and current tokens on the command line.
                root_key = search_text[:word_index].rstrip('--').rstrip('.')
                if root_key:  # root_key should not be empty
                    curr_key = search_text[word_index:]
                    self.prepare_autocomplete_map(root_key)

                    # If there's no current token text, start of a fresh token
                    if not curr_key:
                        commands = []
                        # Try to find a match for prev tokens in cmd map
                        for cmd in six.iterkeys(self.cli_main.cmd_map):
                            if root_key in cmd:
                                split_match = cmd.split(root_key)[-1]
                                if split_match and not split_match.startswith('.'):
                                    continue
                                temp_match = split_match.lstrip('.').split('.')[0]
                                if temp_match:
                                    commands.append((temp_match,
                                                     self.cli_main.ns_cmd_info.get(cmd, ('', True))))
                                else:
                                    commands += \
                                        [(i_cmd, self.cli_main.ns_cmd_info.get('%s.%s' % (cmd, i_cmd), ('', True)))
                                         for i_cmd in self.cli_main.cmd_map[cmd]]

                        if commands:
                            match_dict = OrderedDict(
                                (cmd, ArgumentChoice(cmd, cmd, descr[0], represents_namespace=descr[1])) for cmd, descr in commands)
                        else:
                            # If no match found check if it's a command and return options
                            match_dict = self.complete_pyprompt_command_options(
                                tokens, root_key, curr_key)
                    else:
                        # Special check to auto-complete '+' options
                        if curr_key.startswith('+'):
                            match_dict = PypromptCompleter.get_dcli_options(
                                curr_key)
                        else:
                            commands = []
                            for cmd in six.iterkeys(self.cli_main.cmd_map):
                                if root_key in cmd:
                                    temp_match = \
                                        cmd.split(root_key)[-1].lstrip('.').split('.')[0]
                                    if temp_match:
                                        # cmd has child namespace
                                        commands.append((temp_match,
                                                         self.cli_main.ns_cmd_info.get(
                                                             cmd, ('', True))))
                                    else:
                                        # cmd has child commands
                                        commands += \
                                            [(i_cmd, self.cli_main.ns_cmd_info.get('%s.%s' % (cmd, i_cmd), ('', True)))
                                             for i_cmd in self.cli_main.cmd_map[cmd]]
                            if commands:
                                match_dict = OrderedDict(
                                    (cmd, ArgumentChoice(cmd, cmd, descr[0], represents_namespace=descr[1])) for cmd, descr in commands if
                                    cmd.startswith(curr_key))
                            else:
                                # If no match found check if it's a command and return options
                                match_dict = self.complete_pyprompt_command_options(
                                    tokens, root_key, curr_key)
            else:
                # First word on the prompt
                if not search_text:
                    # First tab on the prompt (no text present)
                    match_dict = OrderedDict(
                        (cmd, ArgumentChoice(cmd,
                                             cmd,
                                             self.cli_main.ns_cmd_info[dot_cmd][0],
                                             represents_namespace=self.cli_main.ns_cmd_info[cmd][1]))
                        for cmd, dot_cmd in [(cmd.replace('.', ' '), cmd)
                                             for cmd in six.iterkeys(self.cli_main.cmd_map)
                                             if cmd == DCLI_SKIP_PREFIX])
                elif search_text.startswith('+'):
                    # Special check to auto-complete '+' options
                    match_dict = PypromptCompleter.get_dcli_options(search_text)
                else:
                    match_dict = OrderedDict((path, ArgumentChoice(path, path, ns_cmd_info[0], represents_namespace=ns_cmd_info[1]))
                                             for cmd, ns_cmd_info in [(cmd, self.cli_main.ns_cmd_info.get(cmd, ('', True)))
                                                                      for cmd in six.iterkeys(self.cli_main.cmd_map)
                                                                      if search_text in cmd]
                                             for path in cmd.split('.')
                                             if path.startswith(search_text))

                    for key, value in DCLI_COMMANDS.items():
                        if key.startswith(search_text):
                            match_dict[key] = ArgumentChoice(key, key, value)

            # Calculate where to insert found match on the prompt
            if tokens and tokens[-1] == ' ':
                location = 0
            elif tokens:
                word_before_cursor = tokens.strip().split()[-1]
                location = -len(word_before_cursor)

            if not match_dict:
                # If no match found, put start_position as 0 to
                # put dropdown directly to cursor position
                key = ''
                display = ''
                display_meta = ''

                yield Completion(key, start_position=0, display=display,
                                 display_meta=display_meta)
            else:
                for key, value in match_dict.items():
                    display = value.display
                    description = value.description
                    style = ''

                    if value.represents_namespace:
                        # if namespace put '> ' infront
                        display = '> %s' % key
                    else:
                        # if command bold the text
                        style = 'bold'
                    if key.startswith('--'):
                        style = 'class:pygments.name.tag'
                    elif key.startswith('+'):
                        style = 'class:pygments.literal.string.doc'

                    if six.PY2:
                        key = key.decode() if key is not None else None
                        display = display.decode() if display is not None else None
                        description = description.decode() if description is not None else None

                    yield Completion(key,
                                     start_position=location,
                                     display=display,
                                     display_meta=description,
                                     style=style)


class CliShell(object):
    """
    Class to open and manage a CLI shell
    """
    def __init__(self, cli_main, prompt=CliOptions.PROMPT_DEFAULT_VALUE):
        """
        CLI shell class init method

        """
        self.prompt_msg = prompt
        self.cli_main = cli_main
        if have_pyprompt:
            self.completer = PypromptCompleter(self.cli_main)
            self.prompt_session = PromptSession(history=self.completer.history)
        else:
            self.completer = None
            self.prompt_session = None

    def get_shell_parser(self):
        """
        Initializes and returns shells' argparse parser

        :rtype:  :class:`CliArgParser`
        :return: CliArgParser object
        """
        parser = CliHelper.get_parser(True)

        # show top level help for one of the available connections
        # doesn't make sense to 'spam' with all
        server_type = None
        if self.cli_main.connections:
            server_type = self.cli_main.connections[0].server_type
        print_top_level_help(True, server_type)

        return parser

    @staticmethod
    def get_cli_style():
        """
        Returns prompt_toolkit style object based on options set.

        :rtype:  :class:`prompt_toolkit.styles.Style`
        :return: Style object
        """
        if not CliOptions.DCLI_COLORS_ENABLED or not CliOptions.DCLI_COLORED_INPUT:
            return None

        pygments_style = get_style_by_name(CliOptions.DCLI_COLOR_THEME)
        default_pygments_style = style_from_pygments_cls(pygments_style)

        def get_color(color, if_missing_color=None):
            """
            Helper function to parse color correctly from pygments color
            """
            if '#' not in color:
                return if_missing_color
            elif color.index('#') != 0:
                try:
                    import re
                    color_value = re.search(r'\s(#.{6})', color).group(1)
                    color = re.sub(r'\s#.{6}', '', color)
                    color = '{} '.format(color_value) + color
                except Exception:
                    return if_missing_color
            return color

        font_color = get_color(pygments_style.styles[Text])
        font_color_selected = get_color(pygments_style.styles[Text])
        font_color_meta = get_color(pygments_style.styles[Comment])
        completion_color_selected = get_color(pygments_style.highlight_color)
        completion_color = get_color(pygments_style.background_color)
        meta_color = get_color(pygments_style.background_color)
        meta_color_selected = get_color(pygments_style.highlight_color)
        progress_background_color = get_color(pygments_style.styles[Comment])
        progress_btn_color = get_color(pygments_style.styles[Text])

        drop_down_styles = []
        if font_color and completion_color:
            drop_down_styles.append(('completion-menu.completion', 'bg:%s fg:%s' % (completion_color, font_color)))
        if completion_color_selected and font_color_selected:
            drop_down_styles.append(('completion-menu.completion.current', 'bg:%s fg:%s bold' % (completion_color_selected, font_color_selected)))
        if meta_color and font_color_meta:
            drop_down_styles.append(('completion-menu.meta.completion', 'bg:%s fg:%s italic' % (meta_color, font_color_meta)))
        if meta_color_selected and font_color:
            drop_down_styles.append(('completion-menu.meta.completion.current', 'bg:%s fg:%s italic' % (meta_color_selected, font_color)))
        if progress_background_color:
            drop_down_styles.append(('scrollbar.background', 'bg:%s' % progress_background_color))
        if progress_btn_color:
            drop_down_styles.append(('scrollbar.button', 'bg:%s' % progress_btn_color))

        return merge_styles([
            Style(drop_down_styles),
            default_pygments_style,
        ])

    def execute_vapi_command(self, parser, command, fp=sys.stdout):
        """
        Method to execute vapi command

        :type  parser: :class:`CliArgParser`
        :param parser: CliArgParser class instance
        :type  command: :class:`str`
        :param command: vAPI command to execute
        :type  fp: :class:`File`
        :param fp: Output file stream
        """
        exp_command = self.completer.expand_short_command(command, True)
        split_cmd = None

        # For interactive mode we have to do quote handling
        # Use shlex for POSIX while for windows do manually
        if os.name == 'nt':
            split_cmd = CliHelper.get_cli_args(exp_command)
        else:
            if six.PY2:
                tmp_cmd = shlex.split(exp_command.encode('utf-8'))
                split_cmd = [c.decode('utf-8') for c in tmp_cmd]
            else:
                split_cmd = shlex.split(exp_command)

        return self.cli_main.process_input(split_cmd, parser, fp=fp)

    def run_shell(self, first_command=None, fp=sys.stdout):
        """
        Method to display CLI shell and process commands

        """
        parser = self.get_shell_parser()
        status = StatusCode.SUCCESS

        while True:
            if not first_command:
                try:
                    command = self.get_command()
                except EOFError as e:
                    error_msg = 'Exiting %s shell' % CliOptions.CLI_CLIENT_NAME
                    handle_error(error_msg, exception=e)
                    return status
                except KeyboardInterrupt:
                    print_dcli_text()
                    continue
            else:
                command = first_command
                first_command = None
                print_dcli_text()  # breaker line between first command and welcome message
            self.cli_main.current_dcli_command = command

            if not command:
                continue
            elif command.split()[0].lower() in DCLI_COMMANDS:
                if command.rstrip().lower() == 'exit':
                    for connection in self.cli_main.connections:
                        if connection.server_type == ServerTypes.VSPHERE \
                                and connection.session_id is not None:
                            calculate_time(connection.session_logout, 'session logout time')
                            connection.session_id = None
                        elif connection.server_type == ServerTypes.VMC:
                            connection.csp_token = None
                    return status
                else:
                    status = calculate_time(lambda: self.completer.call_shell_commands(command.rstrip()),
                                            'shell command execution time',
                                            self.cli_main.current_dcli_command)
            else:
                try:
                    status = calculate_time(lambda: self.execute_vapi_command(parser, command, fp=fp),
                                            'full command execution time',
                                            self.cli_main.current_dcli_command)
                except CommandCollision as e:
                    pass
                except KeyboardInterrupt as e:
                    status = StatusCode.INVALID_COMMAND
                    error_msg = 'Execution of command "%s" interrupted' % command
                    handle_error(error_msg, exception=e)
                except CliArgumentException as e:
                    status = e.status_code
                    if e.print_error:
                        handle_error(e.msg, exception=e)
                except Exception as e:
                    status = StatusCode.INVALID_COMMAND
                    error_msg = 'Error executing command "%s"' % command
                    handle_error(error_msg)
                    msg = extract_error_msg(e)
                    if msg:
                        handle_error(msg, exception=e)

            if self.should_exit_shell():
                break

        return status

    def get_command(self):
        """
        Gets command string
        Note: Used to be patched by testing infrastructure

        :return: command string
        :rtype: :class:`str`
        """
        if self.prompt_session:
            style = CliShell.get_cli_style()
            if CliOptions.DCLI_COLORS_ENABLED and CliOptions.DCLI_COLORED_INPUT:
                prompt_msg = [('class:pygments.name.function bold', self.prompt_msg)]

                from vmware.vapi.client.dcli.style import DcliInputLexer
                lexer = PygmentsLexer(DcliInputLexer)
            else:
                prompt_msg = self.prompt_msg
                lexer = None

            return self.prompt_session.prompt(prompt_msg,
                                              completer=self.completer,
                                              complete_while_typing=True,
                                              auto_suggest=AutoSuggestFromHistory(),
                                              style=style,
                                              include_default_pygments_style=False,
                                              lexer=lexer)

        try:
            # For Python 3 compatibility
            input_func = raw_input  # pylint: disable=W0622
        except NameError:
            input_func = input
        return input_func('{}'.format(self.prompt_msg))

    def should_exit_shell(self):  # pylint: disable=R0201
        """
        Checks whether to exit shell mode
        Note: Used to be patched by testing infrastructure

        :return: whether to exit shell mode
        :rtype: :class:`bool`
        """
        return False
