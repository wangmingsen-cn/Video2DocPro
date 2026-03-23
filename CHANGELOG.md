# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-03-23

### Added
- Stable architecture: EXE only handles UI, processing via subprocess
- Beautiful dark-themed PyQt6 interface
- Real-time progress bar and log output
- Support for single video and batch processing
- Auto-detection of Python and project paths

### Changed
- Completely refactored packaging architecture
- Smaller EXE size (~60MB)
- More stable runtime experience

### Fixed
- Resolved torch DLL loading issues in packaged environment
- Fixed whisper import conflicts

## [1.3.0] - 2026-03-23

### Added
- Simplified GUI interface
- Settings dialog for AI API configuration
- Multiple AI provider support (DeepSeek, OpenAI, Zhipu, Baidu)

### Changed
- Improved processing flow
- Better error handling

## [1.2.0] - 2026-03-23

### Added
- DeepSeek API integration
- AI-generated content displayed at top of HTML
- Summary, mind map, and detailed notes

### Changed
- Enhanced HTML template design
- Added cover image generation

## [1.1.0] - 2026-03-23

### Added
- Batch processing support
- Directory scanning for videos
- Progress tracking

### Fixed
- Fixed FFmpeg path issues
- Fixed Chinese filename encoding

## [1.0.0] - 2026-03-23

### Added
- Video analysis (FFmpeg)
- Audio extraction
- Keyframe extraction
- Whisper speech-to-text
- HTML document generation
- Markdown document generation
- Basic PyQt6 GUI

---

## Roadmap

### v2.0 (Planned)
- [ ] Subtitle export (SRT, VTT)
- [ ] Video segment clipping
- [ ] Multi-language AI summaries
- [ ] Cloud storage integration

### v2.1 (Planned)
- [ ] Web version
- [ ] Mobile adaptation
- [ ] API service

### v2.2 (Planned)
- [ ] Plugin system
- [ ] Custom templates
- [ ] Team collaboration
