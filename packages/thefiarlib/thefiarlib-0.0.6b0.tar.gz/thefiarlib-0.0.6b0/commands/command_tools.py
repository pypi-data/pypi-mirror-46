import click
import os

from config import settings
from library.commands.command_base import BaseCommand, SameCommandException


def my_import(name):
    components = name.split('.')
    command_file_name = components[-2:1]
    # print('.'.join(components[:-1]))
    mod = __import__('.'.join(components[:-1]), fromlist=(command_file_name,))
    # print(mod)
    if hasattr(mod, 'Command'):
        mod = getattr(mod, 'Command')
    else:
        mod = None
    return mod


def check_is_command(import_path):
    # print('importing')
    # print(import_path)
    klass = my_import(import_path)
    if klass:
        return issubclass(klass, BaseCommand), klass
    else:
        return False, None


def iter_classes():
    register_apps = settings.REGISTER_APPS
    for app_import in register_apps:
        app_path = app_import.replace('.', '/')
        dir_folder_path = os.path.join(app_path, 'commands')
        for filename in os.listdir(dir_folder_path):
            if filename.endswith('.py'):
                command_name = filename[:-3]
                current_class_import_path = '.'.join([app_import, 'commands', command_name, 'Command'])
                is_checked, class_cls = check_is_command(current_class_import_path)
                yield is_checked, class_cls, command_name, app_import


class TfCLI(click.MultiCommand):

    def list_commands(self, ctx):
        commands_list = []
        for is_checked, class_cls, command_name, _ in iter_classes():
            if is_checked:
                if command_name in commands_list:
                    raise SameCommandException(command_name)
                commands_list.append(command_name)

        commands_list.sort()
        return commands_list

    def get_command(self, ctx, name):
        for is_checked, class_cls, command_name, app_import in iter_classes():
            if is_checked and command_name == name:
                command = class_cls()
                command.set_app_name(app_import)
                return command

        return None


cli = TfCLI(help='load commands')
