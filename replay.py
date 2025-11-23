import json
import os
import argparse
from playwright.sync_api import sync_playwright
from utils.vision import find_element_on_screen

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
args = parser.parse_args()

WORKFLOW_PATH = os.path.join("workflows", f"{args.name}.json")
TEMPLATE_DIR = "assets/templates"

def main():
    with open(WORKFLOW_PATH) as f:
        workflow = json.load(f)
    with sync_playwright() as p:
        browser = p.chromium.launch(headful=True, slow_mo=400)
        page = browser.new_page()
        for step in workflow.get("steps", []):
            if step.get("type") == "goto":
                page.goto(step.get("url", ""))
            elif step.get("type") == "click":
                selector = step.get("selector", "")
                template = step.get("template", "")
                try:
                    page.click(selector, timeout=2000)
                    continue
                except Exception:
                    pass
                if template:
                    tpath = os.path.join(TEMPLATE_DIR, template)
                    if os.path.exists(tpath):
                        page.screenshot(path=".temp_screen.png")
                        match = find_element_on_screen(".temp_screen.png", tpath)
                        if match:
                            x, y = match
                            page.mouse.click(x, y)
        browser.close()

if __name__ == "__main__":
    main()