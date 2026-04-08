#!/usr/bin/env python3
import os, sys, re, subprocess, time, webbrowser, signal, atexit

# ==================== 配置区域 ====================
DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))
JUPYTER_TIMEOUT = 15
PIP_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
# =================================================

def get_venv_python(target_dir):
    """获取虚拟环境 Python 路径，不存在则创建"""
    for name in ['venv', 'env', '.venv']:
        path = os.path.join(target_dir, name, 'Scripts' if os.name == 'nt' else 'bin', 'python' + ('.exe' if os.name == 'nt' else ''))
        if os.path.exists(path): return path
    
    print("正在创建虚拟环境...")
    venv_path = os.path.join(target_dir, 'venv')
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    return os.path.join(venv_path, 'Scripts' if os.name == 'nt' else 'bin', 'python' + ('.exe' if os.name == 'nt' else ''))

def run_and_manage_jupyter(python_path, target_dir):
    """启动 Jupyter 并处理生命周期"""
    # 设置环境变量以解决Python 3.13兼容性问题
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['LANG'] = 'en_US.UTF-8'
    
    cmd = [python_path, '-m', 'notebook', '--no-browser']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore', cwd=target_dir, bufsize=1, env=env)

    def cleanup():
        if process.poll() is None:
            process.terminate()
            process.wait()
    
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    timeout = time.time() + JUPYTER_TIMEOUT
    while time.time() < timeout:
        line = process.stdout.readline()
        if not line and process.poll() is not None: break
        print(line, end='')
        match = re.search(r'(http://(?:localhost|127\.0\.0\.1):\d+/[^\s]*\?token=[a-f0-9]+)', line)
        if match:
            url = match.group(1)
            print(f"\n成功！正在打开浏览器: {url}")
            webbrowser.open(url)
            print("提示：按 Ctrl+C 或关闭此窗口可停止 Jupyter。")
            # 继续运行，不再等待用户输入
            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    print(line, end='')
            return
    
    process.terminate()
    print("\n错误：启动超时或获取地址失败。")

def main():
    target_dir = os.path.abspath(sys.argv[2] if "--restart" in sys.argv else (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR))
    
    # 1. 环境准备
    python_path = get_venv_python(target_dir)
    
    # 2. 依赖检查
    try:
        subprocess.run([python_path, '-c', 'import notebook'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("正在安装 Jupyter Notebook...")
        subprocess.run([python_path, '-m', 'pip', 'install', '-i', PIP_MIRROR, 'notebook'], check=True)
    
    # 3. 递归重启（可选，若想保持环境纯净）或直接运行
    if "--restart" not in sys.argv:
        os.execv(sys.executable, [sys.executable, __file__, "--restart", target_dir])
    else:
        run_and_manage_jupyter(python_path, target_dir)

if __name__ == '__main__':
    main()