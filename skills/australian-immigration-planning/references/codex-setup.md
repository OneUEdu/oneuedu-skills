# Codex 独立安装与官网 MCP

本 skill 无需安装 OneU 插件。安装文件、连接官网 MCP、账户授权是三个独立步骤；`agents/openai.yaml` 的依赖声明不能证明连接或授权已完成。此说明仅在安装或连接排障时读取。

## 安装 skill 文件

将发行 ZIP 解压到一个新的临时目录。把其中完整的 `australian-immigration-planning/` 目录复制到 `~/.agents/skills/`，保留 `agents/` 和 `references/`。也可放在目标项目的 `.agents/skills/` 中，仅对该项目使用。若已有同名目录，先核对来源与版本，备份后完整替换，不合并不同版本的引用文件。不要在多个扫描目录重复安装同名 skill。

Codex 会检测 skill 变化；未出现时重启。用 `$australian-immigration-planning` 显式选择，或直接提出移民规划问题验证自然触发。已安装的插件如果也暴露同名 skill，应明确选择本地版本进行验证，不默认两者会合并。

## 配置官网连接

先查看现有连接，复用 URL 为 `https://mcp.oneuedu.com/mcp` 的连接；名字可以不同。仅在不存在该连接且用户要求配置时添加。不要覆写同名的其他服务配置。

```sh
codex mcp list
codex mcp add one-u-education --url https://mcp.oneuedu.com/mcp
```

也可以在 Codex 的 MCP 设置中配置 Streamable HTTP URL。要只做匿名公共资料咨询，可在用户配置 `~/.codex/config.toml` 中添加以下表；已有配置则复用，不重复追加：

```toml
[mcp_servers.one-u-education]
url = "https://mcp.oneuedu.com/mcp"
```

CLI 添加时若启动 OAuth 提示，只有用户需要账户能力时才完成授权。匿名资料查询本身不需要账户权限。重新打开 Codex 后检查实际工具发现与错误；文件存在、连接列出和工具可调用是不同的验证结果。

## 需要账户档案或计算时授权

通过 Codex 的 OAuth 登录界面完成官网账户登录。以下为完整规划工作流的权限示例；若连接名称不同，替换名称：

```sh
codex mcp login one-u-education --scopes mcp:read,planning:read,planning:write,planning:calculate
```

仅读取档案时只需基础 `mcp:read` 和 `planning:read`；保存和计算分别增加对应权限。需要保持连接时可按官网授权流程另授予 `offline_access`。以工具返回的当前授权挑战为准，旧授权及刷新不会自动增加 planning 权限。权限允许某项操作不代表用户已要求执行该操作。

不要让用户在聊天中粘贴 token、Cookie、密码或服务 API Key；不要使用公司的 `/toolkit/mcp` 固定 Key 入口访问个人档案。OAuth 客户端被拒绝时，保留具体错误并通过官网支持处理客户端注册/信任问题，不编造客户端 ID 或绕过鉴权。

## 识别失败位置

| 状态 | 下一步 |
| --- | --- |
| skill 未发现 | 检查目录位置、完整文件及是否被禁用，必要时重启 Codex。 |
| 无官网 MCP 连接 | 按用户要求配置连接；仍可用可访问的官方原文回答有证据支持的咨询。 |
| 已连接但没有 planning 工具 | 核查当前服务器工具目录及服务启用状态；不能从课程工具可用推断规划可用。 |
| 未认证或授权过期 | 在宿主中登录；不把失败读取说成没有档案。 |
| insufficient_scope | 按当前操作重新授权所需权限，不反复重试同一失败调用。 |
| 网络、限流或服务错误 | 按实际错误及重试提示处理，保留已接受任务 ID；不通过换 request_id 重复创建任务。 |

连接配置后，可先测试公开问题。账户读取、保存和计算的验证应使用获授权的账号与任务；不为测试偷偷创建真实档案。生成包或通过本地测试不等于生产 OAuth 旅程已通过。

说明核对日期：2026-10-31。Codex 安装与配置依据：[官方 skills 文档](https://learn.chatgpt.com/docs/build-skills)、[官方 MCP 文档](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)；CLI 参数同时通过本地 `codex mcp add --help` 和 `codex mcp login --help` 核对。官网业务权限以服务器当前工具合同为准。
