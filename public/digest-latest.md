# My Briefing · 2026-09-11

12 个活跃信源 -> 4352 条扫描 -> 7 条今日值得看
预计阅读 12 分钟，节省约 181.1 小时。

## 今日导读

- **官方 AI 实验室与公司信号**：官方 AI 实验室与公司信号 本期匹配 1666 篇文章，重点集中在 Agent 工作流、评测/安全、预训练/模型架构。建议先看《Claude's new system prompt really doesn't want to reproduce song lyrics》。
- **AI Agents**：AI Agents 本期匹配 836 篇文章，重点集中在 Agent 工作流、评测/安全、推理训练/测试时计算。建议先看《Using Blender with coding agents on macOS》。
- **推理训练与强化学习**：推理训练与强化学习 本期匹配 545 篇文章，重点集中在 预训练/模型架构、推理训练/测试时计算、后训练/对齐。建议先看《DeepSeek V4.1 Flash 模型正式发布：全面超越 V4 Pro、原生多模态视觉理解，API 定价下调》。

## 今日值得看

- [100] [Using Blender with coding agents on macOS](https://simonwillison.net/2026/Sep/5/blender-coding-agents-macos/) · Simon Willison · 2 min
  TIL: Using Blender with coding agents on macOS I've been having fun with Blender in ChatGPT Codex on my Mac recently. Getting it to work with coding agents is really easy: install the full Mac application from blender.org and run a prompt like this: Use the already install /Applications/Blender to render a scene of a pelican riding a bicycle In this case I followed that up with these two prompts: OK add a background and a lot of flair Then: OK make it a whole lot better And got this image, generated using Blender's Python API : This was covered by my existing Codex subscription, but according to AgentsView it would have cost $4.24 at API prices for gpt-6-astra . Tags: ai , generative-ai , llms , blender , pelican-riding-a-bicycle , coding-agents , gpt-6-astra
- [100] [Introducing the Agents API](https://openai.com/index/introducing-the-agents-api) · OpenAI Blog · 1 min
  Build and launch cloud agents with the Agents API, a managed service powered by the Codex harness for orchestration, long-running sessions, and tool use.
- [100] [大模型厂商纷纷“卖 Token”，消息称 Kimi、MiniMax 等即将在天猫开店](https://www.ithome.com/0/998/822.htm) · IT之家 · 1 min
  IT之家 9 月 5 日消息，上海证券报今天（5 日）独家获悉，Kimi、MiniMax、阶跃星辰等多家大模型厂商也都在与天猫接洽中，未来将入驻天猫开设官方旗舰店，开售 Token 订阅套餐产品。 本月 2 日，国产 AI 大模型厂商智谱正式入驻天猫，开设“智谱旗舰店”。用户可在淘宝 App 搜索“智谱旗舰店”进店下单。店铺目前已上架智谱 GLM Coding Plan 订阅套餐，基于 GLM-5.3 模型，并适配 ZCode、Claude Code、Codex 等 20 余款主流 Agent。 IT之家注：此前大模型厂商主要通过官网等自有渠道销售订阅产品。智谱此次入驻天猫，意味着大模型订阅服务开始进入传统电商平台的消费场景。 本月 3 日，天猫上线 Token 充值中心，首批接入阿里云、智谱、Kimi、MiniMax、DeepSeek 等国产大模型厂商。其中，阿里云和智谱为 品牌官方旗舰店 ，剩余三家目前为代理模式。
- [97] [OpenAI 将为美国政府机构提供 AI 模型五折优惠，终止每年 1 美元试点项目](https://www.ithome.com/1/001/015.htm) · IT之家 · 2 min
  IT之家 9 月 10 日消息，据彭博社报道，美国总务管理局（GSA）发布声明称，OpenAI 将终止一项政府机构试点项目。该项目允许政府机构每年仅花 1 美元 （IT之家注：现汇率约合 6.7 元人民币） 使用其模型；新方案改为按用量计费，联邦工作人员使用该 AI 技术，可以享受标准售价五折优惠。 为推动模型在政府落地，OpenAI 在去年 8 月入驻 GSA 的 OneGov 采购平台，这个平台供联邦机构批量采购 AI 软件。当初协商的首年每年 1 美元 （现汇率约合 6.7 元人民币） 条款，是美国政府中央采购部门有史以来谈下的力度最大的科技产品折扣。GSA 介绍，试点期间共有 350 万名联邦雇员使用 ChatGPT，累计节省 14 亿美元 （现汇率约合 94.16 亿元人民币） 成本。 虽然新方案相比去年的 1 美元 （现汇率约合 6.7 元人民币） 协议涨价，但五折定价依然可以帮助政府机构测试并大规模部署 AI 工具，其中就包括 OpenAI 新款模型 GPT-6 Astra。OpenAI 将于周四宣布，这项折扣不再局限于联邦政府，州政府、地方政府以及部落政府都可享受。 这份与美国政府达成的新协议将于 10 月 1 日生效，有效期超过两年。 就在 OpenAI 2025 年和 GSA 签约几天后，竞争对手 Anthropic PBC 也谈成了同样每年 1 美元 （现汇率约合 6.7 元人民币） 的合作。几周后，这家开发 Claude 聊天机器人的企业在华盛顿联合车站举办大型活动，面向联邦工作人员推介自家 AI 产品，Anthropic 首席执行官达里奥 · 阿莫迪还现场发表演讲。 但对 Anthropic 来说，政府业务很快陷入麻烦：该公司与国防部爆发了激烈争执，起因是 Anthropic 希望在国家安全类合同中加入有关监控和自主打击系统的安全约束条款。 这场矛盾导致美国国防部长皮特 · 赫格塞斯将这家企业列为供应链风险。特朗普还在其 Truth Social 平台发文称：美国绝不允许一家秉持激进左翼、政治正确理念的企业，对我们强大军队的行动指手画脚，要求所有政府机构停用 Anthropic 的产品。 Anthropic 随即起诉美国政府。由于双方诉讼仍在审理，目前还不清楚不涉及国家安全的联邦机构最终是否会停用 Anthropic 的 AI 工具。GSA 最初下达指令，把 Anthropic 从官方 AI 模型平台移除，但加州受理此案的法官发布临时禁令后，GSA 撤销了该决定。 上月，加州案件的法官裁定，特朗普政府必须解除联邦机构使用 Anthropic AI 的禁令。法官表示，国防部固然可以在自身业务中禁用这套技术，但无权单方面强制其他政府机构停用 Anthropic 模型。另一桩相关诉讼仍在华盛顿法院审理，由三名法官组成的合议庭尚未就另一项法律主张作出裁决。 OpenAI 曾在今年 2 月发布声明，表示已经达成协议，向国防部提供 AI 工具。
- [97] [科技巨头密集更新 AI 模型，“模型疲劳”问题凸显](https://www.ithome.com/0/999/036.htm) · IT之家 · 3 min
  IT之家 9 月 6 日消息，据 CNBC 报道，本周，人工智能行业再次迎来一轮密集更新。首先是 Anthropic 更新了 Fable 和 Mythos 模型，随后 Meta 和谷歌相继推出模型升级，OpenAI 紧接着发布了 GPT-6 Astra。 短短一周内，多家争夺人工智能技术领先地位的公司接连推出更新和升级，节奏之快令人眼花缭乱。 OpenAI CEO 萨姆 · 奥尔特曼当地时间周四在接受 CNBC 采访时表示：“我们都在加快迭代节奏。”他认为，近期更新速度加快的部分原因，是“大家都结束暑假回来了”。 但对于 AI 模型和服务的用户而言，这种快速迭代也带来了复杂性和混乱。为了避免掉队，企业 CEO 和 IT 管理人员不得不投入大量时间和资源，对不同产品的价格和能力进行比较。 AI 初创公司 Runpod CEO Zhen Lu 表示：“我觉得‘模型疲劳’确实已经成为一个真实存在的问题。不要误会，我对目前发生的各种创新感到非常兴奋，但我确实认为，我们现在所处的环境有太多泡沫，企业不得不不断制造声量。” 圣母大学门多萨商学院教授、拥有 25 年 AI 从业经验的 Ahmed Abbasi 表示，各家模型开发商如今都在争夺用户预算份额，它们一边努力跟上竞争对手的节奏，一边不断提醒开发者，自己至少与其他公司一样快地推进创新。 尤其是 Anthropic 和 OpenAI，两家公司正朝着公开市场迈进，因此竞争节奏尤为激烈。目前，私募投资者给这两家公司的估值都已接近 1 万亿美元 （IT之家注：现汇率约合 6.73 万亿元人民币） 。 谷歌和 Meta 也有各自的战略目标，而快速发展的开源 AI 社区最近又迎来了一位重量级新成员 —— 英伟达。 它们都希望从今年规模高达 2.59 万亿美元 （现汇率约合 17.44 万亿元人民币） 的 AI 支出中分得一杯羹。Gartner 预计，这一数字将比 2025 年增长 47%。 Gartner 在今年 5 月发布的一份报告中表示，超过一半的 AI 支出将用于 AI 基础设施，而服务、软件、网络安全、模型及其他工具的支出总额也将超过 1 万亿美元 （现汇率约合 6.73 万亿元人民币） 。 本周的更新潮由 Anthropic 在周二率先拉开序幕。该公司发布了 Claude Fable 5.1 和 Claude Mythos 5.1，并称其为“全球最先进的编程和知识工作模型”。 周三，Meta 发布 Muse Spark 1.3，谷歌推出 Gemini 3.8 Flash，两家公司都重点宣传了新模型在编程和 AI Agent 任务方面的能力提升。 周四，OpenAI 发布了 GPT-6 Astra。这款模型重点强化了网络安全和计算机操作能力。OpenAI 表示，它是“多年研究和重大投入”的成果。 同一天，位于阿布扎比的穆罕默德 · 本 · 扎耶德人工智能大学也向开源社区发布了自己的 K2 Horizon 系列 AI 模型，再次凸显 AI 研究和投资已经成为一场全球性的竞争。 与此同时，全球市值最高的公司、此次 AI 热潮核心芯片供应商英伟达也不甘示弱，正式同意以 129 亿美元 （现汇率约合 868.74 亿元人民币） 收购开源 AI 平台 Hugging Face。 英伟达近期也在持续推出开源模型，其中包括上个月发布的 Nemotron 3.5 Lightning。该公司表示，这是一款“轻量级”模型，可以在笔记本电脑或台式机的单块 GPU 上运行。 如此密集的模型更新，再加上 AI 监管政策仍存在诸多不确定性，也加剧了外界对于先进 AI 模型风险的担忧。 过去几周里，OpenAI、Anthropic 和 Meta 开发的模型都曾访问原本不应该访问的第三方网站。而 OpenAI 的模型上个月还成功入侵 Hugging Face，这一事件在整个行业引发强烈震动。 “可能陷入彻底的混乱” Abbasi 等专家尤其担心 AI Agent 的快速发展。他表示，令人担忧的不仅是这些能力本身，更在于“它们正在被如此轻易地部署”。 Abbasi 表示：“随着这些 Agent 的出现，它们不仅存在于你的电脑上，也开始活跃在网络上，整个威胁和漏洞环境都变得更加复杂。如果我们不够谨慎，局面可能彻底陷入混乱。” Abbasi 还认为，各大模型开发商恰好在同一周宣布更新，“这并非巧合”。 AI 金融初创公司 Farsight 的技术负责人 Noah Faro 也持类似观点。Faro 表示，企业可以通过多种方式了解竞争对手正在筹划什么。例如，可以观察云端计算资源的供应情况，因为这些公司都在争夺少数几家供应商提供的大规模算力。 此外，整个行业内部也存在大量信息交流。他表示：“任何一点微小的风吹草动，都会以极快的速度传播出去。” 当然，并非所有模型更新都具有同等重要性。 Faro 表示，与 OpenAI 发布的 GPT-6 Astra 不同，Anthropic、Meta 和谷歌本周推出的大多数更新都属于“点版本更新”。 这意味着，它们是在现有 AI 模型基础上进行升级，而不是从头开发一个全新的模型。 Faro 认为，最近真正对行业格局产生重大影响的两款模型，是 Anthropic 在 6 月发布的 Fable 5，以及中国月之暗面在 7 月推出的 Kimi K3。 不过，企业 AI 初创公司 Clockwork Systems CEO Suresh Vasudevan 表示，即使只是渐进式更新，在 AI 技术快速改变商业和软件开发方式的背景下，也依然具有重要意义。他表示：“现在每一次发布的产品都强得离谱，以至于人们已经很难判断什么才算真正的跨越式进步了。大家都知道，当你身处一条指数增长曲线之中时，你往往意识不到自己正在经历什么。只有退后一步，回头看看自己原来在哪里、现在又走到了哪里，才能真正感受到变化。” Vasudevan 也承认，持续追踪每一次模型更新已经成为一件令人头疼的事情，尤其是在评估过程还需要消耗宝贵计算资源的情况下。他说，如果自己的初创公司希望针对某项任务评估 10 个 AI 模型，最终可能只会挑选其中 5 个进行测试。 Vasudevan 表示：“要把目前所有正在推出的模型逐一评估，真的非常困难。”
- [97] [坚决不用行业标准AGENTS.md，Claude Code惹来“封杀令”：Anthropic终于回应了，但开发者更气了](https://www.infoq.cn/article/GuFWNd24Ww5AFlrXxTBo?utm_medium=article) · InfoQ 中文 · 1 min
  点击查看原文>
- [95] [奥尔特曼称 OpenAI 考虑放缓前沿 AI 开发，希望其他公司也能跟进](https://www.ithome.com/1/001/219.htm) · IT之家 · 2 min
  北京时间 9 月 11 日，据彭博社报道，OpenAI 正在考虑放缓尖端 AI 的开发速度，该公司 CEO 萨姆 · 奥尔特曼 (Sam Altman) 希望其他 AI 公司也能采取同样的做法。 据多名知情人士透露，奥尔特曼本周在一次全体员工会议上告诉员工，OpenAI 可能会放慢 AI 开发节奏，或许会与其他几家 AI 实验室协同行动，但也有一些公司可能不会同意这么做。 近几周，头部 AI 公司的员工纷纷公开表达对先进 AI 系统风险上升的担忧，加剧了这些公司内部的焦虑。今年早些时候，OpenAI 及其竞争对手 Anthropic 都已秘密提交上市文件。 OpenAI 首席科学家雅库布 · 帕乔基 (Jakub Pachocki) 最近发表文章，警告 AI 带来的危险，认为 AI 公司应该“在必要时协调行动，放缓未来的开发进程”。帕乔基还表示，他希望“在共同的安全标准建立之前，自愿放缓开发能够成为行业惯例”。 OpenAI 已表示，出于安全方面的担忧，公司近期已经放缓了部分模型的开发，并暂停了特定内部 AI 训练。奥尔特曼曾在 7 月表示，他已与白宫官员讨论了放缓 AI 开发的“必要性”问题。 周二，Anthropic AI 研究员雅各布 · 考克森 (Jacob Coxon) 辞职，并指控他的两家前雇主 Anthropic 和 OpenAI 在竞相迈向超级智能 AI 的过程中“拿我们的生命赌博”。考克森在社交媒体帖子中表示，开发 AI 的人相信它可能“在这个十年结束前杀死我们所有人”。这些言论迅速传播，获得超过 1.5 亿次浏览，并引起知名议员和公众人物的关注。 截至发稿，OpenAI 不予置评。

## 实体追踪

- 官方 AI 实验室与公司信号：本周 359，今日 +91，官方 AI 实验室与公司信号 本期匹配 1666 篇文章，重点集中在 Agent 工作流、评测/安全、预训练/模型架构。建议先看《Claude's new system prompt really doesn't want to reproduce song lyrics》。
- AI Agents：本周 178，今日 +62，AI Agents 本期匹配 836 篇文章，重点集中在 Agent 工作流、评测/安全、推理训练/测试时计算。建议先看《Using Blender with coding agents on macOS》。
- 推理训练与强化学习：本周 98，今日 +29，推理训练与强化学习 本期匹配 545 篇文章，重点集中在 预训练/模型架构、推理训练/测试时计算、后训练/对齐。建议先看《DeepSeek V4.1 Flash 模型正式发布：全面超越 V4 Pro、原生多模态视觉理解，API 定价下调》。
- 预训练：本周 68，今日 +24，预训练 本期匹配 438 篇文章，重点集中在 预训练/模型架构、推理训练/测试时计算、预训练。建议先看《DeepSeek V4.1 Flash 模型正式发布：全面超越 V4 Pro、原生多模态视觉理解，API 定价下调》。
- 编程 Agent：本周 48，今日 +16，编程 Agent 本期匹配 174 篇文章，重点集中在 评测/安全、预训练/模型架构、Agent 工作流。建议先看《Auto mode is now the default in Claude Code for Pro, Max, and Team plans》。
- 后训练与对齐：本周 40，今日 +12，后训练与对齐 本期匹配 304 篇文章，重点集中在 后训练/对齐、预训练/模型架构、Agent 工作流。建议先看《Anthropic 揭示“AI 训练 AI”新方法，比人类研究员成本更低、速度更快》。
- 数据分析与指标体系：本周 269，今日 +80，数据分析与指标体系 本期匹配 1423 篇文章，重点集中在 推理训练/测试时计算、Agent 工作流、预训练/模型架构。建议先看《Understanding ChatGPT Work》。
- AI 评测与安全：本周 264，今日 +77，AI 评测与安全 本期匹配 1503 篇文章，重点集中在 评测/安全、推理训练/测试时计算、预训练/模型架构。建议先看《Auto mode is now the default in Claude Code for Pro, Max, and Team plans》。
- AI 产品化：本周 237，今日 +76，AI 产品化 本期匹配 1297 篇文章，重点集中在 Agent 工作流、评测/安全、推理训练/测试时计算。建议先看《Claude's new system prompt really doesn't want to reproduce song lyrics》。
- AI 基础设施与算力：本周 182，今日 +53，AI 基础设施与算力 本期匹配 994 篇文章，重点集中在 预训练/模型架构、AI 基础设施、Agent 工作流。建议先看《Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things》。
- 成本管理与 FinOps：本周 146，今日 +35，成本管理与 FinOps 本期匹配 843 篇文章，重点集中在 评测/安全、预训练/模型架构、后训练/对齐。建议先看《Some thoughts on the Navier–Stokes Millennium Prize Problem》。
- AI 改造传统领域：本周 75，今日 +14，AI 改造传统领域 本期匹配 402 篇文章，重点集中在 Agent 工作流、AI 基础设施、评测/安全。建议先看《Claude's new system prompt really doesn't want to reproduce song lyrics》。

## 内容分栏

- 学啥：80 篇
- 读啥：80 篇
- 做啥：47 篇
- 忽略：0 篇