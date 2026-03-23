# 📁 Video2DocPro 项目结构

```
Video2DocPro/
│
├── README.md              ← 项目说明文档（GitHub 首页）
├── INSTALL.md             ← 安装与使用指南
├── CHANGELOG.md           ← 更新日志
├── LICENSE                ← MIT 开源协议
├── requirements.txt       ← Python 依赖清单
├── .gitignore            ← Git 忽略文件
│
├── main.py               ← 源码入口（开发调试用）
├── main_standalone.py    ← EXE 打包入口（最终发布用）
│
├── src/                  ← 核心源代码
│   ├── __init__.py
│   ├── app.py            ← PyQt6 主窗口 + UI 界面
│   └── modules/
│       ├── __init__.py
│       ├── video_processor.py   ← FFmpeg 视频处理（帧抽取/音频提取）
│       ├── transcriber.py       ← Whisper 语音转写
│       ├── ai_generator.py     ← AI 内容生成（总结/导图/笔记）
│       ├── doc_formatter.py    ← HTML/Markdown 文档格式化
│       └── batch_manager.py     ← 批量处理管理器
│
├── resources/             ← 资源文件
│   ├── logo.ico          ← Windows 应用图标
│   ├── logo_256.png      ← 256px Logo
│   └── logo_512.png      ← 512px Logo
│
└── build/                ← 打包配置
    ├── generate_logo.py  ← Logo 生成脚本
    └── inno_setup.iss    ← Inno Setup 安装包配置
```

---

## 📝 文件说明

### 核心代码

| 文件 | 说明 | 用途 |
|------|------|------|
| `main.py` | 源码入口 | 开发调试 |
| `main_standalone.py` | EXE 入口 | 发布打包 |
| `src/app.py` | PyQt6 主窗口 | GUI 界面 |
| `src/modules/video_processor.py` | FFmpeg 封装 | 视频处理 |
| `src/modules/transcriber.py` | Whisper 封装 | 语音转写 |
| `src/modules/ai_generator.py` | AI 内容生成 | 总结/导图/笔记 |
| `src/modules/doc_formatter.py` | 文档生成 | HTML/Markdown |
| `src/modules/batch_manager.py` | 批量处理 | 多视频处理 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `requirements.txt` | Python 依赖 |
| `.gitignore` | Git 忽略规则 |
| `build/inno_setup.iss` | 安装包配置 |

### 资源文件

| 文件 | 说明 |
|------|------|
| `resources/logo.ico` | 应用图标 |
| `resources/logo_256.png` | Logo 图片 |
| `resources/logo_512.png` | Logo 大图 |
| `build/generate_logo.py` | Logo 生成脚本 |

---

## 🔧 开发指南

### 环境搭建

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/Video2DocPro.git
cd Video2DocPro

# 2. 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装 Whisper
pip install openai-whisper

# 5. 运行开发版本
python main.py
```

### 打包 EXE

```bash
# 使用 Nuitka 打包
python -m nuitka --standalone --onefile \
  --windows-console-mode=disable \
  --enable-plugin=pyqt6 \
  --output-dir=dist \
  --output-filename=Video2DocPro.exe \
  --nofollow-import-to=numba \
  --nofollow-import-to=torch \
  --nofollow-import-to=whisper \
  --nofollow-import-to=scipy \
  --nofollow-import-to=matplotlib \
  --nofollow-import-to=pandas \
  --assume-yes-for-downloads \
  main_standalone.py
```

### 安装包打包

```bash
# 使用 Inno Setup
iscc build/inno_setup.iss
```

---

## 📊 代码统计

| 类型 | 数量 |
|------|------|
| Python 文件 | 10 |
| 总代码行数 | ~3000+ |
| 核心模块 | 5 |
| 配置文件 | 4 |
| 资源文件 | 3 |

---

**最后更新：2026-03-23**
