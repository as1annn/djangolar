"""
main.py — демонстрация работы функций из utils.
"""
from utils.math_tools import fib, moving_average, normalize, dot, poly_eval
from utils.text_tools import slugify, tokenize, wrap, GREETING

def demo_math():
    f10 = fib(10)
    ma = moving_average([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    v = normalize([10, -5, 0, 3])
    d = dot([1, 2, 3], [4, 5, 6])
    p = poly_eval([1, 0, -2, 3], 2.0)
    return {"fib10": f10, "ma3": ma, "norm": v, "dot": d, "poly": p}

def demo_text():
    text = f"{GREETING}, World! This, is a demo."
    return {
        "slug": slugify(text),
        "tokens": tokenize(text),
        "wrap20": wrap(text, 20)
    }

def main():
    print("=== MATH ===")
    for k, v in demo_math().items():
        print(f"{k}: {v}")

    print("\n=== TEXT ===")
    for k, v in demo_text().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
