import platform
import subprocess


def exec_command(command: str) -> bool:
    ''' Execute system command '''
    match platform.system():
        case 'Linux':
            match command:
                case 'shutdown':
                    subprocess.run(['sudo', 'shutdown', 'now'], check=False)
                case 'reboot':
                    subprocess.run(
                        ['sudo', 'shutdown', '-r', 'now'], check=False)
                case _:
                    return False
        case 'Windows':
            match command:
                case 'shutdown':
                    subprocess.run(['shutdown', '/s', '/t', '0'], check=False)
                case 'reboot':
                    subprocess.run(['shutdown', '/r', '/t', '0'], check=False)
                case _:
                    return False
    return True
