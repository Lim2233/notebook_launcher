# notebook_launcher

一个自动化的 Jupyter Notebook 启动工具，能够自动检测、创建虚拟环境并安装 Jupyter Notebook。

## 功能特性

- **自动检测虚拟环境**：支持检测常见的虚拟环境目录（venv、env、.venv）
- **自动创建虚拟环境**：当没有找到虚拟环境时，自动创建名为 "venv" 的虚拟环境
- **自动安装 Jupyter**：如果虚拟环境中未安装 Jupyter Notebook，自动从镜像源安装
- **一键启动**：双击脚本即可完成所有准备工作并启动 Jupyter Notebook
- **自动打开浏览器**：启动后自动在默认浏览器中打开 Jupyter Notebook

## 使用方法

1. 将 `auto_jupyter.py` 放在项目目录中
2. 双击 `auto_jupyter.py` 脚本运行
3. 脚本会自动：
   - 检测或创建虚拟环境
   - 安装 Jupyter Notebook（如果需要）
   - 启动 Jupyter Notebook 并打开浏览器

## 工作原理

1. **环境检测**：脚本会检查当前目录下是否存在常见的虚拟环境目录
2. **环境创建**：如果没有找到虚拟环境，使用系统 Python 解释器创建名为 "venv" 的虚拟环境
3. **依赖安装**：检查虚拟环境中是否安装了 Jupyter Notebook，未安装则从清华大学镜像源安装
4. **自动重启**：创建环境或安装依赖后，脚本会自动重启以确保环境正确加载
5. **启动服务**：重启后启动 Jupyter Notebook 并提取访问 URL
6. **打开浏览器**：使用默认浏览器打开 Jupyter Notebook

## 配置选项

脚本中的配置区域可以根据需要修改：

- `DEFAULT_DIR`：默认工作目录（脚本所在目录）
- `JUPYTER_TIMEOUT`：等待 Jupyter 启动的最大秒数
- `PIP_MIRROR`：pip 镜像源地址（默认使用清华大学镜像源）

## 注意事项

- 脚本会使用系统 Python 解释器创建虚拟环境
- 安装 Jupyter Notebook 时使用清华大学镜像源，提高下载速度
- 如果遇到 Python 版本兼容性问题，建议使用 Python 3.12 或更早版本
- 启动后请勿关闭命令窗口，如需停止 Jupyter 请手动结束进程

## 示例

### 首次运行（无虚拟环境）

1. 双击 `auto_jupyter.py`
2. 脚本会创建虚拟环境并安装 Jupyter
3. 自动重启后启动 Jupyter Notebook
4. 浏览器自动打开 Jupyter 界面

### 后续运行（已有虚拟环境）

1. 双击 `auto_jupyter.py`
2. 脚本检测到现有虚拟环境
3. 直接启动 Jupyter Notebook
4. 浏览器自动打开 Jupyter 界面

希望这个小工具对你有帮助 :)