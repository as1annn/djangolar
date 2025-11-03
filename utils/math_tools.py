"""
math_tools.py — набор функций для демонстрации работы с числами.
"""
from typing import Iterable, List, Tuple

PI_APPROX = 3.141592653

def fib(n: int) -> List[int]:
    """Возвращает первые n чисел Фибоначчи."""
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def moving_average(xs: Iterable[float], window: int) -> List[float]:
    """Скользящее среднее."""
    xs = list(xs)
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(xs):
        return []
    out = []
    s = sum(xs[:window])
    out.append(s / window)
    for i in range(window, len(xs)):
        s += xs[i] - xs[i - window]
        out.append(s / window)
    return out

def dot(a: Iterable[float], b: Iterable[float]) -> float:
    a, b = list(a), list(b)
    if len(a) != len(b):
        raise ValueError("Длины списков не совпадают")
    return sum(x * y for x, y in zip(a, b))

def normalize(xs: Iterable[float]) -> List[float]:
    xs = list(xs)
    m = max(abs(x) for x in xs) if xs else 1.0
    return [x / m for x in xs]

def clamp(x: float, lo: float, hi: float) -> float:
    if lo > hi:
        lo, hi = hi, lo
    return max(lo, min(hi, x))

def poly_eval(coeffs: List[float], x: float) -> float:
    """Вычисляет значение многочлена методом Горнера."""
    acc = 0.0
    for c in reversed(coeffs):
        acc = acc * x + c
    return acc
