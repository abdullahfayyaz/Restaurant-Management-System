
class Node:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = None
        self.next = None


class Customer(Node):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "customer"


class Admin(Node):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "admin"


class CustomerLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def dd(self):
        return self.head.next

    def add(self, username, password):
        if self.is_empty():
            node = Admin(username, password)
        else:
            node = Customer(username, password)
        node.next = self.head
        self.head = node
        return True

    def numberofUser(self):
        count = 0
        current = self.head
        while current:
            current = current.next
            count += 1
        return count

    def search(self, info):
        name_found = False
        pass_found = False
        role = ''
        current = self.head
        while current:
            if current.username == info.username:
                name_found = True
                if current.password == info.password:
                    pass_found = True
                    role = current.role
                    break
            current = current.next
        return name_found, pass_found, role, current

    def delete(self, username, password):
        current = self.head
        if current and current.username == username and current.password == password:
            self.head = current.next
            return True

        previous = None
        while current and current.username != username and current.password != password:
            previous = current
            current = current.next

        if current:
            previous.next = current.next
            return True

        return False

    def display_customers(self):
        current_customer = self.head
        while current_customer:
            print(
                f"Username: {current_customer.username}, Password: {current_customer.password}, "
                f"Role: {current_customer.role}")
            current_customer = current_customer.next
