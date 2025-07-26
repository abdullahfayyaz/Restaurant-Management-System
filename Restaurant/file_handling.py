import customer as info
import csv
import pandas as pd
from datetime import datetime
import Feedback
import meal_avl


def load_data():
    file_path = 'customer_data.csv'
    customer_list = info.CustomerLinkedList()
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                password = row['password']
                customer_list.add(username, password)
    except FileNotFoundError:
        print("File not found")
    return customer_list


def save_data(data):
    file_path = 'customer_data.csv'
    customer_data = {'username': data.username, 'password': data.password, 'role': data.role}
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['username', 'password', 'role']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(customer_data)


def save_stack_data(data):
    file_path = 'feedback_data.csv'
    customer_data = [{'username': item.username, 'feedback': item.feedback, 'date': item.date} for item in data.items]
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['username', 'feedback', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customer_data)
    # file_path = 'feedback_data.csv'
    # copy_items = list(data.items)
    # usernames = []
    # dates = []
    # feedbacks = []
    # while not copy_items.isempty():
    #     dt = copy_items.pop()
    #     usernames.append(dt.username)
    #     dates.append(dt.date)
    #     feedbacks.append(dt.feedback)
    # customer_data = {'username': usernames, 'feedback': feedbacks, 'date': dates}
    # df = pd.DataFrame(customer_data)
    # df.to_csv(file_path, mode='w', index=False)


def load_stack_data():
    file_path = 'feedback_data.csv'
    feed_back = Feedback.Feedback()
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                feedback = row['feedback']
                date = row['date']
                data = Feedback.FeedBack_Node(username, date, feedback)
                feed_back.push(data)
    except FileNotFoundError:
        print("File not found")
    return feed_back


def inorder(root, data):
    if root:
        inorder(root.left, data)
        data.append((root.name, root.price))
        inorder(root.right, data)
    return data


def save_avl(data):
    filename = 'meal_data.csv'
    data = inorder(data, [])
    with open(filename, 'w') as file:
        for meal, price in data:
            file.write(f'{meal},{price}\n')


def load_avl():
    avl = meal_avl.AVLIMPLEMENT()
    filename = 'meal_data.csv'
    with open(filename, 'r') as file:
        for line in file:
            meal, price = line.strip().split(',')
            price = int(price)
            avl.insertion(meal, price)
    return avl
