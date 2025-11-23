from typing import Optional

def generate_selector(attrs: dict, tag: str, text: Optional[str]) -> str:
    if attrs.get("id"):
        return f"#{attrs['id']}"
    for key in ["data-testid", "data-test", "name", "aria-label"]:
        if attrs.get(key):
            return f"[{key}='{attrs[key]}']"
    if text:
        t = text.strip()
        if t:
            return f"text={t}"
    return tag