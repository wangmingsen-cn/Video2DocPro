# 🎬 Video2Doc Pro

<div align="center">

![Logo](resources/logo_256.png)

**让每一段视频，都能成为深度阅读的沉浸体验**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/Video2DocPro?style=social)](https://github.com/yourusername/Video2DocPro/stargazers)

**视频转沉浸式图文文档工具 | AI 智能总结 | 思维导图 | 课堂笔记**

[功能介绍](#核心功能) • [应用场景](#十大应用场景) • [安装使用](#快速开始) • [文档下载](#完整文档)

</div>

---

## 🎯 你是否有过这样的困扰？

- 想回看网课重点，却要反复拖动进度条？
- 会议太长，事后想找关键决策却大海捞针？
- 看完视频，核心要点怎么也记不住？
- 想要保存视频内容为文字，却只能手打？

**Video2Doc Pro 正是为解决这些痛点而生。**

---

## ✨ 核心功能

### 🧠 AI 智能总结
基于完整文字稿，AI 自动生成 **一段话核心总结**（≤200字），3秒钟掌握视频精华。

### 🗺️ 可视化思维导图
自动将内容梳理为树形思维导图，各主题逻辑关系一目了然。

### 📖 结构化课堂笔记
分章节整理，每章配有时间标记和重点标注，快速跳转至感兴趣的部分。

### 📹 沉浸式图文阅读
关键帧 + 文字图文对照，配合 AI 内容置顶，给你前所未有的阅读体验。

### 🎤 专业级语音转写
采用 OpenAI Whisper 引擎，精准识别中英文，准确率 90%+。

### 📄 双格式输出
- **HTML** — 深色科技风沉浸式文档（推荐）
- **Markdown** — 轻量文本，可导入各类笔记工具

---

## 🎨 输出文档结构

```
┌────────────────────────────────────────────────┐
│  🏠 顶部导航 + 徽章                              │
├────────────────────────────────────────────────┤
│  🖼️ 封面图（自动生成）                          │
├────────────────────────────────────────────────┤
│  🧠 核心总结（AI 生成，≤200字）                  │
│  关键词：[标签1] [标签2] [标签3]                 │
├────────────────────────────────────────────────┤
│  🗺️ 思维导图（可展开）                          │
│  ├─ 根节点                                     │
│  │  ├─ 子主题1                                 │
│  │  └─ 子主题2                                 │
├────────────────────────────────────────────────┤
│  📖 详细课堂笔记                                │
│  第一章：xxx（时间点 + 重点）                    │
│  第二章：xxx                                     │
├────────────────────────────────────────────────┤
│  📺 沉浸式图文阅读                              │
│  ⏱ 00:00 — Section 1                          │
│  [关键帧图片] + [转写文字]                       │
│  ...                                            │
└────────────────────────────────────────────────┘
```

---

## 🎯 十大应用场景

| 场景 | 说明 |
|------|------|
| 📚 **在线课程学习** | 网课视频转图文笔记，AI 提炼知识点，复习效率提升 300% |
| 💼 **会议高效复盘** | 长会议录像转结构化纪要，AI 总结关键决策和待办 |
| 🎬 **内容创作素材** | 批量处理视频素材，提取文字稿和关键画面 |
| 🌍 **外语学习** | TED 演讲转图文对照，边看视频边学外语 |
| 📰 **新闻资讯速读** | 长新闻视频转图文速读，3分钟掌握要点 |
| 🔬 **学术视频精读** | 学术讲座转详细笔记，提炼核心观点和结论 |
| 🏛️ **法律条文解读** | 法律讲座转条款解读笔记，标注关键法条 |
| 💡 **产品经理必备** | 竞品分析转结构化报告，提炼用户洞察 |
| 🎨 **设计灵感收集** | 设计教程转动作笔记，建立素材库 |
| 🏋️ **健身视频跟练** | 健身教程转动作笔记，配合关键帧跟练 |

---

## 🚀 快速开始

### 方式一：直接使用 EXE（推荐）

1. 下载 `Video2DocPro_v1.4.exe`
2. 双击运行
3. 如提示 Whisper 未安装，运行：
   ```bash
   pip install openai-whisper
   ```

### 方式二：从源码运行

```bash
# 克隆项目
git clone https://github.com/yourusername/Video2DocPro.git
cd Video2DocPro

# 安装依赖
pip install -r requirements.txt

# 安装 Whisper
pip install openai-whisper

# 运行程序
python main.py
```

---

## ⚙️ 配置说明

### AI API 配置

程序默认使用 **DeepSeek V3**，已内置 API Key，开箱即用。

如需使用其他服务商：
1. 点击「⚙️ 设置」
2. 输入 API Key
3. 选择服务商
4. 保存

支持的 AI 服务商：
- ✅ **DeepSeek V3**（推荐，性价比最高）
- ✅ OpenAI GPT-3.5/4
- ✅ 智谱 ChatGLM
- ✅ 百度文心一言

### Whisper 模型选择

| 模型 | 速度 | 准确率 | 内存占用 | 推荐 |
|------|------|--------|---------|------|
| tiny | 最快 | 较低 | ~1GB | 快速预览 |
| **base** | 快 | 良好 | ~1GB | ✅ **日常使用** |
| small | 中 | 高 | ~2GB | 高质量 |
| medium | 慢 | 很高 | ~5GB | 专业转写 |
| large | 最慢 | 最高 | ~10GB | 最高要求 |

---

## 📂 输出文件说明

处理完成后，输出目录会生成：

```
视频名_doc/
├── 视频名.html          ← 主文件，用浏览器打开
├── 视频名.md            ← Markdown 格式
├── cover_视频名.png     ← 封面图（1200×630）
└── frames/             ← 关键帧目录
    ├── frame_000000.jpg
    ├── frame_000030.jpg
    └── ...
```

---

## 🐛 常见问题

**Q: 程序无法启动？**
A: 确保 Windows 10/11 64位，尝试右键「以管理员身份运行」。

**Q: Whisper 处理很慢？**
A: 首次运行会自动下载模型，之后会缓存。可选择更小的模型。

**Q: AI 生成失败？**
A: 检查网络连接、API Key 是否正确、API 额度是否充足。

**Q: 支持哪些格式？**
A: MP4、MOV、AVI、MKV，最大支持 2GB。

---

## 🔄 更新日志

### v1.4 (2026-03-23)
- ✅ 重构架构，解决打包兼容性问题
- ✅ EXE 只负责 UI，处理通过 subprocess 调用
- ✅ 更稳定的运行体验

### v1.0 - v1.3
- ✅ 初始版本发布
- ✅ 添加 DeepSeek API 支持
- ✅ AI 内容置顶显示
- ✅ 批量处理支持

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

---

## 📄 完整文档

| 文档 | 说明 |
|------|------|
| **Video2DocPro产品说明书.docx** | 完整产品说明书（Word 版） |
| [INSTALL.md](INSTALL.md) | 详细安装与使用教程 |
| [CHANGELOG.md](CHANGELOG.md) | 版本更新日志 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献者指南 |

---

## 🙏 致谢

- [Whisper](https://github.com/openai/whisper) — OpenAI 语音识别
- [DeepSeek](https://deepseek.com/) — AI 大语言模型
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) — GUI 框架
- [FFmpeg](https://ffmpeg.org/) — 多媒体处理

---

## 📜 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

---

<div align="center">

**让每一次观看，都有所收获。**

⭐ 如果这个项目对你有帮助，请 Star！

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
