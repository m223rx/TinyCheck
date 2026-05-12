# TinyCheck – Smart Proxy Validation CLI

---

## 🚀 Features

- **Proxy File Validation**
  - Reads proxy lists from a local text file
  - Tests each proxy against a live URL
  - Supports multiple proxy schemes: `http`, `https`, `socks4`, and `socks5`

- **Flexible Command-Line Interface**
  - Specify input proxy list with `-i/--input`
  - Choose output directory with `-o/--output-dir`
  - Override default test URL with `--test-url`

- **Detailed Output and Logging**
  - Colorized terminal logs for success, info, and debug
  - Save only successful proxies to timestamped results folders
  - Optional `--no-color` mode for clean CI-friendly output

- **Resilient Network Handling**
  - Configurable request timeout
  - Graceful handling of request failures and JSON parse errors
  - Detects invalid or missing input files before testing begins

---

## 🛠 Tech Stack

- **Core Language**
  - Python 3 — minimal dependencies and fast execution

- **Libraries**
  - `requests` — proxy request execution and URL validation
  - `argparse` — CLI argument parsing
  - `logging` — terminal output and debug control
  - `dataclasses` — clean internal data handling (where applicable)
  - `colorama` — colored log output

- **Architecture**
  - `app.py` launches the CLI entrypoint
  - `app/proxy_checker.py` manages proxy testing and result persistence
  - `app/colored_formatter.py` enriches log output with color

---

## 💡 Usage

- Run proxy validation interactively:
  ```bash
  python app.py -i proxies.txt
  ```

- Use a custom output directory:
  ```bash
  python app.py -i proxies.txt -o checked_results
  ```

- Test proxies against a custom URL:
  ```bash
  python app.py -i proxies.txt --test-url https://api.ipify.org/?format=json
  ```

- Disable colored logging for scripts or automation:
  ```bash
  python app.py -i proxies.txt --no-color
  ```

---

## 🔮 Future Enhancements

- Add proxy speed and latency scoring
- Add built-in proxy list generation or scraping
- Validate proxy anonymity level and geolocation
- Export results to CSV/JSON formats
- Add concurrent proxy checks for faster validation

---

## ⚠️ Status

- **Active development**
- Core proxy validation workflow is implemented
- CLI options and colorized logging are available
- Improvements for parallel checks, validation rules, and exports are planned

## 👨‍💻 Developer

m223rx – 2026

© 2026 m223rx. All rights reserved.
