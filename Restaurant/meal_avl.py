class Node:
    def __init__(self, name, price):
        self.key = ascii_sum(name)
        self.name = name
        self.price = price
        self.left = None
        self.right = None
        self.height = 1


class AVLIMPLEMENT:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balanceCheck(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            return 1 + max(self.height(node.left), self.height(node.right))

    def left_rotate(self, root_at_which_rotation_applied):

        x = root_at_which_rotation_applied.right
        z = x.left

        x.left = root_at_which_rotation_applied
        root_at_which_rotation_applied.right = z

        self.update_height(root_at_which_rotation_applied)
        self.update_height(x)

        return x

    def right_rotate(self, key_root_at_which_rotation_applied):

        y = key_root_at_which_rotation_applied.left
        z = y.right

        y.right = key_root_at_which_rotation_applied
        key_root_at_which_rotation_applied.left = z

        self.update_height(key_root_at_which_rotation_applied)
        self.update_height(y)

        return y

    def min_value(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete_key(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self.delete_key(root.left, key)
        elif key > root.key:
            root.right = self.delete_key(root.right, key)

        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.min_value(root.right)
            root.key = temp.key
            root.right = self.delete_key(root.right, temp.key)

        self.update_height(root)

        balance = self.balanceCheck(root)

        if balance > 1:
            if self.balanceCheck(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance < -1:
            if self.balanceCheck(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def deletion(self, name):
        key = ascii_sum(name)
        self.root = self.delete_key(self.root, key)

    def insert(self, root, name, price):
        key = ascii_sum(name)
        if root is None:
            return Node(name, price)
        if key < root.key:
            root.left = self.insert(root.left, name, price)
        else:
            root.right = self.insert(root.right, name, price)
        self.update_height(root)

        balance_factor_check = self.balanceCheck(root)
        if balance_factor_check > 1:
            if key < root.left.key:  # LL
                return self.right_rotate(root)
            else:  # LR
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance_factor_check < -1:
            if key > root.right.key:  # RR
                return self.left_rotate(root)
            else:  # RL
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        return root

    def insertion(self, name, price):
        self.root = self.insert(self.root, name, price)

    def search(self, node, key):
        if node is None or node.key == ascii_sum(key):
            return node

        if ascii_sum(key) < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

    def search_key(self, key):
        node = self.search(self.root, key)
        return node

    def change_price(self, node, new_price):
        node.price = new_price

    def get_data(self):
        data = []
        self._get_data_recursive(self.root, data)
        return data

    def _get_data_recursive(self, node, data):
        if node:
            self._get_data_recursive(node.left, data)
            data.append({'name': str(node.name), 'price': str(node.price)})
            self._get_data_recursive(node.right, data)

    def empty(self):
        return self.root is None

def ascii_sum(string):
    stri = str(string)
    return sum(ord(char) for char in stri)
