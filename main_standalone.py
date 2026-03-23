#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main_standalone.py — Video2Doc Pro 独立入口 v1.4
架构：EXE 只负责 UI，所有处理通过 subprocess 调用系统 Python
这样彻底避免 torch/whisper DLL 在打包环境中的加载问题
"""

import os, sys, subprocess, json, threading, glob, time
from pathlib import Path

# ── 找到系统 Python ──────────────────────────────────────────────────────────
def find_python():
    """找到可用的 Python 解释器"""
    candidates = [
        sys.executable,                                    # 当前 Python
        r"C:\Users\29494\AppData\Local\Programs\Python\Python311\python.exe",
        r"C:\Python311\python.exe",
        r"C:\Python310\python.exe",
        r"C:\Python39\python.exe",
    ]
    # 也从 PATH 里找
    import shutil
    for name in ["python", "python3", "python311"]:
        p = shutil.which(name)
        if p:
            candidates.insert(1, p)

    for c in candidates:
        if c and os.path.isfile(c):
            try:
                r = subprocess.run([c, "--version"], capture_output=True, timeout=5)
                if r.returncode == 0:
                    return c
            except Exception:
                pass
    return None

# ── 找到项目根目录 ────────────────────────────────────────────────────────────
def find_project_root():
    """找到 Video2DocPro 项目根目录"""
    # EXE 所在目录
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    candidates = [
        exe_dir,
        os.path.join(exe_dir, "Video2DocPro"),
        r"C:\Users\29494\.qclaw\workspace\Video2DocPro",
        os.path.expanduser("~/.qclaw/workspace/Video2DocPro"),
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(c, "run_test.py")):
            return c
    return None

PYTHON_EXE = find_python()
PROJECT_ROOT = find_project_root()

# ── PyQt6 UI ─────────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFrame,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem,
    QSizePolicy, QDialog, QComboBox, QCheckBox, QScrollArea,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

# ── 配色 ─────────────────────────────────────────────────────────────────────
C_BG      = "#080b12"
C_SURF    = "#0d1117"
C_CARD    = "#161b22"
C_BORDER  = "#21262d"
C_BORDER2 = "#30363d"
C_ACCENT  = "#58a6ff"
C_ACCENT2 = "#8b5cf6"
C_ACCENT3 = "#34d399"
C_TEXT    = "#e6edf3"
C_MUTED   = "#8b949e"
C_MUTED2  = "#6e7681"
C_WARN    = "#f0883e"
C_DANGER  = "#f85149"
FONT_MAIN = "Segoe UI"
FONT_MONO = "Consolas"

# ── 处理线程 ──────────────────────────────────────────────────────────────────
class WorkerThread(QThread):
    log_signal   = pyqtSignal(str, str)   # (message, tag)
    prog_signal  = pyqtSignal(int)        # 0-100
    done_signal  = pyqtSignal(bool, str)  # (success, message)

    def __init__(self, video_path: str, output_dir: str, settings: dict):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.settings   = settings

    def run(self):
        python = PYTHON_EXE
        root   = PROJECT_ROOT

        if not python:
            self.done_signal.emit(False, "未找到 Python 解释器，请确认 Python 已安装")
            return
        if not root:
            self.done_signal.emit(False, "未找到项目目录，请确认 Video2DocPro 已正确安装")
            return

        self.log_signal.emit(f"Python: {python}", "info")
        self.log_signal.emit(f"项目目录: {root}", "info")
        self.log_signal.emit("开始处理视频...", "prog")

        # 构建处理脚本（内联，避免路径问题）
        api_key  = self.settings.get("api_key", "sk-6cd1034d006d47bc9c728a4539f6b812")
        provider = self.settings.get("provider", "deepseek")
        model    = self.settings.get("whisper_model", "base")

        script = f"""
# -*- coding: utf-8 -*-
import sys, os, glob
sys.path.insert(0, r'{root}/src/modules')

video  = r'{self.video_path}'
output = r'{self.output_dir}'
os.makedirs(output, exist_ok=True)

print('[1/5] 分析视频...')
from video_processor import get_video_info, extract_audio, extract_frames
info = get_video_info(video)
print(f'  时长: {{info.duration:.1f}}秒  分辨率: {{info.width}}x{{info.height}}')

from pathlib import Path
video_stem = Path(video).stem
video_out  = os.path.join(output, video_stem + '_doc')
os.makedirs(video_out, exist_ok=True)

print('[2/5] 提取音频...')
audio_path = os.path.join(video_out, '_temp_audio.wav')
extract_audio(video, audio_path)
print(f'  完成: {{os.path.getsize(audio_path)//1024}} KB')

print('[3/5] 提取关键帧...')
frames_dir = os.path.join(video_out, 'frames')
frames = extract_frames(video, frames_dir, interval=30)
print(f'  共 {{len(frames)}} 帧')

print('[4/5] Whisper 语音转写...')
from transcriber import transcribe
result   = transcribe(audio_path, model_name='{model}')
segments = result['segments']
transcript = result['text']
print(f'  语言: {{result["language"]}}  片段: {{len(segments)}}  字符: {{len(transcript)}}')

print('[5/5] AI 内容生成...')
from ai_generator import AIGenerator
ai = AIGenerator(api_key='{api_key}', provider='{provider}')
ai_content = ai.generate_all(transcript, video_stem, segments, frames)
if ai_content.summary:
    print(f'  总结: {{ai_content.summary.content[:60]}}...')
print(f'  笔记: {{len(ai_content.notes)}} 章')

print('[6/6] 生成文档...')
from doc_formatter import DocFormatter, generate_cover_image
formatter  = DocFormatter(video_out)
cover_path = generate_cover_image(video_stem, info.duration, frames_dir, video_out)
cover_rel  = os.path.basename(cover_path) if cover_path else ''
sections   = formatter.merge_segments_by_frames(segments, frames)
html_path  = formatter.to_html(video_stem, ai_content, sections, 'frames', cover_rel, info.duration)
md_path    = formatter.to_markdown(video_stem, ai_content, sections, 'frames', cover_rel, info.duration)

if os.path.exists(audio_path):
    os.remove(audio_path)

print('DONE:' + html_path)
"""

        try:
            proc = subprocess.Popen(
                [python, "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=root,
            )

            html_path = ""
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                if line.startswith("DONE:"):
                    html_path = line[5:]
                    self.log_signal.emit(f"文档已生成: {html_path}", "ok")
                elif line.startswith("["):
                    step = line.split("]")[0].lstrip("[")
                    try:
                        cur, total = step.split("/")
                        pct = int(int(cur) / int(total) * 100)
                        self.prog_signal.emit(pct)
                    except Exception:
                        pass
                    self.log_signal.emit(line, "prog")
                elif "%" in line and "frames/s" in line:
                    # Whisper 进度条，不显示
                    pass
                elif line.startswith("  "):
                    self.log_signal.emit(line.strip(), "info")
                else:
                    self.log_signal.emit(line, "info")

            proc.wait()
            if proc.returncode == 0 or html_path:
                self.prog_signal.emit(100)
                self.done_signal.emit(True, html_path or self.output_dir)
            else:
                self.done_signal.emit(False, f"处理失败，退出码: {proc.returncode}")

        except Exception as e:
            self.done_signal.emit(False, str(e))


# ── 设置对话框 ────────────────────────────────────────────────────────────────
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ AI API 设置")
        self.setFixedSize(560, 420)
        self.setModal(True)
        self.setStyleSheet(f"background:{C_BG}; color:{C_TEXT};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        title = QLabel("🔑 API 配置")
        title.setFont(QFont(FONT_MAIN, 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{C_ACCENT}")
        layout.addWidget(title)

        layout.addWidget(QLabel("支持 DeepSeek / OpenAI / 智谱 ChatGLM"))

        layout.addWidget(QLabel("API Key:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("sk-...")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setStyleSheet(self._inp_style())
        layout.addWidget(self.key_input)

        layout.addWidget(QLabel("服务商:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["DeepSeek V3 ⭐ 推荐", "OpenAI GPT-3.5/4", "智谱 ChatGLM"])
        self.provider_combo.setStyleSheet(self._inp_style())
        layout.addWidget(self.provider_combo)

        layout.addWidget(QLabel("Whisper 模型 (越大越准，越慢):"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny (最快)", "base (推荐)", "small", "medium", "large (最准)"])
        self.model_combo.setCurrentIndex(1)
        self.model_combo.setStyleSheet(self._inp_style())
        layout.addWidget(self.model_combo)

        layout.addStretch()
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel = QPushButton("取消")
        cancel.setStyleSheet(f"background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER}; border-radius:8px; padding:8px 20px;")
        cancel.clicked.connect(self.reject)
        save = QPushButton("保存")
        save.setStyleSheet(f"background:{C_ACCENT}; color:#fff; border:none; border-radius:8px; padding:8px 20px; font-weight:bold;")
        save.clicked.connect(self.accept)
        btn_row.addWidget(cancel)
        btn_row.addWidget(save)
        layout.addLayout(btn_row)

    def _inp_style(self):
        return f"background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER}; border-radius:8px; padding:8px 12px;"

    def get_settings(self):
        providers = ["deepseek", "openai", "zhipu"]
        models    = ["tiny", "base", "small", "medium", "large"]
        return {
            "api_key":       self.key_input.text().strip(),
            "provider":      providers[self.provider_combo.currentIndex()],
            "whisper_model": models[self.model_combo.currentIndex()],
        }

    def set_settings(self, s: dict):
        self.key_input.setText(s.get("api_key", ""))
        providers = ["deepseek", "openai", "zhipu"]
        idx = providers.index(s.get("provider", "deepseek")) if s.get("provider") in providers else 0
        self.provider_combo.setCurrentIndex(idx)
        models = ["tiny", "base", "small", "medium", "large"]
        midx = models.index(s.get("whisper_model", "base")) if s.get("whisper_model") in models else 1
        self.model_combo.setCurrentIndex(midx)


# ── 主窗口 ────────────────────────────────────────────────────────────────────
class MainWindow(QWidget):
    SUPPORTED = {".mp4", ".mov", ".avi", ".mkv"}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video2Doc Pro")
        self.setMinimumSize(900, 680)
        self._settings = QSettings("Video2DocPro", "App")
        self._videos   = []
        self._worker   = None
        self._build()
        self._apply_style()
        QTimer.singleShot(300, self._check_env)

    def _apply_style(self):
        self.setStyleSheet(f"""
            QWidget {{ background:{C_BG}; color:{C_TEXT}; font-family:'{FONT_MAIN}'; font-size:13px; }}
            QLabel  {{ background:transparent; }}
            QLineEdit {{
                background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER};
                border-radius:8px; padding:8px 12px;
            }}
            QLineEdit:focus {{ border-color:{C_ACCENT}; }}
            QListWidget {{
                background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER};
                border-radius:8px; padding:4px;
            }}
            QListWidget::item:selected {{ background:{C_ACCENT}; color:#fff; border-radius:4px; }}
            QTextEdit {{
                background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER};
                border-radius:8px; padding:8px; font-family:'{FONT_MONO}'; font-size:12px;
            }}
            QScrollBar:vertical {{
                background:{C_SURF}; width:6px; border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:{C_BORDER2}; border-radius:3px;
            }}
        """)

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 顶栏 ──────────────────────────────────────────────────────────────
        topbar = QFrame()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet(f"background:{C_SURF}; border-bottom:1px solid {C_BORDER};")
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 0, 20, 0)

        logo = QLabel("🎬 Video2Doc Pro")
        logo.setFont(QFont(FONT_MAIN, 13, QFont.Weight.Bold))
        logo.setStyleSheet(f"color:{C_ACCENT};")
        tb.addWidget(logo)

        badge = QLabel("AI 增强")
        badge.setStyleSheet(f"""
            background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {C_ACCENT},stop:1 {C_ACCENT2});
            color:#fff; border-radius:10px; padding:2px 10px; font-size:11px;
        """)
        tb.addWidget(badge)
        tb.addStretch()

        # 状态指示灯
        self.status_labels = {}
        for key, label in [("python", "Python"), ("ffmpeg", "FFmpeg"), ("whisper", "Whisper"), ("ai", "AI")]:
            lbl = QLabel(f"● {label}")
            lbl.setStyleSheet(f"color:{C_MUTED2}; font-size:11px; padding:0 8px;")
            self.status_labels[key] = lbl
            tb.addWidget(lbl)

        btn_settings = QPushButton("⚙️ 设置")
        btn_settings.setStyleSheet(f"""
            background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER};
            border-radius:6px; padding:4px 14px; font-size:12px;
        """)
        btn_settings.clicked.connect(self._open_settings)
        tb.addWidget(btn_settings)
        root.addWidget(topbar)

        # ── 主体 ──────────────────────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(20, 20, 20, 20)
        body.setSpacing(16)

        # 左栏：输入
        left = QVBoxLayout()
        left.setSpacing(12)

        # 视频选择
        lbl_vid = QLabel("📂 视频文件 / 文件夹")
        lbl_vid.setFont(QFont(FONT_MAIN, 10, QFont.Weight.Bold))
        lbl_vid.setStyleSheet(f"color:{C_MUTED};")
        left.addWidget(lbl_vid)

        row_vid = QHBoxLayout()
        self.video_path_input = QLineEdit()
        self.video_path_input.setPlaceholderText("选择视频文件或包含视频的文件夹...")
        row_vid.addWidget(self.video_path_input)
        btn_file = QPushButton("文件")
        btn_file.setFixedWidth(60)
        btn_file.setStyleSheet(self._btn_secondary())
        btn_file.clicked.connect(lambda: self._browse(False))
        btn_dir = QPushButton("文件夹")
        btn_dir.setFixedWidth(70)
        btn_dir.setStyleSheet(self._btn_secondary())
        btn_dir.clicked.connect(lambda: self._browse(True))
        row_vid.addWidget(btn_file)
        row_vid.addWidget(btn_dir)
        left.addLayout(row_vid)

        # 视频列表
        self.video_list = QListWidget()
        self.video_list.setMinimumHeight(120)
        self.video_count_lbl = QLabel("0 个视频")
        self.video_count_lbl.setStyleSheet(f"color:{C_MUTED2}; font-size:11px;")
        left.addWidget(self.video_list)
        left.addWidget(self.video_count_lbl)

        # 输出目录
        lbl_out = QLabel("📁 输出目录")
        lbl_out.setFont(QFont(FONT_MAIN, 10, QFont.Weight.Bold))
        lbl_out.setStyleSheet(f"color:{C_MUTED};")
        left.addWidget(lbl_out)

        row_out = QHBoxLayout()
        self.output_path_input = QLineEdit()
        default_out = self._settings.value("output_dir", os.path.expanduser("~/Desktop/ARTICAL"))
        self.output_path_input.setText(default_out)
        row_out.addWidget(self.output_path_input)
        btn_out = QPushButton("浏览")
        btn_out.setFixedWidth(60)
        btn_out.setStyleSheet(self._btn_secondary())
        btn_out.clicked.connect(self._browse_output)
        row_out.addWidget(btn_out)
        left.addLayout(row_out)

        # 处理按钮
        self.process_btn = QPushButton("▶  开始处理")
        self.process_btn.setFixedHeight(44)
        self.process_btn.setFont(QFont(FONT_MAIN, 12, QFont.Weight.Bold))
        self.process_btn.setStyleSheet(f"""
            QPushButton {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {C_ACCENT},stop:1 {C_ACCENT2});
                color:#fff; border:none; border-radius:10px;
            }}
            QPushButton:hover {{ opacity:0.9; }}
            QPushButton:disabled {{ background:{C_BORDER}; color:{C_MUTED}; }}
        """)
        self.process_btn.clicked.connect(self._start_process)
        left.addWidget(self.process_btn)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{ background:{C_SURF}; border:none; border-radius:4px; }}
            QProgressBar::chunk {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {C_ACCENT},stop:1 {C_ACCENT3});
                border-radius:4px;
            }}
        """)
        left.addWidget(self.progress_bar)

        body.addLayout(left, 1)

        # 右栏：日志
        right = QVBoxLayout()
        right.setSpacing(8)

        lbl_log = QLabel("📋 处理日志")
        lbl_log.setFont(QFont(FONT_MAIN, 10, QFont.Weight.Bold))
        lbl_log.setStyleSheet(f"color:{C_MUTED};")
        right.addWidget(lbl_log)

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        right.addWidget(self.log_widget)

        row_btns = QHBoxLayout()
        btn_clear = QPushButton("🗑 清空日志")
        btn_clear.setStyleSheet(self._btn_secondary())
        btn_clear.clicked.connect(self.log_widget.clear)
        btn_open = QPushButton("📂 打开输出文件夹")
        btn_open.setStyleSheet(self._btn_secondary())
        btn_open.clicked.connect(self._open_output)
        row_btns.addWidget(btn_clear)
        row_btns.addStretch()
        row_btns.addWidget(btn_open)
        right.addLayout(row_btns)

        body.addLayout(right, 1)
        root.addLayout(body)

    # ── 样式辅助 ──────────────────────────────────────────────────────────────
    def _btn_secondary(self):
        return f"""
            QPushButton {{
                background:{C_CARD}; color:{C_TEXT}; border:1px solid {C_BORDER};
                border-radius:8px; padding:6px 14px;
            }}
            QPushButton:hover {{ border-color:{C_ACCENT}; color:{C_ACCENT}; }}
        """

    # ── 环境检测 ──────────────────────────────────────────────────────────────
    def _check_env(self):
        self._log("正在检测运行环境...", "info")

        # Python
        if PYTHON_EXE:
            self._set_status("python", f"Python OK", C_ACCENT3)
            self._log(f"Python: {PYTHON_EXE}", "ok")
        else:
            self._set_status("python", "Python 未找到", C_DANGER)
            self._log("Python 未找到，请安装 Python 3.8+", "err")

        # 项目目录
        if PROJECT_ROOT:
            self._log(f"项目目录: {PROJECT_ROOT}", "ok")
        else:
            self._log("项目目录未找到！", "err")

        # FFmpeg（通过 subprocess 检测）
        if PYTHON_EXE and PROJECT_ROOT:
            try:
                r = subprocess.run(
                    [PYTHON_EXE, "-c",
                     f"import sys; sys.path.insert(0,r'{PROJECT_ROOT}/src/modules'); "
                     "from video_processor import FFMPEG_BIN; print(FFMPEG_BIN)"],
                    capture_output=True, text=True, timeout=15
                )
                if r.returncode == 0 and r.stdout.strip():
                    self._set_status("ffmpeg", "FFmpeg OK", C_ACCENT3)
                    self._log(f"FFmpeg: {os.path.basename(r.stdout.strip())}", "ok")
                else:
                    self._set_status("ffmpeg", "FFmpeg 未找到", C_DANGER)
                    self._log("FFmpeg 未找到，请运行: pip install imageio-ffmpeg", "warn")
            except Exception as e:
                self._set_status("ffmpeg", "FFmpeg 检测失败", C_WARN)
                self._log(f"FFmpeg 检测失败: {e}", "warn")

        # Whisper（通过 subprocess 检测）
        if PYTHON_EXE:
            try:
                r = subprocess.run(
                    [PYTHON_EXE, "-c",
                     "import importlib.util; s=importlib.util.find_spec('whisper'); print('OK' if s else 'MISSING')"],
                    capture_output=True, text=True, timeout=10
                )
                if "OK" in r.stdout:
                    self._set_status("whisper", "Whisper OK", C_ACCENT3)
                    self._log("Whisper: 已安装", "ok")
                else:
                    self._set_status("whisper", "Whisper 未安装", C_WARN)
                    self._log("Whisper 未安装，请运行: pip install openai-whisper", "warn")
            except Exception as e:
                self._set_status("whisper", "Whisper 检测失败", C_WARN)

        # AI
        api_key = self._settings.value("api_key", "sk-6cd1034d006d47bc9c728a4539f6b812")
        if api_key and len(api_key) > 8:
            provider = self._settings.value("provider", "deepseek")
            self._set_status("ai", f"AI OK ({provider})", C_ACCENT3)
            self._log(f"AI API: {provider} 已配置", "ok")
        else:
            self._set_status("ai", "AI 未配置", C_WARN)

        self._log("环境检测完成，可以开始处理", "ok")

    # ── 浏览文件 ──────────────────────────────────────────────────────────────
    def _browse(self, is_dir: bool):
        if is_dir:
            path = QFileDialog.getExistingDirectory(self, "选择视频文件夹")
            if path:
                self.video_path_input.setText(path)
                self._load_dir(path)
        else:
            path, _ = QFileDialog.getOpenFileName(
                self, "选择视频文件", "",
                "视频文件 (*.mp4 *.mov *.avi *.mkv);;所有文件 (*)"
            )
            if path:
                self.video_path_input.setText(path)
                self._load_single(path)

    def _browse_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_path_input.setText(path)

    def _load_single(self, path: str):
        name = os.path.basename(path)
        size = os.path.getsize(path) / 1e6
        self._videos = [{"name": name, "path": path, "size": size}]
        self._refresh_list()

    def _load_dir(self, folder: str):
        self._videos = []
        try:
            for entry in Path(folder).iterdir():
                if entry.is_file() and entry.suffix.lower() in self.SUPPORTED:
                    self._videos.append({
                        "name": entry.name,
                        "path": str(entry),
                        "size": entry.stat().st_size / 1e6,
                    })
        except Exception as e:
            self._log(f"读取目录失败: {e}", "err")
        self._videos.sort(key=lambda x: x["name"])
        self._refresh_list()

    def _refresh_list(self):
        self.video_list.clear()
        for v in self._videos:
            self.video_list.addItem(f"🎬  {v['name']}  ({v['size']:.1f} MB)")
        self.video_count_lbl.setText(f"{len(self._videos)} 个视频")

    # ── 开始处理 ──────────────────────────────────────────────────────────────
    def _start_process(self):
        if not self._videos:
            self._log("请先选择视频文件或文件夹", "warn")
            return

        out_dir = self.output_path_input.text().strip()
        if not out_dir:
            self._log("请设置输出目录", "warn")
            return

        os.makedirs(out_dir, exist_ok=True)
        self._settings.setValue("output_dir", out_dir)

        if not PYTHON_EXE:
            self._log("未找到 Python 解释器，无法处理", "err")
            return
        if not PROJECT_ROOT:
            self._log("未找到项目目录，无法处理", "err")
            return

        self.process_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_widget.clear()

        settings = {
            "api_key":       self._settings.value("api_key", "sk-6cd1034d006d47bc9c728a4539f6b812"),
            "provider":      self._settings.value("provider", "deepseek"),
            "whisper_model": self._settings.value("whisper_model", "base"),
        }

        # 逐个处理视频
        self._pending = list(self._videos)
        self._out_dir = out_dir
        self._settings_dict = settings
        self._process_next()

    def _process_next(self):
        if not self._pending:
            self.process_btn.setEnabled(True)
            self._log("=" * 40, "sep")
            self._log("全部处理完成！", "ok")
            return

        v = self._pending.pop(0)
        self._log(f"{'='*40}", "sep")
        self._log(f"处理: {v['name']}", "prog")

        self._worker = WorkerThread(v["path"], self._out_dir, self._settings_dict)
        self._worker.log_signal.connect(self._log)
        self._worker.prog_signal.connect(self.progress_bar.setValue)
        self._worker.done_signal.connect(self._on_done)
        self._worker.start()

    def _on_done(self, success: bool, msg: str):
        if success:
            self._log(f"完成！输出: {msg}", "ok")
        else:
            self._log(f"失败: {msg}", "err")
        self._process_next()

    # ── 设置 ──────────────────────────────────────────────────────────────────
    def _open_settings(self):
        dlg = SettingsDialog(self)
        dlg.set_settings({
            "api_key":       self._settings.value("api_key", "sk-6cd1034d006d47bc9c728a4539f6b812"),
            "provider":      self._settings.value("provider", "deepseek"),
            "whisper_model": self._settings.value("whisper_model", "base"),
        })
        if dlg.exec():
            s = dlg.get_settings()
            for k, v in s.items():
                self._settings.setValue(k, v)
            self._log("设置已保存", "ok")

    # ── 打开输出文件夹 ────────────────────────────────────────────────────────
    def _open_output(self):
        out = self.output_path_input.text().strip()
        if os.path.exists(out):
            os.startfile(out)
        else:
            self._log(f"输出目录不存在: {out}", "warn")

    # ── 状态 / 日志 ───────────────────────────────────────────────────────────
    def _set_status(self, key: str, text: str, color: str):
        if key in self.status_labels:
            self.status_labels[key].setText(f"● {text}")
            self.status_labels[key].setStyleSheet(
                f"color:{color}; font-size:11px; padding:0 8px;"
            )

    def _log(self, msg: str, tag: str = "info"):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        colors = {
            "ok": C_ACCENT3, "info": C_MUTED2, "warn": C_WARN,
            "err": C_DANGER, "prog": C_ACCENT, "sep": C_BORDER2,
        }
        pfx = {"ok": "✓", "warn": "⚠", "err": "✗", "prog": "→", "sep": "─"}.get(tag, " ")
        color = colors.get(tag, C_MUTED2)
        html = (f'<span style="color:{C_MUTED2}">[{ts}]</span> '
                f'<span style="color:{color}">{pfx} {msg}</span>')
        self.log_widget.append(html)
        self.log_widget.verticalScrollBar().setValue(
            self.log_widget.verticalScrollBar().maximum()
        )


# ── 入口 ─────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Video2Doc Pro")
    app.setOrganizationName("Video2DocPro")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
