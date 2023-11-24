from Task import *
class ToDoList:
    def __init__(self) -> None:
        self.tasks = {} # (key, value):  (task.id_i, task) 

    def add_task(self, id_i, title):
        if id_i not in self.tasks:
            new_task = Task(id_i, title)
            self.tasks[id_i] = new_task
            print("task added!")
        else:
            print("task already exists!")

    def remove_task(self, id_i):
        if id_i in self.tasks:
            del self.tasks[id_i]
            print("task is removed!")
        else:
            print("not found!")

    def display_tasks(self):
        if len(self.tasks): # there is at least one task
            for task in self.tasks.values():
                print(task) # call `__str__` method of class `Task`
        else:
            print("There is no task!")

manager = ToDoList()
manager.display_tasks()
manager.add_task("1", "a")
manager.add_task("2", "b")
manager.display_tasks()
manager.remove_task("3")
manager.remove_task("1")
manager.display_tasks()