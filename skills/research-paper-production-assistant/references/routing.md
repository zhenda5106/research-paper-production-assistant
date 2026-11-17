# Provider routing

All paths below are relative to the toolkit repository root. Read only the provider needed now.

| Stage | Provider entrypoint | Dispatch rule |
|---|---|---|
| 选题 | `.upstream/ideas/skills/brainstorming-research-ideas/SKILL.md` | Explore and rank research questions; distinguish proposed novelty from verified novelty. |
| 文献阅读 | `.upstream/nature/skills/nature-reader/SKILL.md` | Read supplied papers, translate requested excerpts, or build a bilingual reader. A full reader is not required for a narrow question. |
| 统计检查 | `.upstream/scientific/skills/statistical-analysis/SKILL.md` | Separate raw-data analysis, design/power advice, and manuscript reporting checks. |
| 论文写作 | `.upstream/academic/academic-paper/SKILL.md` | Choose the matching mode, e.g. outline, abstract, drafting or revision. Preserve author evidence and target discipline. |
| 润色 | `.upstream/nature/skills/nature-polishing/SKILL.md` | Improve language within the requested scope; preserve findings and qualifications. |
| 科研绘图 | `.upstream/nature/skills/nature-figure/SKILL.md` | Lead figure narrative, panel arrangement, editable schematics and journal-oriented styling. |
| 数据可视化 | `.upstream/scientific/skills/scientific-visualization/SKILL.md` | Lead Python data encodings, uncertainty, accessibility and export checking. Combine with Nature Figure for complex data figures without duplicate rendering. |
| 审稿／复审 | `.upstream/academic/academic-paper-reviewer/SKILL.md` | Produce critique or verify revisions; findings remain separate from manuscript edits. |
| 组会汇报 | `.upstream/nature/skills/nature-paper2ppt/SKILL.md` | Build a paper-based presentation with evidence figures and speaker notes. |

## Figures

For a data figure using both providers, agree one figure brief, one analysis version and one renderer. Nature Figure supplies the panel narrative; Scientific Visualization supplies data-encoding checks. Respect an existing Python/R choice. For R workflows, do not add a second Python plotting pipeline just because the visualization provider uses Python. Transfer relevant visualization principles and use the R-capable Nature Figure route.

## Revision loop

1. Reviewer: map comments to concrete, located issues; use re-review if changes already exist.
2. Academic Paper: use revision-coach/revision as appropriate to plan or apply authorized changes and draft responses.
3. Reviewer: check each response against the revised manuscript and evidence.

Do not say a response resolves an issue solely because it is persuasive. Do not perform unlimited revision loops; complete the user's requested scope and report residual issues requiring data or author judgment.

## Dependency boundaries

Nature providers require sibling `skills/nature-shared/`. Academic providers use repository-root `shared/`, `scripts/` and other resources. The bootstrap retains repository layout rather than copying bare entrypoints.

Additional upstream skills may be present in snapshots but are not automatically selected. A literature reader does not by itself implement a comprehensive database search or systematic review. If such work is requested, identify the necessary capability and available tools rather than silently claiming complete search coverage.
