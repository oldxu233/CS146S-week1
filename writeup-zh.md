# 第 1 周 Write-up

## Part I：抓取

**环境配置**（足以让读者复现你的抓包）：
```
claude --version:  TODO
mitmproxy version: TODO
proxy command:     TODO
settings file:     TODO (路径 + env 块)
```

**本次会话。** 什么任务、针对哪个仓库，产生了多少个 `POST /v1/messages` 请求？
> TODO

| 要求 | 证据 |
|---|---|
| 触及 ≥ 2 个文件 | TODO |
| 至少失败一次 | TODO |
| 长到需要规划 | TODO |
| 你自己的仓库 | TODO |

**你对下文所引摘录做了哪些脱敏**，以及为什么：
> TODO


## Part II：系统提示词注解

**a. 结构。** 按顺序列出主要小节，每节一行说明它做什么，以及为什么是这个顺序。
> TODO

**b. 语气与冗长度。** 引用起控制作用的指令，然后说明它们在防御什么失败模式。
```
TODO
```
> TODO

**c. 何时不应行动。** 引用破坏性操作的闸门、范围限制或拒绝条件，以及每一条买到了什么。
```
TODO
```
> TODO

**d. 环境上下文。** 智能体被告知了关于机器/仓库/会话的哪些信息，以及这些信息位于请求中的什么位置（`system` 字段还是 `role: "system"` 消息）。
> TODO

**e. `<system-reminder>`。** 它们出现在哪里（举一个例子佐证），你能找到证据支撑的两种不同用途，以及为什么它们在对话中途被注入，而不是在一开始就声明一次。
```
TODO
```
> TODO


## Part III：工具设计注解

**清单。** 工具集合在各次请求之间是否有变化？如果有，是什么触发了它？

| Built-in | MCP | Deferred | **Total** | Changed mid-session? |
|---|---|---|---|---|
| TODO | TODO | TODO | **TODO** | TODO |

**两个工具。** 挑选彼此不同的工具。

| | 工具 1 | 工具 2 |
|---|---|---|
| 名称 | TODO | TODO |
| 关键 schema 字段 | TODO | TODO |
| 必需 vs. 可选 vs. 未暴露，及其原因 | TODO | TODO |
| 描述在防御……（引用 + 那件错误行为） | TODO | TODO |
| 刻意*不*做……以及这暗示了什么 | TODO | TODO |

为什么选这两个？
> TODO


## Part IV：行为分析

**每个回答都必须标注 `[OBSERVED]` 或 `[INFERRED]` 并引用其证据。未标注的回答不得分。**

**a. 错误恢复**：`TODO: label` · 证据：`TODO`

智能体看到的内容，逐字：
```
TODO
```
它接下来尝试了什么，以及恢复所用的轮数：
> TODO

**b. 规划**：`TODO: label` · 证据：`TODO`
> TODO

**c. 计划与任务状态**：`TODO: label` · 证据：`TODO` \
它是如何被创建和推进的？模型每一轮能看到关于任务状态的什么信息，以及这些信息位于请求中的什么位置：
> TODO

**d. 子智能体**：`TODO: label` · 证据：`TODO` \
当智能体进行委派时，子智能体被告知了什么，又返回了什么：
> TODO

**e. 上下文管理**：`TODO: label` · 证据：`TODO` \
随着会话增长，payload 中发生了什么变化：
> TODO


## Part V：反思

**你会照搬的两个决策**，及各自解决的问题：
1. TODO
2. TODO

**一个你会做得不同的决策**（论述它为何可能被那样设计）：
> TODO

**这次轨迹改变了的一件事**——关于你将如何引导一个编码智能体：
> TODO


## 提交
1. 用 `Command (⌘) + F` 搜索 `TODO`。没有结果说明你已完成。
2. 确认你的引用摘录中没有混入任何凭据或 `x-api-key` 头。
3. 把所有更改推送到你的远程仓库，并通过 Gradescope 提交。
4. 别忘了从你仓库的 `.claude/settings.json` 中移除 `ANTHROPIC_BASE_URL`！
