import tkinter as tk
from tkinter import ttk

import mysql.connector
import mysql

mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="12345678",
                                   database="mydb")


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = mydb
        self.view_records()


    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="")
        btn_open_dialog = tk.Button(toolbar, text="Добавить позицию",
                                    command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_edit_dialog = tk.Button(toolbar, text="Редактировать позицию",
                                    command=self.open_update_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete_dialog = tk.Button(toolbar, text="Удалить",
                                    command=self.delete_records, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, column=("id","name", "surname", "thirdname", "number", "letter"), height=15, show='headings')
        self.tree.column("id", width=95, anchor=tk.CENTER)
        self.tree.column("name", width=95, anchor=tk.CENTER)
        self.tree.column("surname", width=95, anchor=tk.CENTER)
        self.tree.column("thirdname", width=95, anchor=tk.CENTER)
        self.tree.column("number", width=95, anchor=tk.CENTER)
        self.tree.column("letter", width=95, anchor=tk.CENTER)


        self.tree.heading("id", text='id')
        self.tree.heading("name", text='Имя')
        self.tree.heading("surname", text='Фамилия')
        self.tree.heading("thirdname", text='Отчество')
        self.tree.heading("number", text='Класс')
        self.tree.heading("letter", text='Буква')


        self.tree.pack()

    def records(self, name, surname, thirdname, number, letter):
        self.db.insert_data(name, surname, thirdname, number, letter)
        self.view_records()

    def update_records(self, name, surname, thirdname, number, letter):
        self.db.c.execute('''UPDATE `student` SET `name` = %s, `surname` = %s, `thirdname` = %s, `number` = %s, `letter` = %s WHERE (`id` = %s);''',( name, surname, thirdname, number, letter, self.tree.set(
                                                                                                                    self.tree.selection()[0],'#1')))
        self.view_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM `student` WHERE (`id` = %s);''', (self.tree.set(selection_item,'#1'),))
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM student;''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()




class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить пользователя")
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='имя')
        label_name.place(x=50, y=50)
        label_surname = tk.Label(self, text='фамилия')
        label_surname.place(x=50, y=75)
        label_thirdname = tk.Label(self, text='отчество')
        label_thirdname.place(x=50, y=100)
        label_number = tk.Label(self, text='класс')
        label_number.place(x=50, y=125)
        label_letter = tk.Label(self, text='буква')
        label_letter.place(x=50, y=150)


        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=75)

        self.entry_thirdname = ttk.Entry(self)
        self.entry_thirdname.place(x=200, y=100)

        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=125)

        self.entry_letter = ttk.Entry(self)
        self.entry_letter.place(x=200, y=150)

        btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        btn_cancel.place(x=300, y=185)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=185)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),self.entry_surname.get(),
                                                                       self.entry_thirdname.get(), self.entry_number.get(),
                                                                  self.entry_letter.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = mydb


    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=185)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_name.get(),self.entry_surname.get(),
                                                                       self.entry_thirdname.get(), self.entry_number.get(),
                                                                  self.entry_letter.get()))

        self.grab_set()
        self.focus_set()









class DB:
    def __init__(self):
        self.db = mydb
        self.c = self.db.cursor()



    def insert_data(self, name, surname, thirdname, number, letter):
        self.c.execute('''INSERT INTO `student`(`name`, `surname`, `thirdname`, `number`, `letter`) VALUES (%s, %s, %s, %s, %s);''',(name, surname, thirdname, number, letter))
        self.db.commit()





if __name__ == "__main__":
    root = tk.Tk()
    mydb = DB()
    app = Main(root)
    app.pack()
    root.title("Пользователи")
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()
