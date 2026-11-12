# One U Education Skills

One U Education 面向官网用户的技能源码。与面向员工的 `OneUEdu/oneulink-skills` 分开维护。

| 技能 | 职责 |
| --- | --- |
| [website-feedback](skills/website-feedback/SKILL.md) | 提交反馈、查询本人进度、续接公开讨论 |
| [australian-course-application](skills/australian-course-application/SKILL.md) | 保存申请意向，使用安全表单和确认组件交给申请专员 |
| [australian-immigration-planning](skills/australian-immigration-planning/SKILL.md) | 个人规划资料、计算及结果解读 |

## 一句话安装

仓库根目录放了各客户端的插件清单，可以直接从 GitHub 安装。插件版会同时装好技能和官方 MCP 连接 `https://mcp.oneuedu.com/mcp`。公开查询不用登录；建规划档案、查自己的反馈时，客户端会弹出 One U Education 登录。

| 客户端 | 安装命令 | 装进去的 |
| --- | --- | --- |
| Claude Code | `claude plugin install one-u-education --marketplace OneUEdu/oneuedu-skills` | 规划、反馈技能 + MCP |
| Codex | `codex plugin marketplace add OneUEdu/oneuedu-skills`，再 `codex plugin add one-u-education@oneuedu` | 规划、反馈技能 + MCP |
| GitHub Copilot CLI | `copilot plugin marketplace add OneUEdu/oneuedu-skills`，再 `copilot plugin install one-u-education@oneuedu` | 规划、反馈技能 + MCP |
| Grok Build | `grok plugin install OneUEdu/oneuedu-skills --trust`，再 `grok plugin enable one-u-education` | 规划、反馈技能 + MCP（未实测，见下） |
| 其他支持 Agent Skills 的客户端（Cursor、Gemini CLI、OpenCode 等） | `npx skills add OneUEdu/oneuedu-skills -s australian-immigration-planning website-feedback` | 只有技能，MCP 要按客户端说明另加 |

在 Claude Code 对话里也可以输入 `/plugin install one-u-education --marketplace OneUEdu/oneuedu-skills`。

- 申请技能 `australian-course-application` 要用 ChatGPT 的安全表单和确认卡片，直接安装不带它。ChatGPT 版由 oneuedu-plugin 打包、走 OpenAI 审核。
- 清单不写版本号，客户端按 Git 提交更新。推送新提交后，用户运行 `claude plugin update one-u-education@oneuedu`、`codex plugin marketplace upgrade` 、`copilot plugin update one-u-education@oneuedu` 或 `grok plugin update one-u-education` 拿到新版。
- `.grok-plugin/` 按 xAI 插件市场（xai-org/plugin-marketplace）的格式写：Grok Build 先读 `.grok-plugin/plugin.json`，再读 `.claude-plugin/`；`marketplace.json` 让仓库能直接 `grok plugin install OneUEdu/oneuedu-skills` 安装。`--trust` 跳过安装时的信任确认；有资料说 enable 之后才加载技能，要新开会话。2026-11-12 还**没有实测**：xAI 的索引脚本总会扫描 `skills/` 整个目录，Grok 是否按清单只装规划、反馈两个技能、要不要单独 enable，以实测为准。
- `.cursor-plugin/` 按 Cursor 文档写好了，但 Cursor 只能从自己的插件市场装，要先在 cursor.com/marketplace/publish 提交，没有实测。VS Code 的 “Chat: Install Plugin From Source” 用的是 Copilot 格式，也没有实测。
- 2026-11-03 在隔离的配置目录里实测：Claude Code 2.1.316、Codex CLI 0.166.0、Copilot CLI 1.0.105 都只加载规划、反馈两个技能，并连上 MCP；skills CLI 1.7.6 按 `-s` 只装这两个。

清单由 `scripts/platforms.py` 一处生成，不要手改。改名称、介绍、技能列表或 MCP 地址时改这个脚本，再运行 `python3 scripts/platforms.py`；`scripts/check.py` 会检查清单是不是最新。新增技能要不要进直接安装版，在脚本的 `SKILLS` 里决定。

## 维护与分发

此仓库是技能说明的唯一维护源；插件包装位于 [oneuedu-plugin](https://github.com/OneUEdu/oneuedu-plugin)。插件的 `plugins/one-u-education/skills` 通过 Git 子模块引用本完整仓库的确切提交，不再复制同步或维护第二份技能正文。源仓库内的业务入口仍是 `skills/<name>/`，构建会将它们放入原有安装包结构。

修改后先运行下面的本地检查，提交并推送到本仓库，再在插件仓库检出这个已推送的子模块提交、`git add plugins/one-u-education/skills`，验证并提交父仓库指针。新增技能提交不会让插件自动更新；取得插件源码需递归克隆或执行 `git submodule update --init --recursive`。完整命令见插件仓库的日常维护说明。

不用上面的命令时，可以把完整的 `skills/<name>/` 复制到客户端的技能目录，或用插件仓库构建独立技能包。保留 `references/` 和 `agents/`，不要只复制 SKILL.md。只装技能不等于已连接 MCP、已登录或已获得工具。

所有技能连接 `https://mcp.oneuedu.com/mcp`。本人反馈需有效账号连接；匿名反馈仍为单向。反馈讨论功能须先部署配套 v2／CRM／官网／MCP；初始源码不表示生产已开放全部工具。

申请流程依赖安全表单与确认组件，不能把可安装 SKILL.md 等同于所有客户端均可完成该流程。新增客户端要先实际验证；ChatGPT 提审包的清单和打包维护在插件仓库。

## 本地检查

Python 3.12，标准库即可：

```sh
python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

校验技能入口、MCP 依赖、引用文件和分发边界；不请求远程服务、不安装技能、不发邮件。技能内容改动还需实际业务验收。

## 迁移

初始 11 份文件原样取自 CRM 已提交候选包，提交及哈希记录在 [migration-source.json](docs/migration-source.json)。没有改写现有业务规则。历史申请技能来自官网生成快照；从本次迁移起，**插件侧说明在此维护**，旧生成器输出需人工对照并审阅，不能覆盖本库。WhatsApp 运行时和服务端规则仍归原项目。

### 规划技能 1.9.2 补同步（2026-11-03）

从 CRM 提交 `b07802e4` 补入迁移前的规划正文及服务参考更新：交付围绕用户当前决定与行动，区分职业比较、目标保存和计算，补足高影响事实澄清及未来费用解释。其余技能与引用保持原样；后续规划修改只在本仓库进行。插件从本仓确切提交同步，本次源码检查不表示服务部署或真实模型验收完成。
