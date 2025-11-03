"""
text_tools.py — функции для работы со строками.
"""
from typing import List

GREETING = "Greetings"

def slugify(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch.isspace() or ch in "-_./":
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug

def tokenize(text: str) -> List[str]:
    text = " ".join(ch if ch.isalnum() else " " for ch in text)
    return [t for t in text.split() if len(t) > 1]

def pad_left(s: str, width: int, fill: str = " ") -> str:
    return (fill * max(0, width - len(s))) + s

def wrap(text: str, width: int) -> List[str]:
    if width <= 0:
        raise ValueError("width должен быть положительным")
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
