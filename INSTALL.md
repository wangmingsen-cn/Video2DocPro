# 📖 Video2DocPro 安装与使用指南

## 📋 目录

- [环境要求](#-环境要求)
- [安装方式](#-安装方式)
- [快速开始](#-快速开始)
- [详细配置](#-详细配置)
- [使用教程](#-使用教程)
- [故障排除](#-故障排除)

---

## 💻 环境要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 10 (64位) | Windows 11 |
| Python | 3.8+ | 3.11 |
| 内存 | 4GB | 8GB+ |
| 磁盘空间 | 2GB | 5GB+ |
| 网络 | 需要（AI 调用） | 100Mbps+ |

---

## 📦 安装方式

### 方式一：直接使用 EXE（推荐）

#### 步骤 1：下载程序

下载最新的 `Video2DocPro_v1.4.exe` 文件（约 60MB）

#### 步骤 2：运行程序

直接双击 `Video2DocPro_v1.4.exe` 即可运行

#### 步骤 3：安装 Whisper（如首次使用）

程序运行后会自动检测环境，如提示 Whisper 未安装，打开命令提示符运行：

```bash
pip install openai-whisper
```

> ⚠️ 首次运行 Whisper 会自动下载模型（约 75MB），请保持网络连接

---

### 方式二：从源码运行

#### 步骤 1：安装 Python

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.11 或更高版本
3. 安装时勾选 **"Add Python to PATH"**

验证安装：
```bash
python --version
```

#### 步骤 2：克隆项目

```bash
git clone https://github.com/yourusername/Video2DocPro.git
cd Video2DocPro
```

#### 步骤 3：创建虚拟环境（推荐）

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### 步骤 4：安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 5：安装 Whisper

```bash
pip install openai-whisper
```

#### 步骤 6：运行程序

```bash
python main.py
```

---

## 🚀 快速开始

### 第一次使用

```
1. 双击 Video2DocPro_v1.4.exe
2. 点击「浏览」选择视频文件
3. 选择输出目录（默认：桌面 ARTICAL）
4. 点击「开始处理」
5. 等待完成（进度条显示）
6. 用浏览器打开生成的 HTML 文件
```

### 批量处理

```
1. 点击「浏览」选择包含多个视频的文件夹
2. 程序自动扫描所有支持格式的视频
3. 点击「开始处理」
4. 程序会依次处理每个视频
```

---

## ⚙️ 详细配置

### AI API 配置

程序默认使用内置的 DeepSeek API，如需使用自己的 API：

1. 点击界面右上角的「⚙️ 设置」
2. 输入你的 API Key
3. 选择服务商
4. 点击「保存」

#### 获取 DeepSeek API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册/登录账号
3. 进入「API Keys」页面
4. 创建新的 API Key
5. 复制并粘贴到程序中

#### API 服务商对比

| 服务商 | 模型 | 特点 | 价格 |
|--------|------|------|------|
| DeepSeek | DeepSeek V3 | 性价比高，中文优化 | 低 |
| OpenAI | GPT-3.5/4 | 通用能力强 | 中高 |
| 智谱 | ChatGLM | 中文能力强 | 中 |

### Whisper 模型选择

| 模型 | 速度 | 准确率 | 内存占用 | 推荐场景 |
|------|------|--------|---------|---------|
| tiny | 最快 | 较低 | ~1GB | 快速预览 |
| **base** | 快 | 良好 | ~1GB | ✅ 推荐日常使用 |
| small | 中 | 高 | ~2GB | 正式场合 |
| medium | 慢 | 很高 | ~5GB | 高质量需求 |
| large | 最慢 | 最高 | ~10GB | 专业转写 |

### 关键帧抽取间隔

默认每 30 秒抽取一帧，可在设置中调整：
- 10 秒：更密集，适合快节奏内容
- 30 秒：平衡（推荐）
- 60 秒：更稀疏，适合长视频

---

## 📖 使用教程

### 场景 1：在线课程转笔记

```
1. 下载网课视频到本地
2. 用程序打开
3. 选择 Whisper "base" 模型
4. 等待处理完成
5. 打开 HTML 查看：
   - AI 核心总结快速了解课程重点
   - 思维导图理清知识结构
   - 课堂笔记详细回顾每个知识点
   - 沉浸式阅读配合关键帧复习
```

### 场景 2：会议记录

```
1. 录制或下载会议视频
2. 批量导入程序
3. 选择 "tiny" 模型加快处理
4. 快速获取会议纪要
5. AI 总结提炼关键决策
```

### 场景 3：内容创作素材

```
1. 收集相关视频素材
2. 用程序批量处理
3. 获取完整文字稿
4. AI 生成的内容可直接用于创作
```

---

## 🐛 故障排除

### 问题 1：程序无法启动

**症状**：双击 EXE 后程序无响应或闪退

**解决方案**：
1. 确保 Windows 10/11 64位系统
2. 安装 Visual C++ Redistributable
3. 尝试右键 -> "以管理员身份运行"

### 问题 2：Whisper 报错 "DLL load failed"

**症状**：提示找不到 torch DLL

**解决方案**：
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 问题 3：FFmpeg 未找到

**症状**：提示 FFmpeg 相关错误

**解决方案**：
```bash
pip uninstall imageio-ffmpeg
pip install imageio-ffmpeg
```

### 问题 4：AI 生成失败

**症状**：API 调用错误或超时

**解决方案**：
1. 检查网络连接
2. 确认 API Key 正确
3. 检查 API 额度是否充足
4. 尝试更换服务商

### 问题 5：处理速度很慢

**解决方案**：
1. 选择更小的 Whisper 模型
2. 关闭其他占用内存的程序
3. 确保足够的磁盘空间

### 问题 6：HTML 文件图片不显示

**症状**：打开 HTML 后图片显示为红叉

**解决方案**：
1. 用 Chrome/Edge 浏览器打开
2. 不要直接双击文件，用浏览器"打开"功能
3. 确保输出文件夹路径不包含特殊字符

---

## 📞 获取帮助

- 📖 查看 [README.md](README.md) 了解项目详情
- 🐛 提交 [Issue](https://github.com/yourusername/Video2DocPro/issues) 报告问题
- 💡 提交 [PR](https://github.com/yourusername/Video2DocPro/pulls) 贡献代码

---

## 🔄 常见问题 FAQ

**Q: 支持哪些视频格式？**
A: MP4、MOV、AVI、MKV，最大支持 2GB

**Q: 处理一个 10 分钟视频需要多久？**
A: 约 3-5 分钟（取决于硬件配置）

**Q: 可以离线使用吗？**
A: 视频处理可以离线，但 AI 生成功能需要网络

**Q: 支持批量处理吗？**
A: 支持，选择文件夹后会自动处理所有视频

**Q: 生成的文档可以编辑吗？**
A: 可以，Markdown 格式可直接编辑

---

**最后更新：2026-03-23**
