class QueueObject:
    def __init__(self, name, order_no):
        self.name = name
        self.order_no = order_no


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            print("Queue is empty")
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            print("Queue is empty")
            return None

    def size(self):
        return len(self.items)

    def print_queue(self):
        if self.is_empty():
            print("Queue is empty")
        else:
            print("Name\tOrderNo")
            for name, order_no in self.items:
                print(f"{name}\t{order_no}")

