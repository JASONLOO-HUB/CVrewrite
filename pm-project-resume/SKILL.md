---
name: pm-project-resume
description: Use when turning a target JD, an existing product manager resume, and a project code repository into a PM-style project-experience entry grounded in repository context and original product intent, especially when source materials risk sounding too technical or overfit to the JD
type: workflow
---

# 产品经理项目经历生成

## 概述

这个 skill 处理的是一条完整工作流，不是单纯润色：

输入：

- 目标 JD
- 用户当前简历
- 项目的代码仓库

输出：

- 仓库上下文摘要
- 原始意图提炼
- JD 选点理由
- 最终项目经历成稿

目标不是把项目写得“像 JD”，而是：

先根据仓库和项目材料提炼**原始意图**，再做**有限度的 JD 包装**，最终产出一段像产品经理简历、但不把项目写成四不像的项目经历。

默认使用**通用产品经理语义**理解项目：

- 产品定位
- 目标用户
- 核心场景
- 用户路径
- 关键机制
- 业务闭环
- 增长 / 留存 / 商业化
- 产品判断

只有当仓库和项目材料明确表明它是游戏、AI 工具、内容平台、社区、B 端工具等特定类型产品时，才允许进一步落到行业语义层。

## 何时使用

在这些场景下使用：

- 用户要基于一个真实代码仓库，生成或修改产品经理简历里的 `项目经历`
- 输入通常同时包含 JD、原简历、项目仓库
- 用户希望内容贴合岗位，但不想过拟合 JD
- 项目材料里可能有 PRD / 设计文档 / 计划，也可能只有代码仓库

不要用于：

- 软件工程师简历
- 纯项目复盘文档
- 不依赖仓库上下文的简单文案润色

## 输入优先级

原始意图的来源优先级如下：

1. PRD、设计文档、需求说明、计划文档
2. 代码仓库本身
3. 原简历与 JD

解释：

- 如果存在 PRD、设计文档、计划文档，优先把它们视为项目原始意图
- 计划中的设计，一律按已经实现处理，可写进简历
- 代码仓库通常是最丰富的上下文来源，用来帮助理解项目如何展开、核心模块如何组织、真实产品主线是什么
- 原简历和 JD 主要用于判断“这个人是谁”“要找什么工作”“这个项目最适合补哪 1-2 个点”

如果没有 PRD 或设计文档，不要停下，直接以代码仓库为主提炼原始意图。

## 资源导航

- 仓库扫描与上下文优先级：读 [references/context-priority.md](references/context-priority.md)
- 贴 JD 但不过拟合：读 [references/jd-selection.md](references/jd-selection.md)
- 技术材料改写成产品经理语言：读 [references/pm-language.md](references/pm-language.md)
- 用 STAR + 产品业务周期写”原始意图提炼”：读 [references/star-pm-lifecycle.md](references/star-pm-lifecycle.md)
- 判断是否必须向用户澄清：读 [references/clarification-threshold.md](references/clarification-threshold.md)
- 正式输出前的主动自审：读 [references/self-review.md](references/self-review.md)
- 中间产物和最终交付结构：用 [assets/deliverable-template.md](assets/deliverable-template.md)
- 最终项目经历默认骨架：用 [assets/project-entry-template.md](assets/project-entry-template.md)

## 核心流程

### 1. 检查输入是否齐全

默认需要：

- JD
- 原简历
- 项目仓库路径

如果这三者缺少任意一项，先问一个简短澄清问题。

### 2. 先扫描仓库，不要直接写

必须先扫描仓库，建立上下文索引，再进入写作阶段。

扫描的目标不是做技术评审，而是过滤噪声、找到高价值文件：

**主动忽略以下内容：**
- 构建产物和依赖目录：`node_modules/`、`dist/`、`build/`、`vendor/`、`.next/`、`__pycache__/` 等
- 版本控制和 IDE 目录：`.git/`、`.vscode/`、`.idea/` 等
- 锁文件：`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`
- 测试快照、日志、临时文件
- 如果 JD 或原简历文件也放在仓库里，同样排除，避免污染项目上下文

**优先关注以下内容（按顺序）：**
1. 文档类：文件名含 `prd`、`spec`、`design`、`plan`、`roadmap`、`architecture` 的 `.md` / `.txt` 文件
2. 入口配置：`package.json`、`README.md`、主框架配置文件
3. 核心代码：页面 / 路由 / 场景层、核心模块、领域对象和数据结构

详细扫描规则见 [references/context-priority.md](references/context-priority.md)。

### 3. 范围收敛（扫描后立即判断）

扫描完成后，先判断仓库是否存在多主线、多应用、碎片化等情况。

**在进入材料阅读之前**，如果出现以下任意一种，必须先做范围收敛：

- monorepo / 单仓多应用，存在多条并列主线
- 用户提供了多个仓库或描述为「整套平台」
- 仓库碎片化，看不出稳定主线

范围未收敛时，不得进入步骤 4。按 [references/clarification-threshold.md](references/clarification-threshold.md) 的范围收敛模板提问。

### 4. 按优先级读材料

读材料顺序如下：

1. 仓库中存在的 PRD / 设计文档 / 计划文档
2. 入口文件、核心目录、关键代码文件
3. 原简历和 JD

不要一开始就围着 JD 写。
先用项目材料和仓库理解”这个项目原本是什么”，再决定怎么包装。

### 5. 先写”原始意图提炼”

在正式写简历前，先基于仓库上下文和项目材料，写一版**原始意图提炼**。

这一段必须同时满足：

- 使用 STAR 的结构组织理解
- 从产品经理的业务周期角度写

这里的重点不是结果复盘，而是回答：

- 项目本来想解决什么问题
- 核心场景和关键体验是什么
- 产品设计沿着什么业务周期展开
- 这个项目最像一个什么类型的产品，而不是什么技术系统

如果没有真实结果数据，`R` 不写进最终简历；中间推理里也只能写”目标结果 / 预期结果”，不能伪装成真实结果。

**检查点：** 原始意图提炼完成后，先输出这一段，再继续。不要跳过直接进入成稿。

### 6. 再做候选人与岗位的匹配判断

原简历 + JD 只用来回答两件事：

- 这个候选人是什么画像
- 这个项目最适合补哪 1-2 个岗位要点

不要试图让一段项目经历覆盖整个 JD。

### 7. 如果上下文仍不够，直接澄清

经过仓库扫描和材料阅读后，如果依然无法稳定判断原始意图，就不要硬写。

按 [references/clarification-threshold.md](references/clarification-threshold.md) 的规则，直接向用户提出简短澄清问题。

### 8. 再生成项目经历成稿

在原始意图已经清楚、JD 选点已经收敛的前提下，再生成最终简历文案。

默认格式：

- 一句项目概述
- 两条 bullet

默认结构：

- 第一条写产品定位 / 核心场景 / 系统抽象 / 产品判断
- 第二条写关键机制 / 用户路径 / 业务闭环 / 增长 / 留存 / 商业化中的第二层价值

### 9. 交付前必须主动自审

不要等用户指出”太技术了””太像文档了””太像贴 JD 了”才回改。

正式输出前，必须按 [references/self-review.md](references/self-review.md) 做一轮主动自审。

## 硬规则

### 原始意图优先于 JD

如果 JD 与项目原始意图发生张力，优先保留项目原始意图，只做有限度包装。

### 不要为了对齐 JD 过拟合改写

目标是“匹配”，不是“覆盖率”。

一段经历通常只包装 1-2 个最强匹配点，不要把所有岗位关键词塞进去。

### 写得像产品经理，不要写得像开发

优先写：

- 产品定位
- 核心场景 / 关键体验
- 系统抽象
- 用户路径
- 业务闭环
- 商业化闭环
- 冷启动 / 留存 / 长期成长机制 / 增长机制

如果行业类型尚不明确，优先用通用产品语言表达，不要默认把项目理解成游戏产品。

慎写：

- 前端 / 后端
- 接口 / 服务
- 数据库 / 缓存
- SDK / 包体 / 部署
- 纯技术架构叙述

## 输出标准

最终交付应让招聘方快速感受到：

- 这个人能从复杂仓库和项目材料中提炼产品原始意图
- 这个人能把复杂产品或复杂系统讲成产品经理语言
- 这个人能控制 JD 对齐力度，而不是为了关键词覆盖破坏项目主线
- 这段经历读起来像产品经理简历，而不是开发说明或设计文档
