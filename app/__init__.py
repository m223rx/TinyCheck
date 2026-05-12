import os
import sys
import logging
import argparse
from .proxy_checker import ProxyChecker
from .colored_formatter import ColoredFormatter


def cli_main() -> None:
    parser = argparse.ArgumentParser(
        description="TinyCheck – test proxies against a URL."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to text file containing proxies (one IP:PORT per line)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="results",
        help="Directory to store results (default: results)",
    )
    parser.add_argument(
        "-t",
        "--test-url",
        default=ProxyChecker.DEFAULT_TEST_URL,
        help="URL to test proxies against (default: ipify)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=ProxyChecker.DEFAULT_TIMEOUT,
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--types",
        nargs="+",
        choices=["http", "https", "socks4", "socks5"],
        default=["http", "https", "socks4", "socks5"],
        help="Proxy types to test (default: all four)",
    )
    parser.add_argument(
        "--save-all-types",
        action="store_true",
        help="Save proxy to each proxy type file it works with (default: only first success)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable coloured output"
    )

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    if args.no_color:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    else:
        formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[handler])

    input_path = args.input
    if not os.path.isfile(input_path):
        sys.exit(f"Input file not found: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        proxies = [line.strip() for line in f if line.strip()]
    if not proxies:
        sys.exit("No proxies found in input file.")

    checker = ProxyChecker(
        test_url=args.test_url or "https://api.ipify.org/?format=json",
        timeout=args.timeout or 30,
        output_dir=args.output_dir or "results",
        proxy_types=args.types or ["http", "https", "socks4", "socks5"],
        save_all_types=args.save_all_types or False,
    )
    checker.run(proxies)
