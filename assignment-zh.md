# 第 1 周：一次真实 Claude Code 会话的轨迹剖析

## 作业概述

本周，你将把一个真实的 Claude Code 会话放到代理（proxy）后面，抓取它实际发出的 HTTP 请求，并**对这些请求进行剖析**。你不是在构建任何新东西，而是以足够细致的粒度去阅读一个生产级系统，细到它的设计决策变得可见。

### 学习目标

- **追踪（Trace）** 一次来自生产级编码智能体的真实编码会话，理解其调用结构。
- **识别（Identify）** 在一个非平凡的编码任务中，提示词（prompting）、工具 schema 与模型响应是如何相互作用的。
- **反思（Reflect）** 在你自己的自定义智能体中，哪些行为你会照搬，哪些你会做出不同选择。

## 材料

- **[Intercepting Claude Code Requests](https://www.ai.moda/en/blog/tutorial-intercepting-claude-code-requests)**：本作业所基于的技术方案，请先阅读。
- **[Anthropic Messages API 参考](https://docs.claude.com/en/api/messages)**：你将阅读的请求结构（`system`、`tools`、`messages`）。
- **[Claude Code 设置参考](https://docs.claude.com/en/docs/claude-code/settings)**：用户级（`~/.claude/settings.json`）与项目级（`.claude/settings.json`）设置的工作方式。

## 环境准备

**前置条件：Claude Code**。斯坦福通过你的 SUNet ID 提供 Claude Code 访问权限。如果你尚未激活账号，请先[申请访问权限](https://uit.stanford.edu/service/claude)，然后[安装并登录](https://code.claude.com/docs/en/setup)。账号获批且安装完成后，用 `claude --version` 确认，并在你的 writeup 中记录该版本号。

**1. 安装 mitmproxy：**

- **macOS**：`brew install --cask mitmproxy`。
- **Windows**：从 [mitmproxy.org](https://mitmproxy.org/) 运行安装程序，它会把 `mitmweb` 放到你的 `PATH` 中。
- **Linux 或任意平台**：`pip install mitmproxy`，如果你创建了课程 conda 环境，就在该环境中执行。

**2. 以反向代理模式启动它：**

```bash
mitmweb --listen-host 127.0.0.1 --listen-port 58888 \
        --web-open-browser --mode reverse:https://api.anthropic.com \
        -w session.flows
```

发往 `127.0.0.1:58888` 的流量会被转发到真实 API；检查界面会在 `http://localhost:8081` 打开。反向模式下，你只需把 Claude Code 指向一个纯 HTTP 的本地地址，因此无需安装 CA 证书。`-w session.flows` 会把每个 flow 保存到磁盘；请从**任何 git 仓库之外**的目录运行该命令，以免抓包文件被意外提交。

**3. 把 Claude Code 指向它**：在你用于 Part I 的仓库中，创建一个**项目级**的 `.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:58888",
    "ENABLE_TOOL_SEARCH": "true"
  }
}
```

> ⚠️ **不要把它放进 `~/.claude/settings.json`！** 否则你机器上的任何 Claude Code 会话都会进入你的抓包（并且一旦停掉 `mitmweb`，会话将无法工作）。

**4. 验证**：启动一个新的 `claude` 会话，随便发送点内容，确认 mitmweb 中出现了 `POST /v1/messages` flow。

**5. 作业完成后**：完成后，删除仓库里的 `.claude/settings.json`（或其中的 `env` 块），并停止 `mitmweb`。

## Part I：抓取一次会话（15 分）

在代理下运行**一次**会话，满足全部四项要求：

1. **多文件（Multi-file）**：至少触及两个文件。
2. **至少失败一次（Fails at least once）**：你需要一段错误恢复序列。故意弄坏一个测试是最可靠的获得方式。
3. **长到需要规划（Long enough to plan）**：智能体应当做出明确的计划，而不是只发起一次工具调用：任务列表、plan mode，或一个 plan 文件。
4. **你自己的仓库（Your own repo）**：一个临时项目，不是本仓库。

**任务灵感**，如果你不想自己发明一个：

- 删除一个被其他模块 import 的函数，然后要求 Claude 在测试通过的前提下恢复完整功能。
- 给一个小的 Web 应用添加一个 endpoint 以及相应测试，然后要求它在一个你并未安装的依赖版本上让测试套件通过。
- 重命名一个模块并让它更新每一处 import，然后运行 lint 和测试。
- 要求一个需要陌生库的特性，这样智能体在写任何代码之前必须先查阅 API。

在 mitmweb UI 中，选中一个 `POST /v1/messages` flow，把**请求体**下载为 JSON。把它们保存在本地。你不需要提交它们，但后续每一部分都会依据从中得出的证据来评分，因此要保留足够多的内容来支撑你的回答。

如果你的 mitmweb 会话中止了，你可以从保存的 `session.flows` 文件继续工作：用 `mitmweb -r session.flows` 重新打开它。

### ⚠️ 对你引用的内容做脱敏

你的抓包中包含你自己的源代码、文件路径和凭据。除了你在 `writeup.md` 中刻意引用的片段之外，任何内容都不应进入仓库。

- 绝不要粘贴原始 flow 或 HTTP 头，因为 `x-api-key` / `authorization` 就在那里。
- **请求体同样可能包含机密。** 智能体读取过的任何内容（`.env`、配置文件、命令输出）都会在 `messages` 中被重放。引用工具结果之前请先检查。
- 让 `session.flows` 远离任何 git 仓库。
- 引用中的私密内容请用可见标记（如 `[REDACTED: internal hostname]`）遮盖，而不是悄无声息地删除。
- 如果某段摘录在不破坏其含义的前提下无法脱敏，请在一个一次性仓库上重新抓包。

## Part II：为系统提示词做注解（25 分）

把 `system` 块以及任何 `role: "system"` 的消息拆解为各个小节。对每一节回答：**这段内容买到了什么行为，又在防御什么失败模式？** 要的是注解，不是摘要。

至少覆盖：

- **结构（Structure）**：主要小节、它们的顺序，以及为什么是这个顺序。
- **语气与冗长度（Tone and verbosity）**：控制回复长度与格式的具体措辞，以及为什么它值得花这些 token。
- **何时不应行动（When not to act）**：破坏性操作的闸门、范围限制、拒绝条件。
- **环境上下文（Environment context）**：智能体被告知了关于机器、仓库和会话的哪些信息，以及这些信息位于请求中的什么位置。

然后，专门针对 `<system-reminder>`：它们出现在哪里（system 块、messages，还是两者都有——请举一个例子佐证），你能找到证据支撑的两种不同用途是什么，以及为什么它们在对话中途被注入，而不是一开始就声明一次？

## Part III：为工具设计做注解（25 分）

**清单：要数字，不要散文。** 当时有多少个工具可用，按内置（built-in）vs. MCP 提供 vs. 延迟/可搜索（deferred/searchable）分类？注意工具集合在各次请求之间是否有过变化，以及是什么触发了它。一个好的回答读起来是*"第一个请求中有 117 个工具：35 个内置，来自三个 MCP server 的 82 个"*，而不是*"有很多工具可用"*。

**设计分析。** 挑选**两个**工具，各自作为接口设计来分析：

- 复现 schema 中的相关部分。
- 为什么是这组参数？哪些是必需的，哪些是可选的，哪些是被刻意不暴露的？
- 描述在防御什么？成熟智能体里的工具描述大多是累积下来的伤疤组织。找出一句仅仅因为模型总是做错某事才存在的描述，并指出那件错事是什么。
- 这个工具刻意*不*做什么，这又暗示了周边系统是什么样的？

挑两个彼此不同的工具。两个文件操作类工具是弱选择；一个文件工具搭配一个编排（orchestration）工具，或者搭配一个具有不寻常失败契约的工具，才是强选择。

## Part IV：基于证据的行为分析（25 分）

用你自己的轨迹回答每个问题。每个回答都必须**引用其证据**（哪个请求、message 索引、tool call），并**标注 `[OBSERVED]` 或 `[INFERRED]`**：observed 意味着你能在抓包中指向它，inferred 意味着你在没有实际观察其发生的情况下依据定义进行推理。两者都可以接受；错误标注则不行，未标注的回答不得分。

- **错误恢复（Error recovery）**：完整走通一次失败。智能体看到了什么，它接下来尝试了什么，恢复花了多少轮？请逐字引用。
- **规划（Planning）**：是某个工具、某句提示词指令、涌现行为，还是它们的组合？哪些证据能把它们区分开？
- **计划与任务状态（Plans and task state）**：计划是如何被创建和推进的？模型每一轮能看到关于任务状态的什么信息，这些信息位于请求中的什么位置？
- **子智能体（Subagents）**：智能体何时进行委派？子智能体被告知了什么，又返回了什么？（如果你的会话从未触发过，一个诚实的 `[INFERRED]` 也是可以的。）
- **上下文管理（Context management）**：随着会话增长，payload 中发生了什么变化？更早的轮次在后来是如何被表示的？

## Part V：反思（10 分）

最多一页：**你会照搬的两个决策**及各自解决的问题；**一个你会做得不同的决策**，并论述它为何可能被那样设计；以及**这次轨迹改变了的一件事**——关于你日复一日将如何引导一个编码智能体。

## 交付物

一份完成的 **`week1/writeup.md`**，其中每个 `TODO` 都已填写。你抓取的轨迹留在你自己的机器上。

## 评分细则（总计 100 分）

| 部分 | 分值 | 怎样拿满分 |
|---|---|---|
| I. 抓取与可复现性 | 15 | 四项会话要求全部满足；环境配置与会话记录详尽到仅凭你的 writeup 就能复现 |
| II. 系统提示词注解 | 25 | 各小节与行为和失败模式挂钩；`<system-reminder>` 有引用示例的说明 |
| III. 工具清单与设计 | 25 | 有具体数字与分类拆解；两个真正不同的工具被作为接口设计来分析 |
| IV. 行为分析 | 25 | 每个回答都有引用且标注正确；错误恢复部分逐字引用 |
| V. 反思 | 10 | 立场具体、有论证，而非复述 |

引用片段中出现未脱敏的凭据，以及把轨迹并不支持的论断当作观察来陈述，都会被扣分。

## 提交说明

1. 确保所有更改已推送到你的远程仓库以供评分。
2. **确保你已将 `mihail911`、`isaackann` 和 `vdaita` 添加为你作业仓库的协作者。**
3. 通过 Gradescope 提交。
4. **别忘了从你仓库的 `.claude/settings.json` 中移除 `ANTHROPIC_BASE_URL`！**
