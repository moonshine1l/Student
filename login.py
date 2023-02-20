import tkinter as tk
import mysql.connector
from tkinter import *

def submitact():
    user = Username.get()
    passw = password.get()

    print(f"Вы ввели {user} {passw}")

    logintodb(user, passw)

def logintodb(user, passw):
    if passw:
        db = mysql.connector.connect(host = "localhost",
                                   user = user,
                                   password = passw,
                                   db="College")
        cursor = db.cursor()
    else:
        db = mysql.connector.connect(host="localhost",
                                     user=user,
                                     db="College")
        cursor = db.cursor()

    savequery = "select * from student"

    try:
        cursor.execute(savequery)
        myresult = cursor.fetchall()

        for x in myresult:
            print(x)
        print("Запрос успешно выполнен")

    except:
        db.rollback()
        print("Ошибка")


root = tk.Tk()
root.geometry("300x300")
root.title("Страница авторизации")

lblfrstrow = tk.Label(root, text="Username -",)
lblfrstrow.place(x = 50, y = 20)

Username = tk.Entry(root, width=35)
Username.place(x = 150, y = 20, width=100)

lblsecrow = tk.Label(root, text="Password -",)
lblsecrow.place(x = 50, y = 50)

password = tk.Entry(root, width=35)
password.place(x = 150, y = 50, width=100)

submitbtn = tk.Button (root, text="Войти",
                       bg='blue', command=submitact)
submitbtn.place(x = 150, y = 135, width=55)

root.mainloop()
