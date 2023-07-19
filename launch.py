#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2021-10-28 21:18:12
# Description: launcher

import os
import platform
import sys
from pathlib import Path
from subprocess import PIPE, run

root_dir = Path(__file__).resolve().parent
core_dir = root_dir / 'core'
sys.path.append(str(core_dir))


def get_venv_path():
    venv_dir = root_dir / '.venv'

    os_platform = platform.system()
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


def start():
    os.chdir(root_dir)
    _, venv_python_path, venv_pip_path = get_venv_path()

    if Path(sys.executable) != venv_python_path:
        run(f'{venv_python_path} {__file__}', shell=True)
        sys.exit()

    try:
        from main import main
        main()

    except ModuleNotFoundError:
        set_pip(venv_pip_path, venv_python_path)
        run(f'{venv_pip_path} install -r requirements.txt',
            shell=True,
            stdout=PIPE)

        from main import main
        main()


if __name__ == '__main__':
    start()
