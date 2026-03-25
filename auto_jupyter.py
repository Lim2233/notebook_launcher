#!/usr/bin/env python3
"""
自动激活 venv 并启动 Jupyter Notebook，然后使用默认浏览器打开。
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
# =================================================

def find_jupyter_url(line):
    """从 Jupyter 输出行中提取访问地址（支持 localhost 和 127.0.0.1，兼容 /tree?token= 等格式）"""
    # 匹配 http://localhost:端口/任意路径?token=...
    pattern = r'(http://(?:localhost|127\.0\.0\.1):\d+/[^\s]*\?token=[a-f0-9]+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None

def launch_jupyter(target_dir):
    """在目标目录的 venv 中启动 Jupyter，返回 (成功标志, 地址或错误信息)"""
    if not os.path.isdir(target_dir):
        return False, f"目录不存在: {target_dir}"

    # 构建虚拟环境中的 Python 解释器路径
    if os.name == 'nt':
        python_path = os.path.join(target_dir, 'venv', 'Scripts', 'python.exe')
    else:
        python_path = os.path.join(target_dir, 'venv', 'bin', 'python')

    if not os.path.isfile(python_path):
        return False, f"未找到虚拟环境: {python_path}"

    # 检查 notebook 是否安装
    check_cmd = [python_path, '-c', 'import notebook']
    try:
        subprocess.run(check_cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False, "虚拟环境中未安装 Jupyter Notebook，请先执行：pip install notebook"

    # 启动 Jupyter Notebook（禁止自动打开浏览器）
    cmd = [python_path, '-m', 'notebook', '--no-browser']
    print(f"正在启动 Jupyter Notebook (目录: {target_dir})...")
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
    # 获取目标目录
    if len(sys.argv) > 1:
        target_dir = os.path.abspath(sys.argv[1])
    else:
        target_dir = DEFAULT_DIR

    print(f"目标目录: {target_dir}")

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