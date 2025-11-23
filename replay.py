import json
import os
import argparse
from playwright.sync_api import sync_playwright
from micro_traversal.vision import find_element_on_screen
from micro_traversal.logutil import get_logger
from typing import List, Dict

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
args = parser.parse_args()

WORKFLOW_PATH = os.path.join("workflows", f"{args.name}.json")
TEMPLATE_DIR = "assets/templates"
REPORTS_DIR = "reports"
logger = get_logger("replay", "INFO")

def main():
    with open(WORKFLOW_PATH) as f:
        workflow = json.load(f)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    results: List[Dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headful=True, slow_mo=300)
        page = browser.new_page()
        for step in workflow.get("steps", []):
            stype = step.get("type")
            if stype == "goto":
                url = step.get("url", "")
                logger.info(f"goto {url}")
                page.goto(url)
                results.append({"type": "goto", "status": "ok", "url": url})
            elif stype == "click":
                selector = step.get("selector", "")
                template = step.get("template", "")
                logger.info(f"click {selector}")
                success = False
                for _ in range(2):
                    try:
                        page.click(selector, timeout=2000)
                        success = True
                        break
                    except Exception:
                        pass
                if success:
                    results.append({"type": "click", "status": "ok", "mode": "dom", "selector": selector})
                else:
                    if template:
                        tpath = os.path.join(TEMPLATE_DIR, template)
                        if os.path.exists(tpath):
                            page.screenshot(path=".temp_screen.png")
                            match = find_element_on_screen(".temp_screen.png", tpath)
                            if match:
                                x, y = match
                                page.mouse.click(x, y)
                                results.append({"type": "click", "status": "ok", "mode": "vision", "x": x, "y": y})
                            else:
                                results.append({"type": "click", "status": "fail", "reason": "vision_no_match"})
                        else:
                            results.append({"type": "click", "status": "fail", "reason": "missing_template"})
                    else:
                        results.append({"type": "click", "status": "fail", "reason": "no_template"})
        browser.close()
    rpath = os.path.join(REPORTS_DIR, f"report_{args.name}.json")
    with open(rpath, "w") as rf:
        json.dump({"results": results}, rf, indent=2)

if __name__ == "__main__":
    main()