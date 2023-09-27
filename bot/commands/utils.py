from .enums import CommandsEnum


def get_commands_array():
    commands = []
    for command in CommandsEnum:
        if command.value:
            commands.append(command.value)

    return commands
