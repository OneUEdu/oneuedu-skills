# Independent installation

Install this complete directory with a host that supports SKILL.md, or use the same skill bundled in One U Education. The workflow and examples are identical in both distributions.

Connect the official remote MCP endpoint `https://mcp.oneuedu.com/mcp` using the host's remote MCP configuration. The dependency declaration is supplied in agents/openai.yaml; not every host automatically installs dependencies. Check actual availability of submit_feedback, list_my_feedback and get_my_feedback before using them. File attachments also need import_feedback_attachments (chat files from the host) or prepare_feedback_upload (local files sent by HTTP PUT); a client offering neither cannot attach files.

Use the host's normal OAuth connection for personal ticket access. New anonymous reports need no account; their references do not allow later reading or discussion. Installing the skill alone neither connects the MCP server nor signs in. Never embed account tokens or service keys in this directory.
