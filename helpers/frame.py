import sys, os
import tkinter as tk
from tkinter import ttk
import database as postgres
import guihelper as guihelper

fontstyle = ("Helvetica", 18)

def View(self, parent, controller):

    self.treeview = None

    label = tk.Label(self, text="Просмотр таблицы", font=fontstyle, bg="black", fg="yellow")
    label.pack(pady=(15, 75), padx=100)

    options = ["post", "employee", "application_log", "bounce_log", "reason_refusal"]
    choice = tk.StringVar()
    choice.set(options[0])
    textbox = tk.OptionMenu(self, choice, *options)
    textbox.configure(bg="black", fg="yellow")

    label = ttk.Label(self, text="Выберите таблицу из списка", background="black", foreground="yellow")
    table = tk.Frame(self, width=500, height=100, bg="black")
    selectbutton = ttk.Button(self, text="Посмотреть/Обновить", command=lambda: guihelper.loadTable(self, table, choice))
    conditionselectbutton = ttk.Button(self, text="Расширенный поиск", command=lambda: guihelper.conditionSelect(self, table, choice))
    output = ttk.Label(self, textvariable=self.console, background="black", foreground="yellow")

    label.pack()
    textbox.pack()
    selectbutton.pack(pady=15)
    conditionselectbutton.pack()
    output.pack(pady=(30, 10))

    guihelper.drawTable(table)  # draws empty table view
    prev = ttk.Button(table, text="Предыдущие 10", command=lambda: guihelper.loadPrev(self, table, textbox))
    next = ttk.Button(table, text="Следующие 10", command=lambda: guihelper.loadNext(self, table, textbox))
    prev.pack()
    next.pack()
    table.pack(fill="none", expand=False)

def Insert(self, parent, controller):

    label = tk.Label(self, text="Вставка данных в таблицу", font=fontstyle, bg="black", fg="yellow")
    label.pack(pady=(15, 75), padx=100)

    label = ttk.Label(self, text="Выберите таблицу из списка", background="black", foreground="yellow")
    options = ["post", "employee", "application_log", "bounce_log", "reason_refusal"]
    choice = tk.StringVar()
    choice.set(options[0])
    textbox = tk.OptionMenu(self, choice, *options)
    textbox.configure(bg="black", fg="yellow")

    zonebutton = ttk.Button(self, text="Подтвердить", command=lambda: guihelper.loadColumnFlags(self, choice))
    output = ttk.Label(self, textvariable=self.console, background="black", foreground="yellow")

    label.pack()
    textbox.pack()
    zonebutton.pack(pady=15)
    output.pack(pady=(30, 10))

def ManageUsers(self, parent, controller):

    label = tk.Label(self, text="Управление пользователями", font=fontstyle, bg="black", fg="yellow")
    label.pack(pady=(15, 75), padx=100)
    updateusers = ttk.Button(self, text="Обновить список пользователей", command=lambda: guihelper.getUsernames())
    updateusers.pack()

def Connection(self, parent):

    label = tk.Label(self, text="Параметры подключения", font=fontstyle, bg="black", fg="yellow")
    label.pack(pady=50, padx=100)

    self.host = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    hostLabel = ttk.Label(self, text="Хост (optional):", background="black", foreground="yellow")
    self.dbname = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    dbnameLabel = ttk.Label(self, text="Название БД (optional):", background="black", foreground="yellow")
    self.user = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    userLabel = ttk.Label(self, text="Логин:", background="black", foreground="yellow")
    self.password = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    passwordLabel = ttk.Label(self, text="Пароль:", background="black", foreground="yellow")

    create = ttk.Button(self, text="Подтвердить", command=lambda: guihelper.setConfig(self))
    output = ttk.Label(self, textvariable=self.connectionstr, background="black", foreground="yellow")

    hostLabel.pack()
    self.host.pack()
    dbnameLabel.pack()
    self.dbname.pack()
    userLabel.pack()
    self.user.pack()
    passwordLabel.pack()
    self.password.pack()

    create.pack(pady=25)
    output.pack()

def NewUser(self, parent):

    label = tk.Label(self, text="Регистрация", font=fontstyle, bg="black", fg="yellow")
    label.pack(pady=50, padx=100)

    self.user = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    userLabel = ttk.Label(self, text="Логин:", background="black", foreground="yellow")
    self.password = tk.Text(self, height=1, width=25, bg="black", fg="yellow", insertbackground="yellow")
    passwordLabel = ttk.Label(self, text="Пароль:", background="black", foreground="yellow")

    create = ttk.Button(self, text="Зарегистрироваться", command=lambda: guihelper.createNewUser(self))
    output = ttk.Label(self, textvariable=self.connectionstr, background="black", foreground="yellow")

    userLabel.pack()
    self.user.pack()
    passwordLabel.pack()
    self.password.pack()

    create.pack(pady=25)
    output.pack()