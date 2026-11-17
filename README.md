# Research Paper Production Assistant

把选题、文献阅读、统计检查、论文写作、润色、科研绘图、审稿返修和组会汇报串联起来的 skill 工具包。

当前为 **本地第一版，面向非商业科研使用**。原创总控按需读取九个指定的上游 skill。上游快照独立下载，保留原目录与许可证，不把不同作者的提示词拼成一个文件。

## 模块

| 环节 | Skill | 来源 | 主许可证 |
|---|---|---|---|
| 选题 | brainstorming-research-ideas | [KalarisLabs/research-agent-skills](https://github.com/KalarisLabs/research-agent-skills) | MIT；另保留原始来源署名 |
| 文献阅读 | nature-reader | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Apache-2.0 |
| 统计检查 | statistical-analysis | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | MIT |
| 论文写作 | academic-paper | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | CC BY-NC 4.0 |
| 语言润色 | nature-polishing | Yuan1z0825/nature-skills | Apache-2.0 |
| 科研绘图 | nature-figure | Yuan1z0825/nature-skills | Apache-2.0；排除未明确授权图库 |
| 数据可视化 | scientific-visualization | K-Dense-AI/scientific-agent-skills | MIT |
| 审稿与复审 | academic-paper-reviewer | Imbad0202/academic-research-skills | CC BY-NC 4.0 |
| 组会汇报 | nature-paper2ppt | Yuan1z0825/nature-skills | Apache-2.0 |

来源是在 2026-11-17 按用户给出的名称匹配并选择的候选，不代表用户已确认这些就是最初看到的每一个版本。版本和下载校验值见 [sources.lock.json](sources.lock.json)。

## 使用

需要 Python 3.10+ 执行本项目下载及检查工具；具体分析、PDF 和 PPT 工作可能需要更高版本 Python、R、绘图/文档库及渲染器，按相应上游说明配置。

在项目根目录执行：

```powershell
python scripts/bootstrap.py
python scripts/validate.py
```

下载器只向 GitHub 获取固定提交的公开 ZIP，不执行下载内容，不安装包，不读取凭据。完整仓库布局保留在被 Git 忽略的 `.upstream/`，其中仅九个选定技能参与默认路由；已知未明确授权的 figures4papers 资产不提取。首次下载需要网络与磁盘空间。

在能够读取本地文件的代理中明确指定：

```text
请读取本项目 skills/research-paper-production-assistant/SKILL.md，
使用 Research Paper Production Assistant 帮我检查这篇稿件的统计报告。
目前只有论文正文，没有原始数据。
```

另一个例子：

```text
请使用本项目的 Research Paper Production Assistant，
先根据我提供的论文制作阅读笔记，再整理为 15 分钟中文组会 PPT。
```

总控依赖此仓库的相对布局，不能只把 SKILL.md 复制到全局技能目录。第一版没有修改全局技能配置，也没有自动注册插件。宿主支持文件读取即可显式调用。

## 整合行为

- 单项任务只加载相关 skill；多阶段任务共用证据、术语与分析版本。
- Nature Figure 主导图的叙事和面板设计，Scientific Visualization 主导数据编码、误差表达和可访问性检查。
- Reviewer 检查问题与修订证据；Academic Paper 负责正文修改和回复草稿。
- 没有原始数据时只做报告检查，不声称完成复算；没有全文时不声称完成全文阅读。
- 上游多代理、外部 API、付费服务及渲染器均取决于实际环境，不因下载技能而自动可用。

## GitHub 发布与许可

建议发布本仓库的原创总控、脚本、来源锁文件和说明；保留 `.gitignore`。不要把整个工作文件夹压缩上传：`.research/` 是审查缓存，`.upstream/` 是本地依赖，均不属于默认发布内容。

原创文件使用 MIT，见 [LICENSE](LICENSE)。这不会改变第三方许可证。两个 Academic skill 含非商业限制；免费发布也不能代替逐项遵守条款。完整来源与发现的素材例外见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 [审查记录](docs/source-audit.md)。

本项目与 Nature / Springer Nature 或各上游作者没有官方隶属或背书关系。Nature 字样保留在上游技能名称中。

## 验证范围

结构检查涵盖固定版本、选定入口、许可证文件、Nature manifest 本地依赖及已排除资产。它不是论文质量、统计方法正确性或所有上游脚本的安全保证。尚未用真实论文完成九模块端到端验收；具体科研任务仍需要对应材料、运行环境与结果检查。
