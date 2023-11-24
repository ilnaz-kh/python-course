## Ex 13 - Q 03
class Counter:
    def __init__(self) -> None:
        self.count = 0
    def __str__(self) -> str:
        return f"Count: {self.count}"
    def increment(self):
        self.count += 1
    def decrement(self):
        if self.count >= 1:
            self.count -= 1
        else:
            print("Counter is already zero")
    def reset(self):
        self.count = 0
    def get_count(self):
        return self.count


c1 = Counter()
c2 = Counter()

print(f"c2: {c2.get_count()}")
c2.increment()
print(f"c2: {c2.get_count()}")

print(f"c1: {c1.get_count()}")
c1.increment()   
c1.increment()
print(f"c1: {c1.get_count()}")
c1.decrement()
print(f"c1: {c1.get_count()}")
c1.reset()
print(c1)

print(c2)