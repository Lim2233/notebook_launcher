@echo off

REM 下载 Python 3.12.4 安装包
set PYTHON_URL=https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe
set PYTHON_EXE=python-3.12.4-amd64.exe

echo 正在下载 Python 3.12.4...
if not exist "%PYTHON_EXE%" (
    echo 请手动下载 Python 3.12.4 安装包：
    echo %PYTHON_URL%
    echo 下载完成后请放在当前目录并重新运行此脚本
    pause
    exit /b 1
)

echo 正在安装 Python 3.12.4...
start /wait "%PYTHON_EXE%" /passive InstallAllUsers=1 PrependPath=1

echo Python 3.12.4 安装完成
pause
