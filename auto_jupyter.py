#!/usr/bin/env python3
"""
自动激活或创建虚拟环境并启动 Jupyter Notebook，然后使用默认浏览器打开。
使用方法：直接运行此脚本，或通过命令行参数指定项目目录。
"""

import os
import sys
import re
import subprocess
import time
import webbrowser
import signal
import atexit

# ==================== 配置区域 ====================
DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))
JUPYTER_TIMEOUT = 15          # 等待 Jupyter 启动的最大秒数
PIP_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"  # 镜像源
# =================================================

def find_jupyter_url(line):
    """从 Jupyter 输出行中提取访问地址（支持 localhost 和 127.0.0.1，兼容 /tree?token= 等格式）"""
    # 匹配 http://localhost:端口/任意路径?token=...
    pattern = r'(http://(?:localhost|127\.0\.0\.1):\d+/[^\s]*\?token=[a-f0-9]+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None

def set_jupyter_language(python_path):
    """设置 Jupyter 的语言为中文"""
    print("正在设置 Jupyter 语言为中文...")
    try:
        # 创建或修改 jupyter 配置文件
        import json
        import os
        
        # 获取用户主目录
        home_dir = os.path.expanduser('~')
        jupyter_config_dir = os.path.join(home_dir, '.jupyter')
        os.makedirs(jupyter_config_dir, exist_ok=True)
        
        # 配置文件路径
        config_file = os.path.join(jupyter_config_dir, 'jupyter_notebook_config.json')
        
        # 读取现有配置
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}
        
        # 设置语言为中文
        config['NotebookApp'] = config.get('NotebookApp', {})
        # 正确的语言配置项是 'language' 而不是 'locale'
        config['NotebookApp']['language'] = 'zh_CN'
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("Jupyter 语言设置为中文成功")
        return True
    except Exception as e:
        print(f"设置 Jupyter 语言失败: {str(e)}")
        return False

def is_first_run(target_dir):
    """检查是否是首次运行"""
    # 创建一个标记文件来记录是否首次运行
    marker_file = os.path.join(target_dir, '.notebook_launcher_first_run')
    return not os.path.exists(marker_file)

def mark_first_run_completed(target_dir):
    """标记首次运行已完成"""
    marker_file = os.path.join(target_dir, '.notebook_launcher_first_run')
    with open(marker_file, 'w') as f:
        f.write('')

def create_start_folder_and_sample(target_dir):
    """创建 Start 文件夹和 hello.ipynb 文件"""
    print("正在创建 Start 文件夹和示例文件...")
    try:
        # 创建 Start 文件夹
        start_folder = os.path.join(target_dir, 'Start')
        os.makedirs(start_folder, exist_ok=True)
        
        # 创建 hello.ipynb 文件
        hello_ipynb = os.path.join(start_folder, 'hello.ipynb')
        
        # 生成 notebook 内容
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Hello World 示例\n",
                        "\n",
                        "这是一个 Jupyter Notebook 示例文件，包含 Markdown 和 Python 代码。\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 输出 Hello World\n",
                        "print('Hello, World!')"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## 变量示例\n",
                        "\n",
                        "下面是一个简单的变量示例："
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 定义变量\n",
                        "name = 'Jupyter'\n",
                        "print(f'Hello, {name}!')"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 2
        }
        
        # 写入文件
        import json
        with open(hello_ipynb, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2, ensure_ascii=False)
        
        print(f"Start 文件夹和 hello.ipynb 文件创建成功，路径：{hello_ipynb}")
        return True
    except Exception as e:
        print(f"创建 Start 文件夹和示例文件失败: {str(e)}")
        return False

def find_venv(target_dir):
    """查找目标目录中已存在的虚拟环境"""
    # 常见虚拟环境目录名称
    venv_names = ['venv', 'env', '.venv']
    
    for venv_name in venv_names:
        if os.name == 'nt':
            python_path = os.path.join(target_dir, venv_name, 'Scripts', 'python.exe')
        else:
            python_path = os.path.join(target_dir, venv_name, 'bin', 'python')
        
        if os.path.isfile(python_path):
            print(f"找到虚拟环境: {venv_name}")
            return python_path, venv_name
    
    return None, None

def create_venv(target_dir):
    """创建新的虚拟环境"""
    venv_name = 'venv'
    venv_path = os.path.join(target_dir, venv_name)
    
    print(f"正在创建虚拟环境: {venv_name}")
    
    # 使用系统 Python 创建虚拟环境
    cmd = [sys.executable, '-m', 'venv', venv_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("虚拟环境创建成功")
        
        # 获取新创建的虚拟环境 Python 路径
        if os.name == 'nt':
            python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:
            python_path = os.path.join(venv_path, 'bin', 'python')
        
        return python_path, venv_name
    except subprocess.CalledProcessError as e:
        return None, f"创建虚拟环境失败: {str(e)}"

def install_jupyter(python_path):
    """安装 Jupyter Notebook"""
    print("正在安装 Jupyter Notebook...")
    
    # 使用镜像源安装
    cmd = [python_path, '-m', 'pip', 'install', '-i', PIP_MIRROR, 'notebook']
    try:
        subprocess.run(cmd, check=True)
        print("Jupyter Notebook 安装成功")
        
        
        # 安装中文语言包
        print("正在安装 Jupyter 中文语言包...")
        try:
            subprocess.run([python_path, '-m', 'pip', 'install', 'jupyterlab-language-pack-zh-CN'], check=True)
            print("中文语言包安装成功")
        except subprocess.CalledProcessError:
            print("中文语言包安装失败（不影响Jupyter使用）")
        
        return True
    except subprocess.CalledProcessError as e:
        error_msg = f"安装 Jupyter Notebook 失败: {str(e)}"
        print(error_msg)
        return False, error_msg

def launch_jupyter(target_dir):
    """在目标目录的虚拟环境中启动 Jupyter，返回 (成功标志, 地址或错误信息, 进程对象)"""
    if not os.path.isdir(target_dir):
        return False, f"目录不存在: {target_dir}", None

    # 查找已存在的虚拟环境
    python_path, venv_name = find_venv(target_dir)
    
    if not python_path:
        return False, "未找到虚拟环境", None

    # 设置 Jupyter 语言为中文
    set_jupyter_language(python_path)

    # 启动 Jupyter Notebook（禁止自动打开浏览器）
    cmd = [python_path, '-m', 'notebook', '--no-browser']
    print(f"正在启动 Jupyter Notebook (目录: {target_dir}, 虚拟环境: {venv_name})...")
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=target_dir,
            bufsize=1
        )
    except Exception as e:
        return False, f"启动 Jupyter Notebook 失败: {str(e)}", None

    # 循环读取输出，寻找 URL
    url = None
    timeout = time.time() + JUPYTER_TIMEOUT
    while time.time() < timeout:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                break
            continue
        print(line, end='')   # 打印到控制台，便于调试
        url = find_jupyter_url(line)
        if url:
            print(f"\n成功获取访问地址: {url}")
            break

    if url:
        # 成功获取 URL，让 Jupyter 在后台继续运行
        return True, url, process
    else:
        # 超时或进程退出，终止子进程
        process.terminate()
        return False, "未能获取 Jupyter Notebook 的访问地址（可能启动超时或未安装 notebook）", None

def check_python_version():
    """检查 Python 版本是否为 3.12"""
    import platform
    version = platform.python_version_tuple()
    major, minor = int(version[0]), int(version[1])
    return major == 3 and minor == 12

def main():
    # 检查是否需要重启
    if len(sys.argv) > 1 and sys.argv[1] == "--restart":
        # 重启模式，跳过环境检查
        target_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DIR
        
        # 启动 Jupyter Notebook
        success, result, process = launch_jupyter(target_dir)
        if success:
            print(f"Jupyter Notebook 已启动，正在用默认浏览器打开...")
            # 使用默认浏览器打开 URL
            webbrowser.open(result)
            
            # 注册清理函数，确保脚本退出时终止 Jupyter 进程
            def cleanup():
                if process.poll() is None:
                    process.terminate()
                    process.wait()
            
            atexit.register(cleanup)
            
            # 处理信号，确保窗口关闭时也能清理
            def signal_handler(signum, frame):
                cleanup()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            print("完成！可以关闭此窗口，Jupyter 将在后台运行。")
            print("提示：关闭此窗口不会停止 Jupyter，请使用 Ctrl+C 或在浏览器中关闭。")
            input("按 Enter 键退出脚本...")
        else:
            print(f"错误: {result}")
            input("按 Enter 键退出...")
            sys.exit(1)
    else:
        # 正常模式
        target_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR

        print(f"目标目录: {target_dir}")

        # 检查 Python 版本
        if not check_python_version():
            print("当前 Python 版本不是 3.12，可能会导致兼容性问题...")
            print("建议使用 Python 3.12 以获得最佳兼容性")
            print("您可以从以下链接下载 Python 3.12.4:")
            print("https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe")
            print("\n正在继续执行...")

        # 检查是否首次运行，如果是则创建 Start 文件夹和示例文件
        if is_first_run(target_dir):
            create_start_folder_and_sample(target_dir)
            mark_first_run_completed(target_dir)

        # 标记是否创建了新环境或安装了Jupyter
        created_env = False
        installed_jupyter = False

        # 查找已存在的虚拟环境
        python_path, venv_name = find_venv(target_dir)
        
        # 如果没有找到虚拟环境，创建新的
        if not python_path:
            print("未找到虚拟环境，正在创建...")
            python_path, error = create_venv(target_dir)
            if not python_path:
                print(f"错误: {error}")
                input("按 Enter 键退出...")
                sys.exit(1)
            venv_name = 'venv'
            created_env = True
        
        # 检查 notebook 是否安装
        check_cmd = [python_path, '-c', 'import notebook']
        try:
            subprocess.run(check_cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError:
            # 未安装，尝试安装
            print("Jupyter Notebook 未安装，正在安装...")
            result = install_jupyter(python_path)
            if isinstance(result, tuple) and not result[0]:
                print(f"错误: {result[1]}")
                input("按 Enter 键退出...")
                sys.exit(1)
            elif not result:
                print("错误: 安装 Jupyter Notebook 失败")
                input("按 Enter 键退出...")
                sys.exit(1)
            installed_jupyter = True

        # 如果创建了新环境或安装了Jupyter，重启脚本
        if created_env or installed_jupyter:
            print("\n环境已准备就绪，正在重启脚本...")
            # 构建重启命令
            restart_cmd = [sys.executable, __file__, "--restart"]
            if len(sys.argv) > 1 and sys.argv[1] != "--restart":
                restart_cmd.append(sys.argv[1])
            # 执行重启
            try:
                subprocess.Popen(restart_cmd)
                print("脚本已重启，正在启动 Jupyter Notebook...")
                sys.exit(0)
            except Exception as e:
                print(f"重启脚本失败: {str(e)}")
                # 重启失败，继续执行
                # 启动 Jupyter Notebook
                success, result, process = launch_jupyter(target_dir)
                if success:
                    print(f"Jupyter Notebook 已启动，正在用默认浏览器打开...")
                    # 使用默认浏览器打开 URL
                    webbrowser.open(result)
                    
                    # 注册清理函数，确保脚本退出时终止 Jupyter 进程
                    def cleanup():
                        if process.poll() is None:
                            process.terminate()
                            process.wait()
                    
                    atexit.register(cleanup)
                    
                    # 处理信号，确保窗口关闭时也能清理
                    def signal_handler(signum, frame):
                        cleanup()
                        sys.exit(0)
                    
                    signal.signal(signal.SIGINT, signal_handler)
                    signal.signal(signal.SIGTERM, signal_handler)
                    
                    print("完成！可以关闭此窗口，Jupyter 将在后台运行。")
                    print("提示：关闭此窗口不会停止 Jupyter，请使用 Ctrl+C 或在浏览器中关闭。")
                    input("按 Enter 键退出脚本...")
                else:
                    print(f"错误: {result}")
                    input("按 Enter 键退出...")
                    sys.exit(1)
        else:
            # 启动 Jupyter Notebook
            success, result, process = launch_jupyter(target_dir)
            if success:
                print(f"Jupyter Notebook 已启动，正在用默认浏览器打开...")
                # 使用默认浏览器打开 URL
                webbrowser.open(result)
                
                # 注册清理函数，确保脚本退出时终止 Jupyter 进程
                def cleanup():
                    if process.poll() is None:
                        process.terminate()
                        process.wait()
                
                atexit.register(cleanup)
                
                # 处理信号，确保窗口关闭时也能清理
                def signal_handler(signum, frame):
                    cleanup()
                    sys.exit(0)
                
                signal.signal(signal.SIGINT, signal_handler)
                signal.signal(signal.SIGTERM, signal_handler)
                
                print("完成！可以关闭此窗口，Jupyter 将在后台运行。")
                print("提示：关闭此窗口不会停止 Jupyter，请使用 Ctrl+C 或在浏览器中关闭。")
                input("按 Enter 键退出脚本...")
            else:
                print(f"错误: {result}")
                input("按 Enter 键退出...")
                sys.exit(1)

if __name__ == '__main__':
    main()