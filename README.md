<div align="center">

# 📚 KnowledgeForge

**轻量级本地AI知识库构建引擎 | Lightweight Local AI Knowledge Base Building Engine**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-yellow.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

KnowledgeForge 是一个**零依赖**、**轻量级**的本地AI知识库构建引擎，专为开发者和知识工作者设计。它让您能够在本地环境中快速构建、索引和搜索个人知识库，无需连接外部API或云服务。

#### 灵感来源

本项目灵感来源于当前AI领域对RAG（检索增强生成）技术的需求增长，以及用户对数据隐私和本地化的关注。我们希望提供一个简单、高效、完全本地运行的知识管理解决方案。

#### 核心价值

- 🔒 **完全本地化** - 所有数据处理在本地完成，保护隐私
- 🚀 **零依赖设计** - 仅使用Python标准库，无需安装额外包
- ⚡ **高效索引** - 基于TF-IDF的智能文本分块和向量化
- 🎯 **语义搜索** - 支持基于内容的相似度检索
- 💬 **RAG问答** - 检索增强生成，提供上下文感知的答案

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📄 **多格式支持** | 支持Markdown、代码文件、文本文件等多种格式 | ✅ |
| 🔍 **语义搜索** | 基于TF-IDF的智能相似度匹配 | ✅ |
| 🧠 **RAG问答** | 检索增强生成，上下文感知的问答 | ✅ |
| 📊 **分块索引** | 智能文本分块，支持重叠区域 | ✅ |
| 🌐 **多语言** | 支持中文、英文等多种语言 | ✅ |
| 🎨 **美观TUI** | 彩色终端界面，进度条显示 | ✅ |
| ⚙️ **可配置** | 支持自定义分块大小、忽略模式等 | ✅ |

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- 无需额外依赖

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/KnowledgeForge.git
cd KnowledgeForge

# 直接运行（推荐）
python3 main.py --help

# 或安装为命令
pip install -e .
knowledge-forge --help
```

#### 基本使用

```bash
# 1. 初始化知识库
python3 main.py init ./my-docs

# 2. 构建索引
python3 main.py build ./my-docs

# 3. 搜索
python3 main.py search ./my-docs "Python编程"

# 4. RAG问答模式
python3 main.py chat ./my-docs

# 5. 查看统计
python3 main.py stats ./my-docs
```

### 📖 详细使用指南

#### 命令说明

| 命令 | 描述 | 示例 |
|------|------|------|
| `init` | 初始化知识库目录 | `kforge init ./docs` |
| `build` | 构建/更新索引 | `kforge build ./docs --force` |
| `search` | 语义搜索 | `kforge search ./docs "关键词"` |
| `chat` | RAG问答模式 | `kforge chat ./docs` |
| `stats` | 查看统计信息 | `kforge stats ./docs` |

#### 配置文件

初始化后会生成 `.knowledge_forge/config.json`：

```json
{
  "index_dir": ".knowledge_forge",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "top_k": 5,
  "supported_extensions": [".md", ".txt", ".py", ".js", ...],
  "ignore_patterns": [".git", "__pycache__", "node_modules"]
}
```

### 💡 设计思路与迭代规划

#### 技术选型

- **纯Python标准库** - 确保零依赖，易于部署
- **TF-IDF向量化** - 轻量级但有效的文本表示方法
- **余弦相似度** - 经典的向量相似度计算
- **智能分块** - 基于句子边界的文本分割

#### 后续规划

- [ ] PDF文件支持
- [ ] HTML网页索引
- [ ] 与LLM API集成（OpenAI、Claude等）
- [ ] Web界面
- [ ] 增量索引更新
- [ ] 向量数据库集成（可选）

### 📦 打包与部署

#### 作为Python包安装

```bash
pip install -e .
```

#### 打包为可执行文件

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name knowledge-forge main.py
```

### 🤝 贡献指南

欢迎提交Issue和PR！请确保：

1. 代码符合PEP 8规范
2. 添加适当的测试
3. 更新文档

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

KnowledgeForge 是一個**零依賴**、**輕量級**的本地AI知識庫構建引擎，專為開發者和知識工作者設計。它讓您能夠在本地環境中快速構建、索引和搜尋個人知識庫，無需連接外部API或雲服務。

#### 核心價值

- 🔒 **完全本地化** - 所有資料處理在本地完成，保護隱私
- 🚀 **零依賴設計** - 僅使用Python標準庫，無需安裝額外包
- ⚡ **高效索引** - 基於TF-IDF的智慧文字分塊和向量化
- 🎯 **語義搜尋** - 支援基於內容的相似度檢索
- 💬 **RAG問答** - 檢索增強生成，提供上下文感知的答案

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📄 **多格式支援** | 支援Markdown、程式碼檔案、文字檔案等多種格式 | ✅ |
| 🔍 **語義搜尋** | 基於TF-IDF的智慧相似度匹配 | ✅ |
| 🧠 **RAG問答** | 檢索增強生成，上下文感知的問答 | ✅ |
| 📊 **分塊索引** | 智慧文字分塊，支援重疊區域 | ✅ |
| 🌐 **多語言** | 支援中文、英文等多種語言 | ✅ |
| 🎨 **美觀TUI** | 彩色終端介面，進度條顯示 | ✅ |

### 🚀 快速開始

```bash
# 1. 初始化知識庫
python3 main.py init ./my-docs

# 2. 構建索引
python3 main.py build ./my-docs

# 3. 搜尋
python3 main.py search ./my-docs "Python程式設計"

# 4. RAG問答模式
python3 main.py chat ./my-docs
```

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

KnowledgeForge is a **zero-dependency**, **lightweight** local AI knowledge base building engine designed for developers and knowledge workers. It enables you to quickly build, index, and search your personal knowledge base locally without connecting to external APIs or cloud services.

#### Core Values

- 🔒 **Fully Local** - All data processing happens locally, protecting your privacy
- 🚀 **Zero Dependencies** - Uses only Python standard library, no extra packages needed
- ⚡ **Efficient Indexing** - Smart text chunking and vectorization based on TF-IDF
- 🎯 **Semantic Search** - Content-based similarity retrieval
- 💬 **RAG Q&A** - Retrieval-Augmented Generation for context-aware answers

### ✨ Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📄 **Multi-format Support** | Supports Markdown, code files, text files, and more | ✅ |
| 🔍 **Semantic Search** | Intelligent similarity matching based on TF-IDF | ✅ |
| 🧠 **RAG Q&A** | Retrieval-Augmented Generation with context awareness | ✅ |
| 📊 **Chunked Indexing** | Smart text chunking with overlap support | ✅ |
| 🌐 **Multi-language** | Supports Chinese, English, and more | ✅ |
| 🎨 **Beautiful TUI** | Colorful terminal interface with progress bars | ✅ |

### 🚀 Quick Start

#### Requirements

- Python 3.8 or higher
- No additional dependencies required

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/KnowledgeForge.git
cd KnowledgeForge

# Run directly (recommended)
python3 main.py --help

# Or install as a command
pip install -e .
knowledge-forge --help
```

#### Basic Usage

```bash
# 1. Initialize knowledge base
python3 main.py init ./my-docs

# 2. Build index
python3 main.py build ./my-docs

# 3. Search
python3 main.py search ./my-docs "Python programming"

# 4. RAG chat mode
python3 main.py chat ./my-docs

# 5. View statistics
python3 main.py stats ./my-docs
```

### 📖 Detailed Usage Guide

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize knowledge base directory | `kforge init ./docs` |
| `build` | Build/update index | `kforge build ./docs --force` |
| `search` | Semantic search | `kforge search ./docs "keywords"` |
| `chat` | RAG Q&A mode | `kforge chat ./docs` |
| `stats` | View statistics | `kforge stats ./docs` |

#### Configuration

After initialization, `.knowledge_forge/config.json` is generated:

```json
{
  "index_dir": ".knowledge_forge",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "top_k": 5,
  "supported_extensions": [".md", ".txt", ".py", ".js", ...],
  "ignore_patterns": [".git", "__pycache__", "node_modules"]
}
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices

- **Pure Python Standard Library** - Ensures zero dependencies and easy deployment
- **TF-IDF Vectorization** - Lightweight yet effective text representation
- **Cosine Similarity** - Classic vector similarity calculation
- **Smart Chunking** - Sentence boundary-based text segmentation

#### Roadmap

- [ ] PDF file support
- [ ] HTML web page indexing
- [ ] LLM API integration (OpenAI, Claude, etc.)
- [ ] Web interface
- [ ] Incremental index updates
- [ ] Vector database integration (optional)

### 📦 Packaging & Deployment

#### Install as Python Package

```bash
pip install -e .
```

#### Package as Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --name knowledge-forge main.py
```

### 🤝 Contributing

Issues and PRs are welcome! Please ensure:

1. Code follows PEP 8 style guide
2. Add appropriate tests
3. Update documentation

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by KnowledgeForge Team**

[⭐ Star us on GitHub](https://github.com/gitstq/KnowledgeForge) | [🐛 Report Issue](https://github.com/gitstq/KnowledgeForge/issues)

</div>
