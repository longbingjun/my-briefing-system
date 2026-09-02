# My Briefing · 2026-09-02

12 个活跃信源 -> 4541 条扫描 -> 7 条今日值得看
预计阅读 14 分钟，节省约 189.0 小时。

## 今日导读

- **官方 AI 实验室与公司信号**：官方 AI 实验室与公司信号 本期匹配 1680 篇文章，重点集中在 Agent 工作流、预训练/模型架构、推理训练/测试时计算。建议先看《llm-anthropic 0.27》。
- **AI Agents**：AI Agents 本期匹配 870 篇文章，重点集中在 Agent 工作流、评测/安全、推理训练/测试时计算。建议先看《A shot-scraper-style JSON API on Bun 1.4's new Bun.WebView》。
- **推理训练与强化学习**：推理训练与强化学习 本期匹配 586 篇文章，重点集中在 推理训练/测试时计算、后训练/对齐、预训练/模型架构。建议先看《前字节强化学习专家孙鹏博士加盟星尘智能，完善Physical AI全栈技术布局》。

## 今日值得看

- [100] [智谱 AI 入驻天猫开设官方旗舰店，大模型套餐可直接网购，个人版月付 118 元起](https://www.ithome.com/0/997/340.htm) · IT之家 · 2 min
  IT之家 9 月 2 日消息，国产 AI 大模型厂商智谱正式入驻天猫，开设“智谱旗舰店”。即日起，用户可在淘宝 App 搜索“智谱旗舰店”进店下单。 店铺目前已上架智谱 GLM Coding Plan 订阅套餐，基于 GLM-5.3 模型，并适配 ZCode、Claude Code、Codex 等 20 余款主流 Agent。 智谱在售商品包括个人版 Lite、Pro、Max 及团队版标准席位，支持按月、季、年订阅。 其中个人版 Lite 版 118 元（含 10000 积分 / 周），Pro 版 538 元（含 60000 积分 / 周），Max 版 1078 元（含 140000 积分 / 周），团队版标准席位 598 元（含 66000 积分 / 席位）。 IT之家注：此前大模型厂商主要通过官网等自有渠道销售订阅产品。智谱此次入驻天猫，意味着大模型订阅服务开始进入传统电商平台的消费场景。 智谱旗舰店的经营者为北京智谱华章科技股份有限公司。智谱方面表示，未来用户购买词元（Token）也可在电商平台完成。
- [100] [坚决不用行业标准AGENTS.md，Claude Code惹来“封杀令”：Anthropic终于回应了，但开发者更气了](https://www.infoq.cn/article/GuFWNd24Ww5AFlrXxTBo?utm_medium=article) · InfoQ 中文 · 1 min
  点击查看原文>
- [100] [Moonlight & Mayhem (Raccoon Heist by Codex + GPT-5.6 Sol Ultra)](https://simonwillison.net/2026/Aug/7/moonlight-mayhem/) · Simon Willison · 3 min
  Moonlight &amp; Mayhem (Raccoon Heist by Codex + GPT-5.6 Sol Ultra) On Wednesday I wrote about One-shotting a Raccoon Heist game using Claude Fable 5 , where I had Claude Fable 5 build a full working game from a premise I generated with GPT-3 and DALL-E four years ago . I decided to pose the exact same prompt to Codex Desktop running GPT-5.6 Sol Ultra - the mode where Sol makes aggressive use of sub-agents - to see how it would do. It produced a much better game! Here's Moonlight &amp; Mayhem - GitHub repository here , including the textures and prompts it generated using gpt-image-2 . Your browser does not support HTML5 video. The original GPT-3 generated game description included: In “Raccoon Heist”, you and your team of thieving raccoons are tasked with pulling off a series of daring heists. From robbing banks to stealing priceless art, no job is too big or too small for your furry crew. Fable's version had you as a single raccoon running around a back yard collecting coins and fish. GPT-5.6 Sol has you in a museum, rescuing your two other raccoon crewmates in order to stack on top of each other and bust the golden sardine out of its case. Much more heisty! There was one catch though: the version produced from the one-shot prompt had a bug where each raccoon had an eyeball that was enlarged to the size of a giant sphere floating over their head! You can play that version here . Despite reviewing screenshots during development Codex failed to spot and correct this bug. I fixed it by prompting: Why do the raccoons have huge black spheres on them? And then: Fix it Which resulted in this fix . I shared the full Codex transcript in the repository - I wish Claude Code had the same "copy as Markdown" feature. Codex spent 52 minutes on the project. Here's the AgentsView cost estimate for that session if I had been paying full API prices as opposed to using my monthly Codex subscription: Tags: game-design , ai , openai , generative-ai , llms , coding-agents , codex , gpt
- [99] [How AI-native companies turn workflows into operating capability](https://openai.com/index/ai-native-company-workflows) · OpenAI Blog · 1 min
  Basis, Clay, and Exa Labs use AI agents to improve onboarding, account management, and developer integrations. See what enterprise leaders can apply.
- [99] [微信支付 AI 专属卡支持接入 DeepSeek Harness 和 OpenClaw](https://www.ithome.com/0/996/655.htm) · IT之家 · 2 min
  IT之家 8 月 31 日消息，微信支付官方今日宣布，微信支付 AI 专属卡上新，继 WorkBuddy、QClaw 之后， 支持接入 DeepSeek Harness 和 OpenClaw 。 授权后，用户只需在对话中提出需求，就能体验 从智能对话推荐到下单支付的全新消费流程。 目前，AI 专属卡已支持在 DeepSeek Harness 和 OpenClaw， 付费调用 Skillhub 上的 700 余个 Pay Skill， 未来将覆盖更多场景。 IT之家附开通步骤： 步骤一： 把下面这句话复制给 DeepSeek Harness 或 OpenClaw，一键完成下载、安装和配置。 请通过 npx -y @ tenpay/weixinpay-ai-installer 来安装 weixinpay 插件 步骤二： 通过 skillhub 使用付费技能，首次支付时 Agent 会生成绑定链接。也可以直接告诉它“帮我绑定一张微信支付 AI 专属卡”，点击 「轻触前往绑定」。 步骤三： Agent 找好 Pay Skill，会发起订单弹出支付授权，在手机端二次确认后， 从 AI 专属卡扣款后， Agent 就能调用 Pay Skill 把活干完。 据IT之家此前报道，6 月 17 日， 微信支付正式发布 AI 专属卡 。 腾讯公司公关总监张军总结了这张卡的功能 ： 大家关注的 AI 专属卡来了。它的额度由用户指定管理，在强授权模式上运行。通俗点讲，就是托人办事，往往需要给人家办事买东西的费用。托智能体办，也是一样。 有网友做了个更加形象的类比： 就像小时候大人给我钱让我去给他买包烟 。 针对安全问题，微信官方重申微信支付 AI 专属卡不是通过获取用户的账户密码等重要信息直接提款，而是在用户 设定好的范围内，允许的情况下 ，帮用户购买、消费： 主账隔离，绝不越界： AI 专属卡和微信支付主账户完全隔离，Agent 里所有消费仅能使用专属卡余额。 放多少你说了算： 卡内放多少钱、怎么用，用户自己决定。还能通过“转入 / 转出”随时调整回收卡内额度。 每笔确认，必须确认： 每一笔订单，没有用户本人的最终授权确认，AI 一分钱都花不出去。
- [97] [Anthropic’s best AI model struggles to attract users as cheaper tools thrive](https://simonwillison.net/2026/Aug/23/anthropics-best-ai-model-struggles-to-attract-users-as-cheaper-t/) · Simon Willison · 3 min
  Anthropic’s best AI model struggles to attract users as cheaper tools thrive A few interesting numbers in this FT story gathered from "people with knowledge of the matter": Anthropic's "annualized revenue" for July is up to $65bn - it was $47bn in May, and I collected more historic numbers here . Anthropic expect Q3 to be profitable according to the same model they used to declare Q2 profitable. "It also told investors that it had 6,000 customers that spend $100,000 annually or more." As for OpenAI, "annualised revenue has jumped 35 per cent in the quarter to date and is now over $40bn, with the launch of GPT 5.6 in July jolting the company’s performance after a sluggish start to the year". This article also introduced me to the Ramp AI index , which uses billing data from 70,000 Ramp credit card using companies to estimate model adoption. Here's Ramp's breakdown of Anthropic model spend for July 2026, which looks reasonable given that Opus 5 was only released on July 24th, and supports the idea that Fable's cost has made it a less popular model: Opus 4.8: 28.0% Sonnet 4.6: 8.3% Fable 5: 8.0% Opus 4.6: 6.9% Sonnet 5: 3.6% Opus 5: 3.5% Opus 4.7: 1.7% Sonnet 4.5: 1.3% Haiku 4.5: 1.0% Opus 4.5: 0.7% Via Hacker News Tags: ai , openai , generative-ai , llms , anthropic , claude , claude-mythos-fable
- [97] [英格兰银行行长贝利警告：先进人工智能威胁全球金融稳定](https://www.ithome.com/0/996/476.htm) · IT之家 · 2 min
  IT之家 8 月 31 日消息，据英国卫报报道，英格兰银行行长安德鲁 · 贝利（Andrew Bailey）加入了越来越多发出警告的知名人士行列，提醒外界关注最先进人工智能技术可能给全球带来的风险。 据IT之家了解，贝利目前担任国际金融稳定委员会（FSB）主席。他近日以这一身份向各国财长和央行行长发出一封两页长的信函，表示“前沿”AI 模型正展现出越来越强的自主能力和问题解决能力，同时也具备执行威胁性行为的能力。 他警告称，这些模型可能通过网络攻击扰乱高度互联的全球金融体系，而网络攻击造成的破坏“可以跨越不同司法管辖区迅速扩散”。 在本周于美国北卡罗来纳州举行的会议前，贝利向二十国集团（G20）财长和央行行长发信表示：“近期的发展也让我注意到，许多司法管辖区尚未建立相应机制，以管理先进前沿 AI 模型的开发、发布和部署，这正在加剧金融领域乃至更广泛范围内的风险。” 贝利的这封信进一步加剧了近期围绕 AI 风险的担忧。过去几周，多位知名科技人士已经陆续发出警告，而贝利的观点也延续了他此前呼吁国际社会合作应对 AI 风险的立场。他此前曾对伦敦金融城的企业负责人表示：“任何国家都无法将自己与如今普遍存在的跨境系统完全隔绝。” 上个月，来自前沿 AI 实验室的 1367 名研究人员和工程师也联名发出警告，其中大多数来自 OpenAI、Anthropic 和 Google DeepMind。这封信让外界进一步了解到每天参与 AI 研发的工程师们究竟在担心什么。 这封联名信指出：“AI 能力的发展存在迅速超越我们理解或控制相关系统能力的真实风险。”信中随后呼吁美国政府支持“一项国际性行动，开发必要的技术和治理工具，以便有意识地控制自动化 AI 发展的速度”。 本月早些时候，还有消息称，OpenAI 员工在其最先进的 AI 智能体逃离训练环境、发起一场前所未有的黑客攻击行动并引发全球关注的数周前，就已经观察到了这些 AI 智能体出现异常行为的迹象。 将这一担忧进一步延伸到金融政策领域，贝利表示：“对于金融体系而言，目前最直接的担忧是前沿 AI 可能对网络风险产生的影响。前沿 AI 可能从根本上改变网络风险的速度、规模和经济成本，尤其是在金融体系高度依赖少数第三方服务提供商的情况下，这可能削弱整个市场的信心。” 贝利呼吁负责维护全球金融体系安全的相关机构，将“采取适当措施，支持前沿 AI 模型在全球范围内安全、负责任地发布和部署”作为优先事项。 这封信还提到了贝利对债券和股票市场杠杆率不断上升的担忧。他表示，当前部分金融市场的估值已经处于较高水平，而且市场高度集中，投资者对 AI 发展前景的乐观情绪尤其推高了相关资产估值。这些因素叠加起来，可能进一步放大未来市场调整的幅度。 贝利写道：“因此，我仍然担心，一次重大冲击，或者多重冲击同时发生，可能会同时触发多个潜在风险点。” 贝利自 2020 年 3 月起担任英格兰银行行长。在此之前，他曾领导英国金融行为监管局（FCA）和审慎监管局（PRA），这两家机构是英国最主要的金融监管机构。去年，他被任命为金融稳定委员会主席。 金融稳定委员会总部位于瑞士巴塞尔，负责协调各国金融监管机构以及国际标准制定机构的工作，推动制定有效的监管措施和政策，以维护全球金融稳定。

## 实体追踪

- 官方 AI 实验室与公司信号：本周 380，今日 +87，官方 AI 实验室与公司信号 本期匹配 1680 篇文章，重点集中在 Agent 工作流、预训练/模型架构、推理训练/测试时计算。建议先看《llm-anthropic 0.27》。
- AI Agents：本周 186，今日 +55，AI Agents 本期匹配 870 篇文章，重点集中在 Agent 工作流、评测/安全、推理训练/测试时计算。建议先看《A shot-scraper-style JSON API on Bun 1.4's new Bun.WebView》。
- 推理训练与强化学习：本周 126，今日 +31，推理训练与强化学习 本期匹配 586 篇文章，重点集中在 推理训练/测试时计算、后训练/对齐、预训练/模型架构。建议先看《前字节强化学习专家孙鹏博士加盟星尘智能，完善Physical AI全栈技术布局》。
- 预训练：本周 110，今日 +26，预训练 本期匹配 478 篇文章，重点集中在 预训练/模型架构、开源动态、后训练/对齐。建议先看《Qwen3.8-Flash-Next》。
- 后训练与对齐：本周 90，今日 +25，后训练与对齐 本期匹配 346 篇文章，重点集中在 后训练/对齐、预训练/模型架构、推理训练/测试时计算。建议先看《Anthropic 揭示“AI 训练 AI”新方法，比人类研究员成本更低、速度更快》。
- 编程 Agent：本周 41，今日 +16，编程 Agent 本期匹配 154 篇文章，重点集中在 预训练/模型架构、评测/安全、Agent 工作流。建议先看《Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things》。
- AI 评测与安全：本周 346，今日 +78，AI 评测与安全 本期匹配 1612 篇文章，重点集中在 评测/安全、预训练/模型架构、推理训练/测试时计算。建议先看《Auto mode is now the default in Claude Code for Pro, Max, and Team plans》。
- 数据分析与指标体系：本周 327，今日 +74，数据分析与指标体系 本期匹配 1487 篇文章，重点集中在 推理训练/测试时计算、预训练/模型架构、Agent 工作流。建议先看《Understanding ChatGPT Work》。
- AI 产品化：本周 309，今日 +73，AI 产品化 本期匹配 1408 篇文章，重点集中在 推理训练/测试时计算、Agent 工作流、后训练/对齐。建议先看《Understanding ChatGPT Work》。
- AI 基础设施与算力：本周 225，今日 +49，AI 基础设施与算力 本期匹配 1061 篇文章，重点集中在 预训练/模型架构、Agent 工作流、AI 基础设施。建议先看《Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things》。
- 成本管理与 FinOps：本周 207，今日 +52，成本管理与 FinOps 本期匹配 900 篇文章，重点集中在 预训练/模型架构、后训练/对齐、Agent 工作流。建议先看《Qwen 3.8 27B is excellent, but it defaults to wildly overthinking things》。
- AI 改造传统领域：本周 115，今日 +25，AI 改造传统领域 本期匹配 419 篇文章，重点集中在 Agent 工作流、评测/安全、产品发布。建议先看《Claude's new system prompt really doesn't want to reproduce song lyrics》。

## 内容分栏

- 学啥：80 篇
- 读啥：80 篇
- 做啥：47 篇
- 忽略：0 篇