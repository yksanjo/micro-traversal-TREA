# micro-traversal

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![GitHub stars](https://img.shields.io/github/stars/yksanjo/micro-traversal?style=social)](https://github.com/yksanjo/micro-traversal/stargazers) [![GitHub forks](https://img.shields.io/github/forks/yksanjo/micro-traversal.svg)](https://github.com/yksanjo/micro-traversal/network/members) [![GitHub issues](https://img.shields.io/github/issues/yksanjo/micro-traversal.svg)](https://github.com/yksanjo/micro-traversal/issues)
[![Last commit](https://img.shields.io/github/last-commit/yksanjo/micro-traversal.svg)](https://github.com/yksanjo/micro-traversal/commits/main)


A minimal, self-healing web automation toolkit that records and replays user workflows using DOM selectors and visual matching.

## Features
- Record user interactions into human-readable JSON
- Replay with DOM-first, vision fallback using template matching
- Runs locally without cloud dependencies

## Tech Stack
- Python
- Playwright
- OpenCV
- JSON

## Quick Start

```
pip install -r requirements.txt
playwright install chromium
python record.py --name example_login --url https://example.com --demo
python replay.py --name example_login
```

## Structure
```
micro-traversal/
├── record.py
├── replay.py
├── utils/vision.py
├── workflows/
└── assets/templates/
```

## License
MIT