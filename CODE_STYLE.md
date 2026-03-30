# 代码风格指南

## Python 代码规范

### 命名规范
- 函数和变量：使用小写字母和下划线，如 `find_venv`, `python_path`
- 常量：使用大写字母和下划线，如 `DEFAULT_DIR`, `JUPYTER_TIMEOUT`
- 类名：使用驼峰命名法，如 `JupyterLauncher`

### 代码格式
- 使用 4 个空格缩进
- 每行代码不超过 88 字符
- 函数之间空两行
- 类之间空两行
- 导入语句按标准库、第三方库、本地模块分组，每组之间空一行

### 注释规范
- 函数和类使用 docstring 说明功能
- 复杂逻辑添加行内注释
- 注释使用中文，与用户语言保持一致

### 错误处理
- 使用 try-except 捕获异常
- 异常信息要清晰明确
- 关键操作失败时提供友好的错误提示

### 函数设计
- 单一职责原则，每个函数只做一件事
- 函数参数不超过 5 个
- 返回值类型保持一致
- 避免使用全局变量

### 导入顺序
```python
import os
import sys
import re
import subprocess
import time
import webbrowser
import signal
import atexit
```

### 示例代码
```python
def find_venv(target_dir):
    """查找目标目录中已存在的虚拟环境"""
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
```

## 项目结构
- 主脚本：`auto_jupyter.py`
- 文档：`README.md`
- 代码风格：`CODE_STYLE.md`

## 开发原则
- 保持代码简洁，避免过度设计
- 优先使用标准库
- 注重代码可读性
- 遵循 Python PEP 8 规范
