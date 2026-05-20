#!/usr/bin/env python3
"""
KnowledgeForge - 轻量级本地AI知识库构建引擎
Lightweight Local AI Knowledge Base Building Engine CLI

核心功能：
- 本地文档索引（支持Markdown、PDF、TXT、代码文件等）
- 语义搜索与相似度匹配
- RAG问答支持
- 零依赖（仅使用Python标准库）
- 纯文本向量化和相似度计算
"""

import os
import sys
import json
import re
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import argparse

__version__ = "1.0.0"
__author__ = "KnowledgeForge Team"

# =============================================================================
# 配置常量
# =============================================================================
DEFAULT_CONFIG = {
    "index_dir": ".knowledge_forge",
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k": 5,
    "supported_extensions": [".md", ".txt", ".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".html", ".css", ".json", ".yaml", ".yml"],
    "ignore_patterns": [".git", "__pycache__", "node_modules", ".knowledge_forge", "*.pyc", ".env", ".venv"]
}

# =============================================================================
# 终端UI组件
# =============================================================================
class Colors:
    """终端颜色定义"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"

class UI:
    """终端UI工具类"""
    
    @staticmethod
    def print_banner():
        """打印应用横幅"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   {Colors.BOLD}📚 KnowledgeForge{Colors.RESET}{Colors.CYAN} - 轻量级本地AI知识库构建引擎{Colors.RESET}{Colors.CYAN}          ║
║                                                                  ║
║   {Colors.DIM}Lightweight Local AI Knowledge Base Building Engine{Colors.RESET}{Colors.CYAN}           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)
    
    @staticmethod
    def info(msg: str):
        print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")
    
    @staticmethod
    def success(msg: str):
        print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
    
    @staticmethod
    def warning(msg: str):
        print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")
    
    @staticmethod
    def error(msg: str):
        print(f"{Colors.RED}❌ {msg}{Colors.RESET}")
    
    @staticmethod
    def progress(current: int, total: int, prefix: str = "Progress"):
        """显示进度条"""
        percent = int(100 * current / total) if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r{Colors.CYAN}{prefix}: [{bar}] {percent}% ({current}/{total}){Colors.RESET}", end="", flush=True)
        if current >= total:
            print()
    
    @staticmethod
    def box(title: str, content: str, width: int = 60):
        """绘制内容框"""
        lines = content.split("\n")
        print(f"{Colors.CYAN}┌{'─' * (width - 2)}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.BOLD} {title:<{width-4}}{Colors.RESET}{Colors.CYAN} │{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * (width - 2)}┤{Colors.RESET}")
        for line in lines:
            print(f"{Colors.CYAN}│{Colors.RESET} {line:<{width-4}}{Colors.CYAN} │{Colors.RESET}")
        print(f"{Colors.CYAN}└{'─' * (width - 2)}┘{Colors.RESET}")

# =============================================================================
# 文本处理工具
# =============================================================================
class TextProcessor:
    """文本处理工具类"""
    
    # 常用停用词
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "must", "shall", "can", "need", "dare",
        "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him",
        "her", "us", "them", "my", "your", "his", "her", "its", "our", "their", "from", "as", "not",
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也",
        "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那"
    }
    
    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """分词 - 使用简单规则"""
        # 转换为小写
        text = text.lower()
        # 提取单词和中文字符
        tokens = re.findall(r'[a-z]+|[\u4e00-\u9fff]', text)
        # 过滤停用词和短词
        return [t for t in tokens if len(t) > 1 and t not in cls.STOP_WORDS]
    
    @classmethod
    def chunk_text(cls, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """将文本分块"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            # 尝试在句子边界分割
            if end < text_len:
                for sep in ["\n\n", "\n", "。", ". ", "! ", "? "]:
                    pos = text.rfind(sep, start, end)
                    if pos != -1:
                        end = pos + len(sep)
                        break
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "start": start,
                    "end": end,
                    "tokens": cls.tokenize(chunk_text)
                })
            
            start = end - overlap if end < text_len else text_len
        
        return chunks
    
    @classmethod
    def compute_tf(cls, tokens: List[str]) -> Dict[str, float]:
        """计算词频(TF)"""
        tf = defaultdict(int)
        for token in tokens:
            tf[token] += 1
        total = len(tokens) if tokens else 1
        return {k: v / total for k, v in tf.items()}
    
    @classmethod
    def compute_idf(cls, documents: List[List[str]]) -> Dict[str, float]:
        """计算逆文档频率(IDF)"""
        import math
        idf = {}
        total_docs = len(documents)
        
        # 统计每个词出现在多少文档中
        doc_freq = defaultdict(int)
        for doc in documents:
            seen = set(doc)
            for token in seen:
                doc_freq[token] += 1
        
        # 计算IDF
        for token, freq in doc_freq.items():
            idf[token] = math.log((total_docs + 1) / (freq + 1)) + 1
        
        return idf
    
    @classmethod
    def compute_tf_idf(cls, tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
        """计算TF-IDF向量"""
        tf = cls.compute_tf(tokens)
        return {k: tf[k] * idf.get(k, 0) for k in tf}
    
    @classmethod
    def cosine_similarity(cls, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算余弦相似度"""
        import math
        
        # 获取所有维度
        all_keys = set(vec1.keys()) | set(vec2.keys())
        
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in all_keys)
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

# =============================================================================
# 文件处理器
# =============================================================================
class FileHandler:
    """文件处理工具类"""
    
    @staticmethod
    def should_ignore(path: Path, ignore_patterns: List[str]) -> bool:
        """检查是否应该忽略该路径"""
        path_str = str(path)
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True
            if path.name.startswith(pattern.replace("*", "")):
                return True
        return False
    
    @staticmethod
    def read_file(filepath: Path) -> str:
        """读取文件内容"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            UI.warning(f"无法读取文件 {filepath}: {e}")
            return ""
    
    @classmethod
    def scan_directory(cls, root_path: Path, config: Dict) -> List[Path]:
        """扫描目录获取所有支持的文件"""
        files = []
        extensions = config.get("supported_extensions", DEFAULT_CONFIG["supported_extensions"])
        ignore_patterns = config.get("ignore_patterns", DEFAULT_CONFIG["ignore_patterns"])
        
        for path in root_path.rglob("*"):
            if path.is_file():
                if cls.should_ignore(path, ignore_patterns):
                    continue
                if path.suffix.lower() in extensions:
                    files.append(path)
        
        return sorted(files)

# =============================================================================
# 知识库索引
# =============================================================================
class KnowledgeIndex:
    """知识库索引管理"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.index_dir = base_path / DEFAULT_CONFIG["index_dir"]
        self.index_file = self.index_dir / "index.json"
        self.config_file = self.index_dir / "config.json"
        self.index_data = {"documents": {}, "chunks": [], "stats": {}}
        self.config = DEFAULT_CONFIG.copy()
        self.idf = {}
        
        self._ensure_index_dir()
        self._load_config()
    
    def _ensure_index_dir(self):
        """确保索引目录存在"""
        self.index_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception as e:
                UI.warning(f"加载配置失败: {e}")
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            UI.error(f"保存配置失败: {e}")
    
    def load(self) -> bool:
        """加载索引"""
        if not self.index_file.exists():
            return False
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index_data = json.load(f)
            
            # 重新计算IDF
            all_tokens = [chunk.get("tokens", []) for chunk in self.index_data.get("chunks", [])]
            self.idf = TextProcessor.compute_idf(all_tokens)
            
            return True
        except Exception as e:
            UI.error(f"加载索引失败: {e}")
            return False
    
    def save(self):
        """保存索引"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            UI.error(f"保存索引失败: {e}")
    
    def build(self, force: bool = False):
        """构建索引"""
        if not force and self.load():
            UI.info("已加载现有索引，使用 --force 重新构建")
            return
        
        UI.info(f"开始扫描目录: {self.base_path}")
        
        files = FileHandler.scan_directory(self.base_path, self.config)
        UI.info(f"找到 {len(files)} 个文件")
        
        if not files:
            UI.warning("没有找到可索引的文件")
            return
        
        # 重置索引
        self.index_data = {"documents": {}, "chunks": [], "stats": {}}
        all_chunks_tokens = []
        
        for i, filepath in enumerate(files):
            UI.progress(i + 1, len(files), "索引文件")
            
            # 计算文件哈希
            content = FileHandler.read_file(filepath)
            if not content:
                continue
            
            file_hash = hashlib.md5(content.encode()).hexdigest()
            rel_path = str(filepath.relative_to(self.base_path))
            
            # 分块
            chunks = TextProcessor.chunk_text(
                content,
                self.config["chunk_size"],
                self.config["chunk_overlap"]
            )
            
            # 存储文档信息
            self.index_data["documents"][rel_path] = {
                "hash": file_hash,
                "size": len(content),
                "chunks": len(chunks),
                "modified": os.path.getmtime(filepath)
            }
            
            # 存储块信息
            for j, chunk in enumerate(chunks):
                chunk_id = f"{rel_path}#{j}"
                chunk_data = {
                    "id": chunk_id,
                    "file": rel_path,
                    "text": chunk["text"],
                    "start": chunk["start"],
                    "end": chunk["end"],
                    "tokens": chunk["tokens"]
                }
                self.index_data["chunks"].append(chunk_data)
                all_chunks_tokens.append(chunk["tokens"])
        
        print()  # 换行
        
        # 计算全局IDF
        UI.info("计算TF-IDF权重...")
        self.idf = TextProcessor.compute_idf(all_chunks_tokens)
        
        # 更新统计
        self.index_data["stats"] = {
            "total_files": len(files),
            "total_chunks": len(self.index_data["chunks"]),
            "indexed_at": time.time(),
            "vocabulary_size": len(self.idf)
        }
        
        # 保存索引
        self.save()
        self._save_config()
        
        UI.success(f"索引构建完成！")
        UI.info(f"  - 文档数: {len(files)}")
        UI.info(f"  - 块数: {len(self.index_data['chunks'])}")
        UI.info(f"  - 词汇表大小: {len(self.idf)}")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """语义搜索"""
        if top_k is None:
            top_k = self.config["top_k"]
        
        if not self.index_data["chunks"]:
            UI.error("索引为空，请先运行 build 命令")
            return []
        
        # 处理查询
        query_tokens = TextProcessor.tokenize(query)
        query_vector = TextProcessor.compute_tf_idf(query_tokens, self.idf)
        
        # 计算相似度
        results = []
        for chunk in self.index_data["chunks"]:
            chunk_vector = TextProcessor.compute_tf_idf(chunk.get("tokens", []), self.idf)
            similarity = TextProcessor.cosine_similarity(query_vector, chunk_vector)
            
            if similarity > 0:
                results.append({
                    "id": chunk["id"],
                    "file": chunk["file"],
                    "text": chunk["text"],
                    "similarity": similarity
                })
        
        # 排序并返回前K个
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def stats(self):
        """显示索引统计"""
        if not self.index_data["stats"]:
            UI.error("索引为空，请先运行 build 命令")
            return
        
        stats = self.index_data["stats"]
        docs = self.index_data["documents"]
        
        UI.box("📊 索引统计", f"""
总文档数: {stats.get('total_files', 0)}
总块数: {stats.get('total_chunks', 0)}
词汇表大小: {stats.get('vocabulary_size', 0)}
索引时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.get('indexed_at', 0)))}
        """)
        
        if docs:
            print(f"\n{Colors.CYAN}📁 已索引文档 (前10个):{Colors.RESET}")
            for i, (path, info) in enumerate(list(docs.items())[:10]):
                size_kb = info.get('size', 0) / 1024
                print(f"  {Colors.DIM}{i+1}.{Colors.RESET} {path} {Colors.DIM}({size_kb:.1f} KB, {info.get('chunks', 0)} 块){Colors.RESET}")

# =============================================================================
# RAG问答
# =============================================================================
class RAGEngine:
    """RAG问答引擎"""
    
    def __init__(self, index: KnowledgeIndex):
        self.index = index
    
    def answer(self, question: str, context_chunks: int = 3) -> Dict:
        """基于检索的问答"""
        # 检索相关块
        results = self.index.search(question, top_k=context_chunks)
        
        if not results:
            return {
                "answer": "抱歉，没有找到相关信息。",
                "sources": []
            }
        
        # 构建上下文
        context = "\n\n".join([
            f"[来源: {r['file']}]\n{r['text']}" 
            for r in results
        ])
        
        # 生成答案（简化版，实际可接入LLM）
        answer = self._generate_answer(question, context, results)
        
        return {
            "answer": answer,
            "sources": results
        }
    
    def _generate_answer(self, question: str, context: str, results: List[Dict]) -> str:
        """生成答案（基于检索结果的摘要）"""
        # 提取最相关的文本片段
        best_match = results[0] if results else None
        
        if not best_match:
            return "无法找到相关信息。"
        
        # 简单的答案生成逻辑
        answer = f"基于知识库检索，找到以下内容：\n\n"
        
        for i, r in enumerate(results, 1):
            similarity_pct = r['similarity'] * 100
            text_preview = r['text'][:200] + "..." if len(r['text']) > 200 else r['text']
            answer += f"{i}. [{r['file']}] (相关度: {similarity_pct:.1f}%)\n{text_preview}\n\n"
        
        return answer.strip()

# =============================================================================
# 命令行接口
# =============================================================================
def cmd_init(args):
    """初始化知识库"""
    UI.print_banner()
    
    path = Path(args.path).resolve()
    if not path.exists():
        UI.error(f"路径不存在: {path}")
        return
    
    index = KnowledgeIndex(path)
    index._save_config()
    
    UI.success(f"已在 {path / DEFAULT_CONFIG['index_dir']} 初始化知识库")
    UI.info("配置文件已创建，您可以编辑 config.json 调整参数")

def cmd_build(args):
    """构建索引"""
    UI.print_banner()
    
    path = Path(args.path).resolve()
    if not path.exists():
        UI.error(f"路径不存在: {path}")
        return
    
    index = KnowledgeIndex(path)
    index.build(force=args.force)

def cmd_search(args):
    """搜索知识库"""
    UI.print_banner()
    
    path = Path(args.path).resolve()
    index = KnowledgeIndex(path)
    
    if not index.load():
        UI.error("索引不存在，请先运行 build 命令")
        return
    
    query = args.query
    top_k = args.top_k or index.config["top_k"]
    
    UI.info(f"搜索: {query}")
    results = index.search(query, top_k=top_k)
    
    if not results:
        UI.warning("没有找到相关结果")
        return
    
    print(f"\n{Colors.CYAN}🔍 搜索结果 (Top {len(results)}):{Colors.RESET}\n")
    
    for i, r in enumerate(results, 1):
        similarity = r['similarity'] * 100
        color = Colors.GREEN if similarity > 50 else (Colors.YELLOW if similarity > 20 else Colors.RED)
        
        print(f"{Colors.BOLD}{i}.{Colors.RESET} {color}[{similarity:.1f}%]{Colors.RESET} {Colors.CYAN}{r['file']}{Colors.RESET}")
        text_preview = r['text'][:150] + "..." if len(r['text']) > 150 else r['text']
        print(f"   {Colors.DIM}{text_preview}{Colors.RESET}\n")

def cmd_chat(args):
    """RAG问答模式"""
    UI.print_banner()
    
    path = Path(args.path).resolve()
    index = KnowledgeIndex(path)
    
    if not index.load():
        UI.error("索引不存在，请先运行 build 命令")
        return
    
    rag = RAGEngine(index)
    
    print(f"\n{Colors.CYAN}💬 RAG问答模式 - 输入问题开始对话 (输入 'quit' 退出){Colors.RESET}\n")
    
    while True:
        try:
            question = input(f"{Colors.GREEN}你: {Colors.RESET}").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if not question:
                continue
            
            result = rag.answer(question, context_chunks=args.context)
            
            print(f"\n{Colors.CYAN}🤖 KnowledgeForge:{Colors.RESET}")
            print(result['answer'])
            print()
            
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            break
    
    print(f"\n{Colors.CYAN}再见！👋{Colors.RESET}")

def cmd_stats(args):
    """显示统计信息"""
    UI.print_banner()
    
    path = Path(args.path).resolve()
    index = KnowledgeIndex(path)
    
    if not index.load():
        UI.error("索引不存在，请先运行 build 命令")
        return
    
    index.stats()

def main():
    parser = argparse.ArgumentParser(
        description="KnowledgeForge - 轻量级本地AI知识库构建引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s init ./my-docs              # 初始化知识库
  %(prog)s build ./my-docs             # 构建索引
  %(prog)s search ./my-docs "关键词"    # 搜索
  %(prog)s chat ./my-docs              # 问答模式
  %(prog)s stats ./my-docs             # 查看统计
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化知识库")
    init_parser.add_argument("path", nargs="?", default=".", help="目标目录 (默认: 当前目录)")
    
    # build 命令
    build_parser = subparsers.add_parser("build", help="构建索引")
    build_parser.add_argument("path", nargs="?", default=".", help="目标目录 (默认: 当前目录)")
    build_parser.add_argument("-f", "--force", action="store_true", help="强制重新构建")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索知识库")
    search_parser.add_argument("path", help="知识库目录")
    search_parser.add_argument("query", help="搜索查询")
    search_parser.add_argument("-k", "--top-k", type=int, help="返回结果数量")
    
    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="RAG问答模式")
    chat_parser.add_argument("path", help="知识库目录")
    chat_parser.add_argument("-c", "--context", type=int, default=3, help="上下文块数")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="显示统计信息")
    stats_parser.add_argument("path", nargs="?", default=".", help="知识库目录")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    commands = {
        "init": cmd_init,
        "build": cmd_build,
        "search": cmd_search,
        "chat": cmd_chat,
        "stats": cmd_stats
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
