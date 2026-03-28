# notebook_launcher

一个自动化的 Jupyter Notebook 启动工具，能够自动检测、创建虚拟环境并安装 Jupyter Notebook。

## 功能特性

- **自动检测虚拟环境**：支持检测常见的虚拟环境目录（venv、env、.venv）
- **自动创建虚拟环境**：当没有找到虚拟环境时，自动创建名为 "venv" 的虚拟环境
- **自动安装 Jupyter**：如果虚拟环境中未安装 Jupyter Notebook，自动从镜像源安装
- **自动安装中文插件**：安装 Jupyter 时自动安装中文插件，支持代码高亮、自动补全等功能
- **自动安装中文语言包**：安装 Jupyter 时自动安装中文语言包（jupyterlab-language-pack-zh-CN），不使用镜像源
- **自动切换成中文**：启动时自动设置 Jupyter 语言为中文
- **首次开启创建示例**：首次运行时自动创建 Start 文件夹和 hello.ipynb 示例文件，包含 Markdown 和 Python 代码示例
- **优化重启时机**：重启脚本的时机放在所有准备工作结束以后
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
4. **中文插件安装**：自动安装 Jupyter 中文插件（jupyter_contrib_nbextensions），提供代码高亮、自动补全等增强功能
5. **中文语言包安装**：自动安装 Jupyter 中文语言包（jupyterlab-language-pack-zh-CN）
6. **首次运行检测**：检查是否首次运行，如果是则创建 Start 文件夹和 hello.ipynb 示例文件
7. **自动重启**：创建环境或安装依赖后，脚本会自动重启以确保环境正确加载
8. **语言设置**：启动时自动设置 Jupyter 语言为中文
9. **启动服务**：重启后启动 Jupyter Notebook 并提取访问 URL
10. **打开浏览器**：使用默认浏览器打开 Jupyter Notebook

## 配置选项

脚本中的配置区域可以根据需要修改：

- `DEFAULT_DIR`：默认工作目录（脚本所在目录）
- `JUPYTER_TIMEOUT`：等待 Jupyter 启动的最大秒数
- `PIP_MIRROR`：pip 镜像源地址（默认使用清华大学镜像源）

## 中文支持说明

脚本会自动安装以下中文相关组件：

- **jupyter_contrib_nbextensions**：提供丰富的扩展功能集合
- **jupyter_nbextensions_configurator**：提供图形化配置界面
- **jupyterlab-language-pack-zh-CN**：Jupyter 中文语言包

安装完成后，可以在 Jupyter Notebook 的 "Nbextensions" 标签页中启用各种插件，常用的插件包括：

- **Code prettify**：代码格式化
- **Hinterland**：代码自动补全
- **Highlight selected word**：高亮选中的词
- **Variable Inspector**：变量检查器
- **ExecuteTime**：显示代码执行时间

脚本会自动设置 Jupyter 语言为中文，无需手动配置。

如果中文组件安装失败，不会影响 Jupyter Notebook 的正常使用。

## 注意事项

- 脚本会使用系统 Python 解释器创建虚拟环境
- 安装 Jupyter Notebook 时使用清华大学镜像源，提高下载速度
- 如果遇到 Python 版本兼容性问题，建议使用 Python 3.12 或更早版本
- 启动后请勿关闭命令窗口，如需停止 Jupyter 请手动结束进程

## 示例

### 首次运行（无虚拟环境）

1. 双击 `auto_jupyter.py`
2. 脚本会创建虚拟环境并安装 Jupyter
3. 自动安装中文插件和语言包
4. 创建 Start 文件夹和 hello.ipynb 示例文件
5. 自动重启后启动 Jupyter Notebook（语言已设置为中文）
6. 浏览器自动打开 Jupyter 界面

### 后续运行（已有虚拟环境）

1. 双击 `auto_jupyter.py`
2. 脚本检测到现有虚拟环境
3. 直接启动 Jupyter Notebook（语言已设置为中文）
4. 浏览器自动打开 Jupyter 界面

希望这个小工具对你有帮助 :)