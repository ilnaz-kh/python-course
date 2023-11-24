## Ex 14 - Q 01
class Task:
    def __init__(self, id_i, title) -> None:
        self.id_i = id_i
        self.title = title
        self.status = False

    def __str__(self) -> str:
        return f"ID: {self.id_i}, Title: {self.title}, Status: {self.status}"

    def update_status(self, new_status):
        self.status = new_status or self.status

if __name__ == "__main__":
    t1 = Task("1", "a")
    print(t1)
    t1.update_status(True)
    print(t1)
