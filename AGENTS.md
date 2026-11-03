# One U Education 技能维护

- `skills/<name>/` 是插件侧业务说明的唯一维护源；保持技能名和 MCP 身份稳定。
- 通用流程写在 SKILL.md，按需细节放 references；客户端专属清单和打包逻辑归 oneuedu-plugin。
- 当前申请流程依赖安全组件及人工点击；迁移或适配客户端时不得把聊天同意改作组件确认。连接、授权及可用工具以宿主和服务实际提供为准。
- 修改后运行 `python3 scripts/check.py` 和 `python3 -m unittest discover -s scripts -p 'test_*.py'`；业务变更还需对应服务／客户端验证。
- 提交并推送技能后，在插件仓库检出对应子模块版本并提交父仓库的 Git 指针；插件的 `plugins/one-u-education/skills` 引用本完整仓库，打包时只取其中 `skills/`。不再复制同步或另维护逐文件锁文件，不把未提交的子模块工作作为发布来源。此仓库不包含服务端实现、账户凭据或真实业务记录。
