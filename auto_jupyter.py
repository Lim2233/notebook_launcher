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
        return True
    except subprocess.CalledProcessError as e:
        error_msg = f"安装 Jupyter Notebook 失败: {str(e)}"
        print(error_msg)
        return False, error_msg

def launch_jupyter(target_dir):
    """在目标目录的虚拟环境中启动 Jupyter，返回 (成功标志, 地址或错误信息)"""
    if not os.path.isdir(target_dir):
        return False, f"目录不存在: {target_dir}"

    # 查找已存在的虚拟环境
    python_path, venv_name = find_venv(target_dir)
    
    if not python_path:
        return False, "未找到虚拟环境"

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
        return False, f"启动 Jupyter Notebook 失败: {str(e)}"

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
        return True, url
    else:
        # 超时或进程退出，终止子进程
        process.terminate()
        return False, "未能获取 Jupyter Notebook 的访问地址（可能启动超时或未安装 notebook）"

def main():
    # 检查是否需要重启
    if len(sys.argv) > 1 and sys.argv[1] == "--restart":
        # 重启模式，跳过环境检查
        target_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DIR
    else:
        # 正常模式
        target_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR

    print(f"目标目录: {target_dir}")

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
    success, result = launch_jupyter(target_dir)
    if success:
        print(f"Jupyter Notebook 已启动，正在用默认浏览器打开...")
        # 使用默认浏览器打开 URL
        webbrowser.open(result)
        print("完成！请勿关闭此窗口，如需停止 Jupyter 请手动结束进程。")
        input("按 Enter 键退出脚本，Jupyter 将继续在后台运行...")
    else:
        print(f"错误: {result}")
        input("按 Enter 键退出...")
        sys.exit(1)

if __name__ == '__main__':
    main()