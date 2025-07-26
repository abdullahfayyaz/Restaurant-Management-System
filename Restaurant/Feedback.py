class FeedBack_Node:
    def __init__(self, username, date, feedback):
        self.feedback = feedback
        self.username = username
        self.date = date


class Feedback:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            print("Stack is empty")

    def getdata(self):
        feedback = []
        item_copy = list(self.items)  # Create a copy of the stack
        while item_copy:
            data = item_copy.pop()
            fd = [str(data.username), str(data.feedback), str(data.date)]
            feedback.append(fd)
        return feedback
