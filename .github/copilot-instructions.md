<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Quick onboarding for AI coding agents

This repo is a minimal Node.js (CommonJS) starter with Claude/Anthropic integration. Use these notes to be immediately productive and avoid incorrect assumptions.

- Project type: Node.js (see `package.json` "type": "commonjs"). Prefer CommonJS (`const X = require('x')` / `module.exports`) when adding runtime files.
- Dependency of interest: `@anthropic-ai/claude-code` (v^2.0.34) is declared in `package.json`. Expect an `.env` file with `ANTHROPIC_API_KEY` for integration.

- Developer workflows discovered:
  - Install: `npm install` (standard)
  - Tests: `npm test` currently prints an error placeholder (no test suite yet). If you add tests, update `package.json` scripts.
  - There is no build step or src dir enforced by config — add sensible structure (e.g., `src/`, `test/`) and update `package.json`.

- Platform notes: `setup-ai-tools.bat` configures VS Code user settings (Windows). Do not rely on that for CI; it's a local convenience script that lists recommended extensions (OpenAI, ChatGPT, Code Runner, etc.).

- When editing or adding files:
  - Keep CommonJS module style unless you also change `package.json` to `type: "module"` and update consuming code.
  - If you add environment usage, read/write `.env` and document new variables in `CLAUDE.md`.
  - Update `package.json` scripts for any new commands (e.g., `start`, `build`, `test`).

- Integration and security:
  - Anthropic/Claude client will use `ANTHROPIC_API_KEY` in `.env` — treat this as a secret and do not commit `.env` to the repo.

- Examples (use these patterns when scaffolding integration code):
  - Require style: `const Claude = require('@anthropic-ai/claude-code');`
  - Read env: `const key = process.env.ANTHROPIC_API_KEY;`

- Places to look when you need context:
  - `package.json` — declared dependency and scripts
  - `CLAUDE.md` — current human/agent-oriented notes
  - `setup-ai-tools.bat` — local VS Code setup hints and extension suggestions (Windows)

If something is missing (for example, a CI config, src layout, or tests), propose small, self-contained changes (one PR per change). Ask for clarification before making large structural edits.

If this file should merge existing content elsewhere, paste that content into a comment and request a targeted merge.

-- End of agent guidance
