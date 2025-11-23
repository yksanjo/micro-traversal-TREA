import json
import os
import cv2
import argparse
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--url", default="https://example.com")
parser.add_argument("--demo", action="store_true")
args = parser.parse_args()

WORKFLOW_DIR = "workflows"
TEMPLATE_DIR = "assets/templates"
os.makedirs(WORKFLOW_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

def save_workflow(workflow):
    path = os.path.join(WORKFLOW_DIR, f"{args.name}.json")
    with open(path, "w") as f:
        json.dump(workflow, f, indent=2)
    print(f"Saved workflow to {path}")

def capture_template(page, selector, step_index):
    el = page.query_selector(selector)
    if not el:
        return None
    box = el.bounding_box()
    if not box:
        return None
    filename = f"{args.name}_step{step_index}.png"
    path = os.path.join(TEMPLATE_DIR, filename)
    page.screenshot(path=path)
    img = cv2.imread(path)
    x1 = int(box["x"]) 
    y1 = int(box["y"]) 
    x2 = int(box["x"] + box["width"]) 
    y2 = int(box["y"] + box["height"]) 
    crop = img[y1:y2, x1:x2]
    cv2.imwrite(path, crop)
    return filename

def main():
    workflow = {"steps": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headful=True, slow_mo=250)
        page = browser.new_page()
        page.goto(args.url)
        workflow["steps"].append({"type": "goto", "url": args.url})
        if args.demo:
            selector = "a"
            tmpl = capture_template(page, selector, len(workflow["steps"]))
            workflow["steps"].append({"type": "click", "selector": selector, "template": tmpl or ""})
            save_workflow(workflow)
            browser.close()
            return
        print("Recording. Type CSS selectors to capture clicks. Type 'done' to finish.")
        while True:
            sel = input("selector> ").strip()
            if sel.lower() == "done":
                break
            tmpl = capture_template(page, sel, len(workflow["steps"]))
            workflow["steps"].append({"type": "click", "selector": sel, "template": tmpl or ""})
            print(f"Added click step for {sel}")
        save_workflow(workflow)
        browser.close()

if __name__ == "__main__":
    main()