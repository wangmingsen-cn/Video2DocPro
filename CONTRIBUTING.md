# 🎯 贡献指南

感谢你对 Video2DocPro 的兴趣！我们欢迎各种形式的贡献。

---

## 🤔 如何贡献

### 🐛 报告问题

如果你发现了 Bug 或有新功能建议：

1. 搜索 [Issue 列表](https://github.com/yourusername/Video2DocPro/issues) 确认问题未被报告
2. 创建新的 Issue，描述：
   - 清晰的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（操作系统、Python 版本等）
   - 错误日志或截图

### 🔧 修复代码

1. Fork 本项目
2. 创建特性分支：
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```
3. 进行开发，确保：
   - 代码遵循 PEP 8 规范
   - 添加适当的测试
   - 更新相关文档
4. 提交代码：
   ```bash
   git commit -m "Add: 新功能描述"
   git commit -m "Fix: 问题修复描述"
   ```
5. 推送到你的 Fork：
   ```bash
   git push origin feature/your-feature-name
   ```
6. 创建 Pull Request

### 📖 改进文档

文档改进同样重要！包括：
- 修正错别字或语法错误
- 补充遗漏的使用说明
- 翻译成其他语言
- 添加示例或教程

---

## 📋 Pull Request 指南

### 标题格式

```
[Feature] 新功能描述
[Fix] Bug 修复描述
[Refactor] 代码重构
[Docs] 文档更新
[Style] 代码格式调整
[Test] 测试相关
[Chore] 构建/工具更新
```

### PR 描述模板

```markdown
## 描述
简要描述你的更改

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 破坏性更改
- [ ] 文档更新

## 测试
描述你如何测试这些更改

## 截图（如有 UI 更改）
[在此添加截图]

## Checklist
- [ ] 我的代码遵循项目的代码规范
- [ ] 我已经进行了自测
- [ ] 我已经更新了相关文档
```

---

## 🏗️ 开发环境

### 环境要求

- Python 3.8+
- Git
- 推荐：VS Code 或 PyCharm

### 设置开发环境

```bash
# Fork 项目到你的账户
# 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/Video2DocPro.git
cd Video2DocPro

# 添加上游仓库
git remote add upstream https://github.com/yourusername/Video2DocPro.git

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
pip install openai-whisper

# 运行开发版本
python main.py
```

### 保持同步上游

```bash
# 切换到 main 分支
git checkout main

# 获取上游最新代码
git fetch upstream

# 合并到本地 main
git merge upstream/main

# 推送到你自己的 origin
git push origin main
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_video_processor.py

# 带覆盖率报告
python -m pytest --cov=src --cov-report=html
```

### 编写测试

```python
# tests/test_example.py
import pytest
from src.modules.video_processor import get_video_info

def test_video_info():
    # 你的测试代码
    info = get_video_info("test_video.mp4")
    assert info.duration > 0
    assert info.width > 0
    assert info.height > 0
```

---

## 📐 代码规范

### Python 代码规范

- 遵循 [PEP 8](https://pep8.org/)
- 使用类型注解（type hints）
- Docstrings 使用 Google/NumPy 风格
- 最大行长度：120 字符

### 示例

```python
def process_video(
    video_path: str,
    output_dir: str,
    model: str = "base",
) -> dict:
    """
    处理视频文件并返回结果。

    Args:
        video_path: 视频文件的完整路径
        output_dir: 输出目录路径
        model: Whisper 模型名称

    Returns:
        包含处理结果的字典

    Raises:
        FileNotFoundError: 当视频文件不存在时
        ValueError: 当视频格式不支持时
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    result = {
        "success": True,
        "output_path": output_dir,
    }
    return result
```

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块 | 小写下划线 | `video_processor.py` |
| 类 | 大写驼峰 | `class VideoProcessor` |
| 函数 | 小写下划线 | `def process_video()` |
| 常量 | 全大写下划线 | `MAX_VIDEO_SIZE` |
| 变量 | 小写下划线 | `video_path` |

---

## 💬 社区

- 📌 [GitHub Issues](https://github.com/yourusername/Video2DocPro/issues) - 问题反馈
- 💬 [Discussions](https://github.com/yourusername/Video2DocPro/discussions) - 讨论区
- 📧 邮箱：your.email@example.com

---

## 📜 开源协议

通过贡献代码，你同意将你的代码按照 [MIT 协议](LICENSE) 开源。

---

## 🙏 致谢

感谢所有贡献者的付出！

<a href="https://github.com/yourusername/Video2DocPro/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/Video2DocPro" />
</a>

---

**再次感谢你的贡献！🎉**
