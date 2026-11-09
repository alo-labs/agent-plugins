# alo-labs/agent-plugins

Unified thin marketplace for [Ālo Labs](https://alolabs.dev) agent plugins across Claude Code, Codex, and Cursor.

Plugin content stays authoritative in upstream repos (Silver Bullet in `alo-exp/silver-bullet`). This repo holds host-specific marketplace manifests only.

## Marketplace IDs (stable)

| Host | Marketplace ID | Manifest path |
|------|----------------|---------------|
| Claude Code | `alo-labs` | `.claude-plugin/marketplace.json` |
| Codex | `alo-labs-codex` | `.agents/plugins/marketplace.json` |
| Cursor | `alo-labs-cursor` | `.cursor-plugin/marketplace.json` |

## Install Silver Bullet

### Claude Code

```text
/plugin marketplace add alo-labs/agent-plugins
/plugin install silver-bullet@alo-labs
```

Or from checkout: `bash scripts/install-claude.sh`

### Codex

```bash
codex plugin marketplace add alo-labs/agent-plugins --sparse .agents/plugins
codex plugin add silver-bullet@alo-labs-codex
```

Or: `bash scripts/install-codex.sh --public-release --purge-legacy-skills`

### Cursor

1. Add marketplace source: `https://github.com/alo-labs/agent-plugins`
2. Install `silver-bullet` from marketplace `alo-labs-cursor`

Or: `bash scripts/install-cursor.sh --public-release`

## Layout

```text
.claude-plugin/marketplace.json
.cursor-plugin/marketplace.json
.agents/plugins/marketplace.json
README.md
```

## Version sync

Silver Bullet release bumps are pushed from the Silver Bullet source repo:

```bash
scripts/sync-release-marketplace-versions.sh <version>
```

That script synchronizes Silver Bullet entries across the three hosts. For an Optimax release, update only the `optimax` entry in `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`: set `version` to the release version, `source.ref` to its `v<version>` tag, and `source.sha` to the full accepted upstream commit SHA. Preserve each host's source identity and all unrelated entries; Optimax has no Cursor catalog entry.

Update the release constants in `tests/test_optimax_release.py` and run the offline catalog checks before publishing:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Legacy per-host repos (`alo-labs/claude-plugins`, `alo-labs/codex-plugins`, `alo-labs/alo-labs-cursor-marketplace`) redirect here during the transition window.
