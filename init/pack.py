#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import argparse
import contextlib
import errno
import os
import platform
import shutil
import stat
from pathlib import Path
from subprocess import PIPE, run
from zipfile import ZipFile

os_platform = platform.system()
root_dir = Path(__file__).resolve().parents[1]


def get_venv_path():
    venv_dir = root_dir / '.venv'

    if os_platform == 'Windows':
        python_str = 'python'
        python_path = venv_dir / 'scripts' / 'python.exe'
        pip_path = venv_dir / 'scripts' / 'pip.exe'

    elif os_platform == 'Linux':
        python_str = 'python3'
        python_path = venv_dir / 'bin' / 'python3'
        pip_path = venv_dir / 'bin' / 'pip3'

    else:
        raise EnvironmentError('unsupported platform!')

    return python_str, python_path, pip_path


def set_pip(pip_path, python_path):
    cmd_list = [
        f'{pip_path} config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/',
        f'{pip_path} config set global.trusted-host pypi.tuna.tsinghua.edu.cn',
        f'{pip_path} config set global.timeout 6000',
        f'{python_path} -m pip install -U pip'
    ]

    [run(cmd, shell=True, stdout=PIPE, stderr=PIPE) for cmd in cmd_list]


def arg_parse():
    parser = argparse.ArgumentParser(prog='pack',
                                     description='packaging python files')
    parser.add_argument('--type',
                        choices=('zip', 'exe'),
                        metavar='zip|exe',
                        default='zip',
                        help='select type, default: zip')
    parser.add_argument('--use',
                        choices=('nuitka', 'pyinstaller'),
                        metavar='nuitka|pyinstaller',
                        default='pyinstaller',
                        help='select tool, default: pyinstaller')
    parser.add_argument('--mode',
                        choices=('typical', 'custom'),
                        metavar='typical|custom',
                        default='typical',
                        help='select mode, default: typical')
    parser.add_argument('--extra',
                        metavar='',
                        default='',
                        help='extra option, default: None')

    return parser.parse_args()


def is_empty(folder):
    for _ in folder.iterdir():
        return False
    return True


def pack_zip(_root_dir, output_dir):
    """package _root_dir as zip file, save to output_dir"""

    include_dirs = (_root_dir / 'bin', _root_dir / 'conf', _root_dir / 'core',
                    _root_dir / 'docs', _root_dir / 'init', _root_dir / 'res')
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / f'{_root_dir.name}.zip'
    if zip_path.exists():
        zip_path.unlink()

    with ZipFile(zip_path, 'w') as z_file:
        for file in _root_dir.iterdir():
            if file.is_dir() and not is_empty(
                    file
            ) and file in include_dirs and file.name != '__pycache__':
                for sub_file in file.rglob('*'):
                    if file.parent.name != '__pycache__':
                        z_file.write(sub_file, sub_file.relative_to(_root_dir))
            if file.is_file() and file.parent.name != '__pycache__':
                z_file.write(file, file.relative_to(_root_dir))


def pack_exe(_root_dir, output_dir, pack_cmd):
    """use Nuitka or Pyinstaller package _root_dir as exe file, save to output_dir"""

    def _onerror(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove,
                    os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            func(path)
        else:
            raise

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(output_dir, onerror=_onerror)
    output_dir.mkdir(parents=True, exist_ok=True)

    include_dirs = (_root_dir / 'bin', _root_dir / 'conf', _root_dir / 'res')
    for _dir in include_dirs:
        if _dir.exists() and not is_empty(_dir):
            shutil.copytree(_dir, output_dir / _dir.name)

    run(pack_cmd, shell=True)

    for _dir in output_dir.iterdir():
        if '.dist' in _dir.name:
            new_name = _dir.name.replace('.dist', '')
            new_path = _dir.with_name(new_name)
            os.rename(_dir, new_path)

        if _dir.is_dir() and _dir.name == 'main':
            for _d in _dir.iterdir():
                if _d.is_dir() and _d.suffix == '.dist-info':
                    shutil.rmtree(_d)

    shutil.rmtree(_root_dir / 'build', ignore_errors=True)
    with contextlib.suppress(Exception):
        os.remove(_root_dir / 'main.spec')


def pack_use_nuitka(pip_path, pack_mode, extra_option):
    run(f'{pip_path} install -U Nuitka orderedset zstandard',
        shell=True,
        stdout=PIPE,
        stderr=PIPE)
    if pack_mode == 'typical':
        standalone = '--standalone'
        output_dir = Path('output', root_dir.name)
        remove_output = '--remove-output'
        windows_disable_console = '--windows-disable-console'
        windows_icon = Path('res', 'main_256.ico')
        plugin_enable = 'tk-inter'
        target_file = Path('core', 'main.py')
    else:
        standalone = ''
        output_dir = ''
        remove_output = ''
        windows_disable_console = ''
        windows_icon = ''
        plugin_enable = ''
        target_file = ''

    upx_binary = root_dir / 'init' / 'upx' / 'upx.exe'
    if os_platform == 'Windows' and upx_binary.exists():
        pack_cmd = 'nuitka ' \
                   f'{standalone} ' \
                   f'--output-dir={output_dir} ' \
                   f'{remove_output} ' \
                   f'{windows_disable_console} ' \
                   f'--windows-icon-from-ico={windows_icon} ' \
                   f'--plugin-enable=upx --upx-binary={upx_binary} ' \
                   f'--plugin-enable={plugin_enable} ' \
                   f'{extra_option} ' \
                   f'{target_file}'
    else:
        pack_cmd = 'nuitka ' \
                   f'{standalone} ' \
                   f'--output-dir={output_dir} ' \
                   f'{remove_output} ' \
                   f'{windows_disable_console} ' \
                   f'--windows-icon-from-ico={windows_icon} ' \
                   f'--plugin-enable={plugin_enable} ' \
                   f'{extra_option} ' \
                   f'{target_file}'

    pack_cmd = pack_cmd.replace('  ', ' ')
    pack_exe(root_dir, output_dir, pack_cmd)

    return output_dir


def pack_use_pyinstaller(pip_path, pack_mode, extra_option):
    run(f'{pip_path} install -U pyinstaller',
        shell=True,
        stdout=PIPE,
        stderr=PIPE)
    if pack_mode == 'typical':
        output_dir = Path('output', root_dir.name)
        windows_disable_console = '--windowed'
        windows_icon = Path('res', 'main_256.ico')
        target_file = Path('core', 'main.py')
    else:
        output_dir = ''
        windows_disable_console = ''
        windows_icon = ''
        target_file = ''

    upx_binary = root_dir / 'init' / 'upx' / 'upx.exe'
    if os_platform == 'Windows' and upx_binary.exists():
        pack_cmd = 'pyinstaller ' \
                   f'--distpath={output_dir} ' \
                   f'{windows_disable_console} ' \
                   f'--icon={windows_icon} ' \
                   f'--upx-dir={upx_binary.parent} ' \
                   f'{extra_option} ' \
                   f'{target_file}'
    else:
        pack_cmd = 'pyinstaller ' \
                   f'--distpath={output_dir} ' \
                   f'{windows_disable_console} ' \
                   f'--icon={windows_icon} ' \
                   f'{extra_option} ' \
                   f'{target_file}'

    pack_cmd = pack_cmd.replace('  ', ' ')
    print(pack_cmd)
    pack_exe(root_dir, output_dir, pack_cmd)

    return output_dir


def main():
    os.chdir(root_dir)
    _, venv_python_path, venv_pip_path = get_venv_path()
    set_pip(venv_pip_path, venv_python_path)

    exclude_modules = [
        'altgraph', 'black', 'future', 'importlib-metadata', 'Nuitka',
        'orderedset', 'order-set', 'pefile', 'pyinstaller',
        'pyinstaller-hooks-contrib', 'pywin32-ctypes', 'typing_extensions',
        'yapf', 'zipp', 'zstandard'
    ]
    exclude_string = ' --exclude '.join(exclude_modules)
    run(f'{venv_pip_path} freeze --exclude {exclude_string} >requirements.txt',
        shell=True,
        stdout=PIPE,
        stdin=PIPE)

    args = arg_parse()
    pack_type = args.type
    extra_option = args.extra

    if pack_type == 'zip':
        output_dir = root_dir / 'output'
        pack_zip(root_dir, output_dir)
    else:
        pack_use = args.use
        pack_mode = args.mode
        if pack_use == 'nuitka':
            output_dir = pack_use_nuitka(venv_pip_path, pack_mode,
                                         extra_option)

        else:
            output_dir = pack_use_pyinstaller(venv_pip_path, pack_mode,
                                              extra_option)

    if os_platform == 'Windows':
        run(f'explorer {output_dir}', shell=True, stdout=PIPE, stderr=PIPE)


if __name__ == '__main__':
    main()
