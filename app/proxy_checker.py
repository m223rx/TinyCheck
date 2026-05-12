import logging
import os
from datetime import datetime
from typing import List, Optional

import requests


class ProxyChecker:
    DEFAULT_TEST_URL = "https://api.ipify.org/?format=json"
    DEFAULT_TIMEOUT = 30
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) "
            "Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"
        )
    }
    PROXY_TYPES = ["http", "https", "socks4", "socks5"]

    def __init__(
        self,
        test_url: str = DEFAULT_TEST_URL,
        headers: dict = None,
        timeout: int = DEFAULT_TIMEOUT,
        output_dir: str = "results",
        proxy_types: List[str] = None,
        save_all_types: bool = False,
    ) -> None:
        self.test_url = test_url
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout
        self.output_dir = output_dir
        self.proxy_types = proxy_types or self.PROXY_TYPES
        self.save_all_types = save_all_types

        self.results: dict = {ptype: [] for ptype in self.proxy_types}

    def check_proxy(self, proxy_server: str) -> Optional[str]:
        for proxy_type in self.proxy_types:
            if self._test_proxy_type(proxy_server, proxy_type):
                if not self.save_all_types:
                    return proxy_type
                self.results[proxy_type].append(proxy_server)
        if self.save_all_types and any(self.results[pt] for pt in self.proxy_types):
            return "mixed"
        return None

    def _test_proxy_type(self, proxy_server: str, proxy_type: str) -> bool:
        proxy_url = f"{proxy_type}://{proxy_server}"
        session = requests.Session()
        session.trust_env = False
        target_scheme = self._get_url_scheme(self.test_url)
        session.proxies = {target_scheme: proxy_url}

        try:
            resp = session.get(
                self.test_url, headers=self.headers, timeout=self.timeout
            )
            if resp.status_code != 200:
                logging.debug(f"Proxy {proxy_url} returned {resp.status_code}")
                return False
            data = resp.json()
            actual_ip = data.get("ip")
            if not actual_ip:
                logging.debug(f"Proxy {proxy_url} response lacks 'ip' field")
                return False
            logging.info(f"Working proxy: {proxy_url}  (IP: {actual_ip})")
            return True
        except requests.RequestException as e:
            logging.debug(f"Proxy {proxy_url} failed: {e}")
            return False
        except ValueError as e:
            logging.debug(f"Proxy {proxy_url} returned non‑JSON: {e}")
            return False

    def _get_url_scheme(self, url: str) -> str:
        return url.split(":", 1)[0].lower()

    def _write_results(self, timestamp: str) -> None:
        base = os.path.join(self.output_dir, timestamp)
        os.makedirs(base, exist_ok=True)
        for ptype, proxies in self.results.items():
            if not proxies:
                continue
            filename = f"worked_proxies_{ptype}.txt"
            filepath = os.path.join(base, filename)
            with open(filepath, "a") as f:
                for proxy in proxies:
                    f.write(proxy + "\n")
            logging.info(f"Saved {len(proxies)} {ptype.upper()} proxies to {filepath}")

    def run(self, proxy_list: List[str]) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        total = len(proxy_list)
        for idx, proxy in enumerate(proxy_list, 1):
            logging.info(f"Checking ({idx}/{total}): {proxy}")
            ptype = self.check_proxy(proxy)
            if ptype and not self.save_all_types:
                self.results[ptype].append(proxy)

        self._write_results(timestamp)
        working = sum(len(v) for v in self.results.values())
        print(f"\nDone. {working}/{total} proxies worked.")
