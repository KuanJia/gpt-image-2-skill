# GPT Image 2 Skill

![GPT Image 2 Skill hero](assets/readme-hero.png)

Reusable Codex skill for generating images with `gpt-image-2` through OpenAI-compatible Images APIs.

This repository is designed to stay secret-safe:

- Real `base_url` values are provided during local installation.
- Real API keys are read from environment variables.
- No live credentials are committed into the repository.

## Repository Layout

- `skills/gpt-image-2-generator/`: installable Codex skill
- `skills/gpt-image-2-generator/scripts/install_config.py`: writes local config
- `skills/gpt-image-2-generator/scripts/generate_image.py`: generates images
- `skills/gpt-image-2-generator/config.example.json`: safe config template

## Install The Skill

If you already have the Codex `skill-installer` helper:

```bash
python install-skill-from-github.py --repo KuanJia/gpt-image-2-skill --path skills/gpt-image-2-generator
```

Restart Codex after installation so it can discover the new skill.

## Configure Locally

Go into the installed skill directory and create a local config file:

```bash
python scripts/install_config.py --base-url https://your-endpoint.example/v1 --api-key-env OPENAI_API_KEY
```

This writes `config.local.json` locally and keeps it out of git.

Then set your API key:

```bash
export OPENAI_API_KEY="your_api_key"
```

On PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

## Generate An Image

```bash
python scripts/generate_image.py --prompt "A scientific diagram of a pacemaker" --output output.png
```

Example with a larger landscape output:

```bash
python scripts/generate_image.py --prompt "A polished repository banner for an AI image generation skill" --output banner.png --size 1536x1024
```

## Security Model

- Commit `config.example.json`, never `config.local.json`
- Keep API keys in environment variables
- Pass endpoint configuration at install time
- Share the repository freely without leaking deployment secrets

## Published Skill

The installable skill entry point is:

- `skills/gpt-image-2-generator`

Inside that folder, the main skill instructions live in:

- `skills/gpt-image-2-generator/SKILL.md`
