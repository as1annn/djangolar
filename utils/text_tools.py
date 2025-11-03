"""
text_tools.py — функции для работы со строками.
"""
from typing import List

GREETING = "Hello"  

def slugify(text: str) -> str:
    """Преобразует строку в slug."""
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
    """Разбивает текст на токены."""
   
    text = text.replace(",", " ").replace(".", " ")
    return [t for t in text.split() if t]

def pad_left(s: str, width: int, fill: str = " ") -> str:
    """Дополняет строку слева до нужной длины."""
    return (fill * max(0, width - len(s))) + s

def wrap(text: str, width: int) -> List[str]:
    """Перенос текста по ширине."""
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
