import argparse
import base64
import json
import os
from pathlib import Path
import urllib.request


def load_config() -> dict:
    skill_root = Path(__file__).resolve().parents[1]
    local_config = skill_root / "config.local.json"
    if not local_config.exists():
        raise SystemExit(
            "Missing config.local.json. Run scripts/install_config.py first."
        )
    return json.loads(local_config.read_text(encoding="utf-8"))


def generate_image(
    base_url: str,
    api_key: str,
    prompt: str,
    output_path: Path,
    model: str,
    size: str,
    quality: str | None,
    background: str | None,
    timeout_seconds: int,
    trust_env: bool,
) -> None:
    endpoint = f"{base_url.rstrip('/')}/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
    }
    if quality:
        payload["quality"] = quality
    if background:
        payload["background"] = background

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    opener = (
        urllib.request.build_opener()
        if trust_env
        else urllib.request.build_opener(urllib.request.ProxyHandler({}))
    )

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with opener.open(request, timeout=timeout_seconds) as response:
        body = json.loads(response.read().decode("utf-8"))

    data = body.get("data") or []
    if not data:
        raise RuntimeError(f"API returned no image data: {body}")

    image_item = data[0]
    if "b64_json" in image_item:
        image_bytes = base64.b64decode(image_item["b64_json"])
    elif "url" in image_item:
        with opener.open(image_item["url"], timeout=timeout_seconds) as image_response:
            image_bytes = image_response.read()
    else:
        raise RuntimeError(f"Unsupported image response format: {body}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)


def main() -> None:
    config = load_config()
    parser = argparse.ArgumentParser(
        description="Generate an image with gpt-image-2 via an OpenAI-compatible API.",
    )
    parser.add_argument("--prompt", required=True, help="Prompt used for image generation.")
    parser.add_argument(
        "--output",
        required=True,
        help="Output image path.",
    )
    parser.add_argument("--size", default="1024x1024", help="Image size.")
    parser.add_argument(
        "--quality",
        default=None,
        help="Optional quality parameter if the endpoint supports it.",
    )
    parser.add_argument(
        "--background",
        default=None,
        help="Optional background parameter if the endpoint supports it.",
    )
    parser.add_argument(
        "--api-key-env",
        default=None,
        help="Override the API key environment variable name from config.local.json.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model from config.local.json.",
    )
    args = parser.parse_args()

    api_key_env = args.api_key_env or config["api_key_env"]
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise SystemExit(f"Missing API key in environment variable: {api_key_env}")

    generate_image(
        base_url=config["base_url"],
        api_key=api_key,
        prompt=args.prompt,
        output_path=Path(args.output),
        model=args.model or config.get("model", "gpt-image-2"),
        size=args.size,
        quality=args.quality,
        background=args.background,
        timeout_seconds=int(config.get("timeout_seconds", 180)),
        trust_env=not bool(config.get("disable_env_proxy", True)),
    )
    print(f"Image saved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
