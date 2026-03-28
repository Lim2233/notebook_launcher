@echo off

REM 下载 Python 3.12.4 安装包
set PYTHON_URL=https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe
set PYTHON_EXE=python-3.12.4-amd64.exe

echo 正在下载 Python 3.12.4...
if not exist "%PYTHON_EXE%" (
    REM 使用 bitsadmin 下载，更可靠
    bitsadmin /transfer PythonDownload /download /priority foreground "%PYTHON_URL%" "%~dp0%PYTHON_EXE%"
)

echo 正在安装 Python 3.12.4...
start /wait "%PYTHON_EXE%" InstallAllUsers=1 PrependPath=1

echo Python 3.12.4 安装完成

REM 重新运行 auto_jupyter.py 脚本
echo 正在重新运行脚本...
REM 使用绝对路径运行 Python 3.12
"C:\Program Files\Python312\python.exe" "%~dp0auto_jupyter.py"
