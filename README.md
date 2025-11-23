# micro-traversal

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