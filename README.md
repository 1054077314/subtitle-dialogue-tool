# YouTube 字幕对话稿人物标注项目文档

## 项目目标

输入 YouTube 自动字幕或英文字幕文本，系统自动清洗字幕、分块处理、识别对话人物，并输出带人物标识的对话稿，方便阅读、整理和二次使用。

## 文档结构

```text
docs/
├── 01-requirements.md          # 需求文档
├── 02-project-design.md        # 项目设计文档
├── 03-module-split.md          # 模块拆分文档
├── 04-task-plan.md             # 开发计划文档
├── 05-data-format.md           # 数据格式约定
├── 06-ai-prompt-plan.md        # AI 提示词方案
├── 07-acceptance-smoke.md      # 验收与测试清单
└── CLAUDE.md                   # AI 开发规则
```

## 推荐开发顺序

```text
字幕文本输入
→ 字幕清洗
→ 字幕分块
→ 单块人物识别
→ 结构化 JSON 输出
→ 多块结果合并
→ 全局人物统一
→ 导出 Markdown 对话稿
```

## 第一版范围

第一版只做最小闭环：

```text
输入字幕文本 → 清洗 → 分块 → 调用大模型识别人物 → 输出 Markdown 对话稿
```

暂时不做：

- YouTube 自动下载
- 登录系统
- 数据库
- 多用户管理
- 前端复杂 UI
- 视频播放同步
