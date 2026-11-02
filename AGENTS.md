# One U Education 技能维护

- `skills/<name>/` 是插件侧业务说明的唯一维护源；保持技能名和 MCP 身份稳定。
- 通用流程写在 SKILL.md，按需细节放 references；客户端专属清单和打包逻辑归 oneuedu-plugin。
- 当前申请流程依赖安全组件及人工点击；迁移或适配客户端时不得把聊天同意改作组件确认。连接、授权及可用工具以宿主和服务实际提供为准。
- 修改后运行 `python3 scripts/check.py` 和 `python3 -m unittest discover -s scripts -p 'test_*.py'`；业务变更还需对应服务／客户端验证。
- 提交技能后，由插件仓库 sync 锁定确切提交；不手改插件内的快照。此仓库不包含服务端实现、账户凭据或真实业务记录。
