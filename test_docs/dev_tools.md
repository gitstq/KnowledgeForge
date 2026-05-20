# 开发者工具推荐

## 代码编辑器

### Visual Studio Code
- 免费开源
- 丰富的插件生态
- 内置Git支持
- 强大的调试功能

### PyCharm
- Python专用IDE
- 智能代码补全
- 内置测试工具
- 数据库工具集成

## 版本控制

### Git
分布式版本控制系统，必备技能。

常用命令：
```bash
git init
git add .
git commit -m "message"
git push origin main
git pull
git branch
git merge
```

### GitHub
- 代码托管平台
- 协作开发
- CI/CD集成
- 项目管理

## 终端工具

### 命令行增强
- **zsh** + **oh-my-zsh** - 强大的shell
- **tmux** - 终端复用器
- **fzf** - 模糊查找器

### 现代替代工具
- **ripgrep** - 快速搜索
- **fd** - 快速查找
- **bat** - 语法高亮cat
- **exa** - 现代化ls

## Docker

容器化平台，简化应用部署。

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## API测试

### Postman
- 图形化API测试工具
- 集合管理
- 环境变量
- 自动化测试

### curl
命令行HTTP客户端。

```bash
curl -X GET https://api.example.com/data
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com/submit
```

## 数据库工具

### DBeaver
- 通用数据库管理工具
- 支持多种数据库
- 可视化查询构建器

### TablePlus
- 现代化数据库GUI
- 简洁的界面
- 快速性能

## 生产力工具

- **Notion** - 知识管理
- **Obsidian** - 笔记工具
- **Alfred/Raycast** - 快捷启动器
- **Fig/Tabby** - 终端增强
