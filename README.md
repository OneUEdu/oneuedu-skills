# One U Education Skills

One U Education 面向官网用户的技能源码，私有仓库。与面向员工的 `OneUEdu/oneulink-skills` 分开维护。

| 技能 | 职责 |
| --- | --- |
| [website-feedback](skills/website-feedback/SKILL.md) | 提交反馈、查询本人进度、续接公开讨论 |
| [australian-course-application](skills/australian-course-application/SKILL.md) | 保存申请意向，使用安全表单和确认组件交给申请专员 |
| [australian-immigration-planning](skills/australian-immigration-planning/SKILL.md) | 个人规划资料、计算及结果解读 |

## 维护与分发

此仓库是技能说明的唯一维护源；插件包装位于 [oneuedu-plugin](https://github.com/OneUEdu/oneuedu-plugin)。插件的 `plugins/one-u-education/skills` 通过 Git 子模块引用本完整仓库的确切提交，不再复制同步或维护第二份技能正文。源仓库内的业务入口仍是 `skills/<name>/`，构建会将它们放入原有安装包结构。

修改后先运行下面的本地检查，提交并推送到本仓库，再在插件仓库检出这个已推送的子模块提交、`git add plugins/one-u-education/skills`，验证并提交父仓库指针。新增技能提交不会让插件自动更新；取得插件源码需递归克隆或执行 `git submodule update --init --recursive`。完整命令见插件仓库的日常维护说明。

独立使用时，取得仓库访问权限，复制完整的 `skills/<name>/` 到所用客户端支持的技能安装位置，或使用插件仓库构建独立技能包。保留 `references/` 和 `agents/`，不要只复制 SKILL.md。独立安装不等于已连接 MCP、已登录或已获得工具。

所有技能连接 `https://mcp.oneuedu.com/mcp`。本人反馈需有效账号连接；匿名反馈仍为单向。反馈讨论功能须先部署配套 v2／CRM／官网／MCP；初始源码不表示生产已开放全部工具。

目前沿用既有宿主说明，尚未新增或验证 Claude 插件格式。申请流程依赖安全表单与确认组件，不能把可安装 SKILL.md 等同于所有客户端均可完成该流程。未来客户端差异应经过实际验证，包装适配维护在插件仓库。

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
