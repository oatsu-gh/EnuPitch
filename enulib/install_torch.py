#!/usr/bin/env python3
# Copyright (c) 2021-2023 oatsu
"""
CUDAの有無やバージョンを調べる

## CUDA 11.0 環境がある場合

nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2020 NVIDIA Corporation
Built on Wed_Jul_22_19:09:35_Pacific_Daylight_Time_2020
Cuda compilation tools, release 11.0, V11.0.221
Build cuda_11.0_bu.relgpu_drvr445TC445_37.28845127_0

## 環境がない場合

nvcc : 用語 'nvcc' は、コマンドレット、関数、スクリプト ファイル、または操作可能なプログラムの名前として認識されません。
名前が正しく記述されていることを確認し、パスが含まれている場合はそのパスが正しいことを確認してから、再試行してください。
発生場所 行:1 文字:1
+ nvcc -V
+ ~~~~
    + CategoryInfo          : ObjectNotFound: (nvcc:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

"""

import subprocess
import sys
from os.path import abspath

PYTORCH_STABLE_URL = 'https://download.pytorch.org/whl/torch_stable.html'
PYTORCH_PACKAGES_DICT = {
    # CUDA 11
    'release 11.': r'torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --extra-index-url https://download.pytorch.org/whl/cu118',
    # CUDA 10
    'release 10.': r'torch==1.10.1+cu102 torchvision==0.11.2+cu102 torchaudio==0.10.1 --extra-index-url https://download.pytorch.org/whl/cu102',
    # no CUDA
    'cpu': r'torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1'
}


def nvcc_v() -> str:
    """
    nvcc -V
    """
    proc = subprocess.run(['nvcc', '-V'], check=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    result = proc.stdout.decode('utf-8')
    return result


def get_pytorch_package_list(nvcc_v_result: str) -> list:
    """
    CUDAのバージョン情報を返す。
    """
    for key, value in PYTORCH_PACKAGES_DICT.items():
        if key in nvcc_v_result:
            return value
    return PYTORCH_PACKAGES_DICT['cpu']


def pip_install_torch(python_exe):
    """
    python.exe -m pip install torch torchaudio torchvision
    """
    # CUDAのインストール状況を調べて、対応するPyTorchのバージョンを取得
    try:
        pytorch_packages = get_pytorch_package_list(nvcc_v())
    # NVIDIA製GPU非搭載でnvccコマンドが見つからない場合はCPU向けパッケージを選択
    except FileNotFoundError:
        pytorch_packages = get_pytorch_package_list('cpu')
    # Pytorchをインストールする。
    command = [python_exe, '-m', 'pip', 'install',
               '--quiet'] + pytorch_packages.split()
    print('command:', command)
    subprocess.run(command, check=True)


def ltt_install_torch(python_exe):
    """
    python -m light_the_torch install torch torchaudio torchvision
    """
    # Upgrade pip and ltt
    command = [python_exe,
               '-m', 'pip', 'install', '--upgrade', 'light-the-torch',
               '--no-warn-script-location',
               '--disable-pip-version-check',
               ]
    subprocess.run(command, check=True)
    # Install pytorch
    command = [python_exe, '-m', 'light_the_torch', 'install',
               'torch', 'torchaudio', 'torchvision',
               '--no-warn-script-location',
               '--disable-pip-version-check',
               ]
    subprocess.run(command, check=True)


def main():
    """
    インストールを実行する
    """
    if input('インストールされているpytorchを上書きしてもいいですか？(YES/NO): ') == 'YES':
        ltt_install_torch(abspath(sys.executable))
    #    pip_install_torch(abspath(sys.executable))


if __name__ == '__main__':
    main()
