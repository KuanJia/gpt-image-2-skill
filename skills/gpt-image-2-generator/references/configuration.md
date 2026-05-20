# Configuration

## Local files

- `config.example.json` is the checked-in template.
- `config.local.json` is created per machine and ignored by git.

## Install flow

Run:

```bash
python scripts/install_config.py --base-url https://your-endpoint.example/v1 --api-key-env OPENAI_API_KEY
```

This writes `config.local.json` into the skill folder.

## Security

- Never commit real API keys.
- Store the API key in an environment variable.
- Pass the base URL at install time, not in repository files.

## Generation

Run:

```bash
python scripts/generate_image.py --prompt "A scientific diagram of a pacemaker" --output output.png
```
