def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else "0으로 나눌 수 없음"

print("3 + 7 =", add(3, 7))
print("10 / 2 =", div(10, 2))
