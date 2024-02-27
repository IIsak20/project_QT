import sys
import random
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox

data_code = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't',
             'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
             'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S',
             'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

data_login = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a',
              's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
              'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S',
              'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']


class MyWidget(QMainWindow):  # главный класс. тут происходит проверка на базу
    def __init__(self, *args):  # и при отрицательном ответе создается новая
        super().__init__()
        uic.loadUi('designer/widget1.ui', self)
        self.connection = sqlite3.connect("data/Logins.sqlite")
        self.initUI()
        try:
            cur = self.connection.cursor()
            num = cur.execute('SELECT * FROM log_pas')
        except sqlite3.OperationalError:
            cur = self.connection.cursor()
            cur.execute(
                '''CREATE TABLE log_pas (
                      id        PRIMARY KEY
                                UNIQUE
                                NOT NULL,
                      plase,
                      login,
                      password
                    );
                    '''
            )

    # общий метод класса MyWidget
    def initUI(self):
        self.exit.clicked.connect(self.exit_def)
        self.start_generate_widget.clicked.connect(self.open_generate_code)
        self.table_start.clicked.connect(self.open_table)

    def open_table(self):  # открывает виджет с таблицой
        global widget_table
        widget_table = Table(self)
        widget_table.show()

    def open_generate_code(self):  # открывает виджет с генератором кода
        global widget_code
        widget_code = WidgetCode(self)
        widget_code.show()

    def exit_def(self):  # реализует кнопку выход
        sys.exit(app.exec())


class WidgetCode(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()

    # общий метод класса WidgetCode
    def initUI(self):
        uic.loadUi('designer/generate_code.ui', self)
        self.connection = sqlite3.connect('data/Logins.sqlite')

        self.back1.clicked.connect(self.back_on_widget1)
        self.generate_login.clicked.connect(self.start_generate_login)
        self.generate_code.clicked.connect(self.start_generate_code)
        self.save_data.clicked.connect(self.save_data_table)

    def start_generate_login(self):  # генерирует логин
        login_name = ''
        for i in range(self.kol_login.value()):
            login_name += random.choice(data_login)
        self.login.setText(login_name)

    def start_generate_code(self):  # генерирует пароль
        code_name = ''
        for i in range(self.kol_code.value()):
            code_name += random.choice(data_code)
        self.code.setText(code_name)

    def back_on_widget1(self):  # выход на главный виджет
        widget_code.hide()

    def save_data_table(self):  # сохраняет данные в таблицу паралельно шифруя их
        cur = self.connection.cursor()
        res = ''
        for i in self.code.text():
            ind = ord(i)
            ind_2 = int(ind) + 6
            res += chr(ind_2)
        self.password_ = res
        res = ''
        for i in self.login.text():
            ind = ord(i)
            ind_2 = int(ind) + 6
            res += chr(ind_2)
        self.login_ = res
        res = ''
        for i in self.plase_edit.text():
            ind = ord(i)
            ind_2 = int(ind) + 6
            res += chr(ind_2)
        self.plase_ = res
        num = cur.execute('SELECT * FROM log_pas')
        num_l = []
        for i, row in enumerate(num):
            z = row[0]
            res = ''
            for j in str(z):
                ind = ord(j)
                ind_2 = int(ind) - 6
                res += chr(ind_2)
            df = int(res)
            num_l.append(df)
        self.id_ = 0
        self.id_ += 1
        while True:
            if self.id_ in num_l:
                self.id_ += 1
            else:
                break
        res = ''
        for i in str(self.id_):
            ind = ord(i)
            ind_2 = int(ind) + 6
            res += chr(ind_2)
        self.id_ = str(res)
        cur.execute(f"""INSERT INTO log_pas(id, plase, login, password) 
        VALUES('{self.id_}', '{self.plase_}', '{self.login_}', '{self.password_}')""")
        res = ''
        for i in str(self.id_):
            ind = ord(i)
            ind_2 = int(ind) - 6
            res += chr(ind_2)
        self.id_ = int(res)
        self.connection.commit()


class Table(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()

    # общий метод класса Table, выводит элементы базы данных в таблицу паралельно дешифруя их
    def initUI(self):
        uic.loadUi('designer/table.ui', self)
        self.connection = sqlite3.connect('data/Logins.sqlite')
        res = self.connection.cursor().execute('''SELECT * FROM log_pas''').fetchall()
        self.table_widget.setColumnCount(4)

        for i, row in enumerate(res):
            self.table_widget.setRowCount(
                self.table_widget.rowCount() + 1)
            for j, elem in enumerate(row):
                res = ''
                for f in elem:
                    ind = ord(f)
                    ind_2 = int(ind) - 6
                    res += chr(ind_2)
                elem = res
                self.table_widget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.back2.clicked.connect(self.back_on_widget1_2)
        self.delete_elem.clicked.connect(self.delete_metod)

    def delete_metod(self):  # метод реализующий удаление элементов из базы данных
        rows = list(set([i.row() for i in self.table_widget.selectedItems()]))
        id_ = [self.table_widget.item(i, 0).text() for i in rows]
        object_ = QMessageBox.question(self, '', 'удалить записи' + ",".join(id_), QMessageBox.Yes, QMessageBox.No)
        if object_ == QMessageBox.Yes:
            cur = self.connection.cursor()
            id_l = list()
            for i in id_:
                res = ''
                for j in str(i):
                    ind = ord(j)
                    ind_2 = int(ind) + 6
                    res += chr(ind_2)
                id_l.append(res)
            id_l = "', '".join(id_l)
            cur.execute(f"DELETE from log_pas WHERE id IN ('{id_l}')")
            self.connection.commit()

    def back_on_widget1_2(self):  # выход на главный виджет
        widget_table.hide()


def except_hook(cls, exception, traceback):  # нормальный вывод ошибок
    sys.__excepthook__(cls, exception, traceback)


# проверка на завершение программы

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ss = WidgetCode()
    ss.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sq = Table()
    sq.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
