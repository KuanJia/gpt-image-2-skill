---
name: gpt-image-2-generator
description: Generate images with `gpt-image-2` through an OpenAI-compatible Images API. Use when Codex or another agent needs to create PNG images from prompts in any project, especially when the API endpoint is not the default OpenAI base URL and must be configured locally at install time without storing secrets in the repository.
---

# GPT Image 2 Generator

## Overview

Configure a reusable, secret-safe image generation workflow for `gpt-image-2`. Keep the skill repository free of real credentials by writing local machine settings into `config.local.json` and reading the API key from an environment variable.

## Quick Start

1. Create local configuration:

```bash
python scripts/install_config.py --base-url https://your-endpoint.example/v1 --api-key-env OPENAI_API_KEY
```

2. Export the API key into the configured environment variable:

```bash
export OPENAI_API_KEY="..."
```

On PowerShell:

```powershell
$env:OPENAI_API_KEY="..."
```

3. Generate an image:

```bash
python scripts/generate_image.py --prompt "A scientific diagram of a pacemaker" --output output.png
```

## Workflow

- Run `scripts/install_config.py` once per machine or once per endpoint profile.
- Keep `config.local.json` out of version control.
- Read `references/configuration.md` if you need the config layout or security rules.
- Use `scripts/generate_image.py` for actual generation.

## Notes

- The generation script supports either `b64_json` or `url` image responses.
- The script disables environment proxies by default when `disable_env_proxy` is `true` in local config.
- Override `--model` or `--api-key-env` at runtime only when needed; otherwise prefer the local config defaults.

## Files

- `scripts/install_config.py`: write local configuration without storing secrets in git.
- `scripts/generate_image.py`: call the OpenAI-compatible Images API and save the image.
- `config.example.json`: safe template for local config.
- `references/configuration.md`: concise setup and usage reference.
