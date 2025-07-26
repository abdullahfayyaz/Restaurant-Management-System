import csv
from datetime import datetime
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QMessageBox, QTableWidgetItem, \
    QTableWidget, QInputDialog, QComboBox
import customer as info
import file_handling
import Validation
import re
import Feedback
import order_queue
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Ui_File.ui", self)
        self.index = None
        self.cart = []
        self.displayBill = False
        self.queue = order_queue.Queue()
        self.order_no = 1
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.feedback_stack = file_handling.load_stack_data()
        self.Meal = file_handling.load_avl()
        self.users = file_handling.load_data()  # users list
        self.loginBtn.clicked.connect(self.login)  # login button
        self.createAccount.clicked.connect(self.next_page)  # Go to sign up page button
        self.registerBtn.clicked.connect(self.createAccountClicked)  # create account button
        self.feedbtn.clicked.connect(self.viewfeedback)
        self.mealadd.clicked.connect(self.mealframe)  # show add meal Frame
        self.mealremove.clicked.connect(self.mealframeremove)  # show remove meal Frame
        self.mealprice.clicked.connect(self.pricemealframeremove)  # show price meal frame
        self.addmealbtn.clicked.connect(self.addMeal)  # add meal button
        self.removemealbtn.clicked.connect(self.delete_meal)  # remove meal button
        self.namecheckbtn.clicked.connect(self.change_meal_price)  # name validation button
        self.pricecheckbtn.clicked.connect(self.change_meal_price)  # price change button
        self.backToLoginBtn.clicked.connect(self.prev)
        self.adminout.clicked.connect(self.logout)
        self.userout.clicked.connect(self.logout1)
        self.checkBox.stateChanged.connect(self.show_passwordS)
        self.checkBox_2.stateChanged.connect(self.show_passwordL)
        self.home.clicked.connect(self.homeview)
        self.home2.clicked.connect(self.homeviewforuser)
        self.givefeed.clicked.connect(self.feedGF)
        self.SUBMITfEEDBACK.clicked.connect(self.giveFeedback)
        self.menushow.clicked.connect(self.viewMeal)
        self.mealbuy.clicked.connect(self.meal_purchase)
        self.placebtn.clicked.connect(self.place_order)
        self.billcheckbtn.clicked.connect(self.bill_check)
        self.mealsearch.clicked.connect(self.searchFrame)
        self.searchbtn.clicked.connect(self.search_meal)
        self.orderlistbtn.clicked.connect(self.frame_order)
        self.dequebtn.clicked.connect(self.remove_order)  # order remove button
        self.adminUI.hide()
        self.usersUI.hide()
        self.feedview.hide()
        self.feedgive.hide()
        self.next_window = None

    def prev(self):
        self.loginFrame.show()

    def next_page(self):
        self.loginFrame.hide()

    def logout(self):
        self.adminUI.hide()
        self.loginFrame.show()

    def logout1(self):
        self.usersUI.hide()
        self.adminUI.hide()
        self.loginFrame.show()

    def homeview(self):
        self.feedview.hide()
        self.addmealframe.hide()
        self.removemealframe.hide()
        self.changepricemealframe.hide()
        self.orderlist.hide()
        self.Home.show()

    def homeviewforuser(self):
        self.feedgive.hide()
        self.viewmeal.hide()
        self.bymeal.hide()
        self.billframe.hide()
        self.searchingframe.hide()
        self.Home1.show()

    def cutomerUI(self):
        self.usersUI.show()
        self.loginFrame.show()
        self.signUpFrame.show()
        self.adminUI.show()

    def mealframe(self):

        self.feedview.show()
        self.addmealframe.show()
        self.removemealframe.hide()
        self.changepricemealframe.hide()
        self.orderlist.hide()

    def mealframeremove(self):
        self.feedview.show()
        self.addmealframe.show()
        self.removemealframe.show()
        self.orderlist.hide()

    def feedGF(self):
        self.Home1.show()
        self.feedgive.show()
        self.viewmeal.hide()
        self.searchingframe.hide()

    def pricemealframeremove(self):
        self.feedview.show()
        self.addmealframe.show()
        self.removemealframe.show()
        self.changepricemealframe.show()
        self.orderlist.hide()

    def show_message_box(self, message):
        QMessageBox.information(None, 'Info', message)

    def load_Data(self):
        customer_list = file_handling.load_data()
        return customer_list

    def show_passwordS(self):
        if self.checkBox.isChecked():
            self.confirmLine.setEchoMode(QLineEdit.Normal)
            self.passLine.setEchoMode(QLineEdit.Normal)
        else:
            self.confirmLine.setEchoMode(QLineEdit.Password)
            self.passLine.setEchoMode(QLineEdit.Password)

    def show_passwordL(self):
        if self.checkBox_2.isChecked():
            self.passL.setEchoMode(QLineEdit.Normal)
        else:
            self.passL.setEchoMode(QLineEdit.Password)

    def createAccountClicked(self):
        self.create_Account()

    def reset_credentialS(self):
        self.usernameLine.clear()
        self.passLine.clear()
        self.confirmLine.clear()

    def reset_credentialL(self):
        self.nameL.clear()
        self.passL.clear()

    def create_Account(self):

        while True:
            username = self.usernameLine.text()

            if not Validation.is_valid_username(username):
                self.show_message_box(
                    "Invalid username. Enter at least 4 characters (only use alphabets, numbers, and underscore).")
                self.usernameLine.clear()
                return 0

            password = self.passLine.text()
            if not Validation.is_valid_password(password):
                self.show_message_box(
                    "Invalid password. At least 8 characters, containing uppercase, lowercase, numeric, and special"
                    " characters (#, $, %, &).")
                self.passLine.clear()
                return 0

            confirm_pass = self.confirmLine.text()
            if not Validation.is_valid_password(confirm_pass):
                self.show_message_box("Invalid Password")
                self.confirmLine.clear()
                return 0

            if password != confirm_pass:
                self.show_message_box("Passwords do not match. Please try again.")
                self.passLine.clear()
                self.confirmLine.clear()
                return 0

            if self.users.is_empty():
                data = info.Admin(username, password)
                self.users.add(username, password)
                file_handling.save_data(data)
                self.show_message_box("Sign up successfully as Admin")
                self.reset_credentialS()

            else:
                try:
                    data = info.Customer(username, password)
                    username_found, _, _, _ = self.users.search(data)
                    if username_found:
                        self.show_message_box("Username already exists. Please choose a different one.")
                        self.usernameLine.clear()
                    else:
                        self.users.add(username, password)
                        file_handling.save_data(data)
                        self.show_message_box("Sign up successful. You can now log in.")
                        self.reset_credentialS()

                except Exception as e:
                    print(e)
            self.reset_credentialS()
            return 1

    def login(self):
        username = self.nameL.text()
        password = self.passL.text()
        if username == "" or password == "":
            self.show_message_box("Fields required")
            return

        if not Validation.is_valid_username(username):
            self.show_message_box("Invalid username. Please enter a valid username.")
            self.nameL.clear()
        if not Validation.is_valid_password(password):
            self.show_message_box("Invalid password. Please enter a valid password.")
            self.passL.clear()
            return 0

        data = info.Node(username, password)
        self.index = None
        name_found, pass_found, role, self.index = self.users.search(data)
        if name_found and pass_found:
            if role == "customer":
                self.cutomerUI()
                self.homeviewforuser()
                self.label_46.setText(self.index.username)
            elif role == "admin":
                self.adminUI.show()
                self.homeview()
                self.label_29.setText(self.index.username)
        elif name_found:
            self.show_message_box("Password is incorrect.")
        else:
            self.show_message_box("Invalid username or password. Please try again.")
        self.reset_credentialL()

    def viewfeedback(self):
        self.feedview.show()
        self.addmealframe.hide()
        self.orderlist.hide()

        if not self.feedback_stack.is_empty():
            try:
                table_widget = self.tableView
                data = self.feedback_stack.getdata()
                self.tableView.setRowCount(len(data))
                table_widget.setColumnCount(len(data[0]))
                table_widget.setHorizontalHeaderLabels(["Username", "FeedBack", "Date"])
                for row, row_data in enumerate(data):
                    for col, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        table_widget.setItem(row, col, item)
            except Exception as e:
                print(e)
        else:
            self.stackedWidget.setCurrentIndex(1)

    def addMeal(self):
        name = self.mealN.text()
        name = name.upper()
        if not re.match("^[A-Za-z ]+$", name):
            self.show_message_box("Invalid name. Please enter only letters.")
            self.mealN.clear()
            return 0

        price_input = self.mealP.text()
        if not price_input:
            return
        try:
            price = int(price_input)
        except ValueError:
            self.show_message_box("Invalid price. Please enter a valid integer.")
            self.mealP.clear()
            return

        if not self.Meal.search_key(name):
            self.Meal.insertion(name, price)
            file_handling.save_avl(self.Meal.root)
            self.show_message_box("MEAL IS ADDED")
        else:
            self.show_message_box("Already in Menu")
        self.mealN.clear()
        self.mealP.clear()

    def change_meal_price(self):
        name = self.mealN_3.text()
        name = name.upper()
        self.stackedWidget_2.setCurrentIndex(0)
        if not re.match("^[A-Za-z ]+$", name):
            self.show_message_box("Invalid name. Please enter only letters.")
            self.mealN_3.clear()
            return 0

        if node := self.Meal.search_key(name):
            self.stackedWidget_2.setCurrentIndex(1)
            price_input = self.mealP_3.text()
            if not price_input:
                return
            try:
                price = int(price_input)
            except ValueError:
                self.show_message_box("Invalid price. Please enter a valid integer.")
                self.mealP_3.clear()
                return

            self.Meal.change_price(node, price)
            file_handling.save_avl(self.Meal.root)
            self.show_message_box("Price updated successfully.")
            self.stackedWidget_2.setCurrentIndex(0)
            self.mealN_3.clear()
            self.mealP_3.clear()
        else:
            self.show_message_box("Meal not found")
            self.mealN_3.clear()
            self.mealP_3.clear()

    def delete_meal(self):
        name = self.mealN_2.text()
        name = name.upper()

        if not re.match("^[A-Za-z ]+$", name):
            self.show_message_box("Invalid name. Please enter only letters.")
            self.mealN_2.clear()
            return

        if self.Meal.search_key(name):
            self.Meal.deletion(name)
            file_handling.save_avl(self.Meal.root)
            self.show_message_box("Meal Removed")
            self.mealN_2.clear()

        else:
            self.show_message_box("Meal not found")
            self.mealN_2.clear()

    def giveFeedback(self):

        feed = self.fb.text()
        mame = self.index.username
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = Feedback.FeedBack_Node(mame, date, feed)
        self.feedback_stack.push(data)
        file_handling.save_stack_data(self.feedback_stack)
        self.show_message_box("Your feedBack is submitted")
        self.fb.clear()

    def viewMeal(self):
        self.viewmeal.show()
        self.feedgive.show()
        self.Home1.show()
        self.bymeal.hide()
        self.stackedWidget_3.setCurrentIndex(0)
        if not self.Meal.empty():
            self.stackedWidget_3.setCurrentIndex(0)
            try:
                table_widget = self.tableViewmeal
                data = self.Meal.get_data()
                self.tableViewmeal.setRowCount(len(data))
                table_widget.setColumnCount(len(data[0]) + 1)  # Add one column for the button

                # Set the horizontal header labels
                header_labels = ["Name", "Price", "Add To Cart"]
                table_widget.setHorizontalHeaderLabels(header_labels)

                # Add a button to the last column
                for row, row_data in enumerate(data):
                    for col, col_data in enumerate(row_data.values()):
                        item = QTableWidgetItem(str(col_data))
                        table_widget.setItem(row, col, item)

                    button = QPushButton("Add to cart")
                    button.clicked.connect(self.onButtonClick)
                    table_widget.setCellWidget(row, len(data[0]), button)


            except Exception as e:
                print(e)
        else:
            self.stackedWidget_3.setCurrentIndex(1)

    def onButtonClick(self):
        button = self.sender()
        if button:
            row = self.tableViewmeal.indexAt(button.pos()).row()
            item_name = self.tableViewmeal.item(row, 0).text()
            item_price = float(self.tableViewmeal.item(row, 1).text())

            if any(name == item_name for name, _, _ in self.cart):
                self.cart = [(name, price, quantity) for name, price, quantity in self.cart if name != item_name]
                self.show_message_box(f"{item_name} removed from cart")
                button.setText("Add to cart")
            else:
                self.cart.append((item_name, item_price, 1))
                self.show_message_box(f"{item_name} added to cart")
                button.setText("Remove from cart")
    def meal_purchase(self):
        self.bymeal.show()
        self.feedgive.show()
        self.viewmeal.show()
        self.billframe.hide()
        self.searchingframe.hide()

        cart_table = self.tableWidgetby
        cart_table.setColumnCount(5)
        cart_table.setHorizontalHeaderLabels(["Item Name", "Price", "Quantity", "Total Price", "Cancel"])

        if not self.cart:
            self.stackedWidget_4.setCurrentIndex(1)
        else:

            self.stackedWidget_4.setCurrentIndex(0)
            for row, (item_name, item_price, quantity) in enumerate(self.cart):
                item_already_in_table = False
                for existing_row in range(cart_table.rowCount()):
                    if cart_table.item(existing_row, 0).text() == item_name:
                        item_already_in_table = True

                        quantity_combobox = cart_table.cellWidget(existing_row, 2)
                        current_quantity = int(quantity_combobox.currentText())
                        new_quantity = current_quantity
                        quantity_combobox.setCurrentText(str(new_quantity))

                        self.update_total_price(existing_row, item_price, quantity_combobox)
                        break

                if not item_already_in_table:
                    item_name_item = QTableWidgetItem(item_name)
                    item_price_item = QTableWidgetItem(str(item_price))

                    cart_table.insertRow(row)
                    cart_table.setItem(row, 0, item_name_item)
                    cart_table.setItem(row, 1, item_price_item)

                    quantity_combobox = QComboBox()
                    quantity_combobox.addItems(map(str, range(1, 10)))
                    quantity_combobox.setCurrentText(str(quantity))
                    quantity_combobox.currentIndexChanged.connect(
                        lambda _, r=row, p=item_price, qc=quantity_combobox: self.update_total_price(r, p, qc))
                    cart_table.setCellWidget(row, 2, quantity_combobox)

                    total_price_item = QTableWidgetItem(str(item_price * quantity))
                    cart_table.setItem(row, 3, total_price_item)

                    cancel_button = QPushButton("Cancel")
                    cancel_button.clicked.connect(lambda _, r=row: self.cancel_order_row(r))
                    cart_table.setCellWidget(row, 4, cancel_button)

    def update_total_price(self, row, item_price, quantity_combobox):
        new_quantity = int(quantity_combobox.currentText())
        new_total_price = new_quantity * item_price

        total_price_item = QTableWidgetItem(str(new_total_price))
        self.tableWidgetby.setItem(row, 3, total_price_item)

    def cancel_order_row(self, row):
        if row < self.tableWidgetby.rowCount():
            self.tableWidgetby.removeRow(row)

        if row < len(self.cart):
            del self.cart[row]

        if not self.cart:
            self.stackedWidget_4.setCurrentIndex(1)
    def place_order(self):
        if not self.cart:
            self.show_message_box("Cart is Empty")
        else:

            file_path = "order_data.csv"
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Item Name", "Price", "Quantity", "Total Price"])
                for row in range(self.tableWidgetby.rowCount()):
                    item_name = self.tableWidgetby.item(row, 0).text()
                    item_price = float(self.tableWidgetby.item(row, 1).text())
                    quantity = int(self.tableWidgetby.cellWidget(row, 2).currentText())
                    total_price = float(self.tableWidgetby.item(row, 3).text())

                    writer.writerow([item_name, item_price, quantity, total_price])

            self.cart.clear()

            cart_table = self.tableWidgetby
            cart_table.setRowCount(0)
            self.show_message_box("Order Has Been Placed")
            self.displayBill = True
            order_info = order_queue.QueueObject(self.index.username, self.order_no)
            self.order_no += 1
            self.queue.enqueue(order_info)
            self.queue_table()
            self.stackedWidget_4.setCurrentIndex(1)

    def bill_check(self):
        self.billframe.show()
        self.bymeal.show()
        self.viewmeal.show()
        self.feedgive.show()
        self.searchingframe.hide()
        file_path = 'order_data.csv'
        total_bill = 0
        self.stackedWidget_5.setCurrentIndex(1)
        if self.displayBill:
            self.stackedWidget_5.setCurrentIndex(0)
            self.tableWidgetbill.setRowCount(0)
            try:
                with open(file_path, mode='r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    self.tableWidgetbill.setColumnCount(len(header))
                    self.tableWidgetbill.setHorizontalHeaderLabels(header)

                    for row_data in reader:
                        row_position = self.tableWidgetby.rowCount()
                        self.tableWidgetbill.insertRow(row_position)

                        item_price = float(row_data[1])
                        quantity = int(row_data[2])
                        total_price = item_price * quantity
                        total_bill += total_price

                        for column, data in enumerate(row_data):
                            item = QTableWidgetItem(data)
                            self.tableWidgetbill.setItem(row_position, column, item)

                            # Add quantity option as a combobox
                            if column == 2:
                                quantity_combobox = QComboBox()
                                quantity_combobox.addItems(map(str, range(1, 10)))
                                quantity_combobox.setCurrentText(data)
                                quantity_combobox.currentIndexChanged.connect(
                                    lambda _, r=row_position, qc=quantity_combobox: self.update_total_price(r, qc))
                                self.tableWidgetby.setCellWidget(row_position, 2, quantity_combobox)

                        # Add total price item
                        total_price_item = QTableWidgetItem(str(total_price))
                        self.tableWidgetbill.setItem(row_position, 3, total_price_item)

                        # Add cancel button
                        cancel_button = QPushButton("Cancel")
                        cancel_button.clicked.connect(lambda _, r=row_position: self.cancel_order_row(r))
                        self.tableWidgetbill.setCellWidget(row_position, 4, cancel_button)

            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")

            self.label_59.setText(str(total_bill))

    def searchFrame(self):
        self.billframe.show()
        self.bymeal.show()
        self.viewmeal.show()
        self.feedgive.show()
        self.searchingframe.show()

    def search_meal(self):
        self.stackedWidget_7.setCurrentIndex(0)
        meal_name = self.searchL.text()
        meal_name = meal_name.upper()
        node = self.Meal.search_key(meal_name)
        if node:
            self.stackedWidget_7.setCurrentIndex(1)
            self.label_88.setText(str(node.name))
            self.label_90.setText(str(node.price))
        else:
            self.show_message_box('Not found')
            self.stackedWidget_7.setCurrentIndex(0)

    def frame_order(self):
        self.feedview.show()
        self.addmealframe.show()
        self.removemealframe.show()
        self.changepricemealframe.show()
        self.orderlist.show()
        if not self.queue.is_empty():
            self.stackedWidget_6.setCurrentIndex(0)
        else:
            self.stackedWidget_6.setCurrentIndex(1)

    def queue_table(self):
        data = list(self.queue.items)
        self.tableWidgetlist.setRowCount(len(data))
        self.tableWidgetlist.setColumnCount(2)
        self.tableWidgetlist.setHorizontalHeaderLabels(["Name", "Order No"])
        for row, item in enumerate(data):
            item_name = QTableWidgetItem(item.name)
            item_order_no = QTableWidgetItem(str(item.order_no))
            self.tableWidgetlist.setItem(row, 0, item_name)
            self.tableWidgetlist.setItem(row, 1, item_order_no)

    def remove_order(self):
        if not self.queue.is_empty():
            self.queue.dequeue()
            self.queue_table()
            if self.queue.is_empty():
                self.stackedWidget_6.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
