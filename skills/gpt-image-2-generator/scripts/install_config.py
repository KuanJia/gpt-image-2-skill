import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a local config file for the gpt-image-2 skill.",
    )
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible API base URL.")
    parser.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable name that stores the API key.",
    )
    parser.add_argument(
        "--model",
        default="gpt-image-2",
        help="Image model name.",
    )
    parser.add_argument(
        "--enable-proxy",
        action="store_true",
        help="Allow requests to use HTTP(S)_PROXY from the environment.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=180,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override the config.local.json output path.",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    output_path = Path(args.output) if args.output else skill_root / "config.local.json"
    config = {
        "base_url": args.base_url,
        "api_key_env": args.api_key_env,
        "model": args.model,
        "disable_env_proxy": not args.enable_proxy,
        "timeout_seconds": args.timeout_seconds,
    }
    output_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote config to: {output_path}")


if __name__ == "__main__":
    main()
