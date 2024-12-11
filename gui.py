import sys, os
from sys import path

import tkinter as tk
from tkinter import ttk

path.append(path[0] + '\\helpers')

import database as postgres
import guihelper as guihelper
import frame as frame

fontstyle = ("Helvetica", 20)

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        # Set icons, title, and window size
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default='./icons/now-black.ico')
        tk.Tk.wm_title(self, 'База Данных АвтоВокзала')
        self.geometry("1024x768")

        # Apply dark theme
        self.configure(bg="#808080")

        # Setup frame layout for application
        container = tk.Frame(self, bg="#808080")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frame "Router" for use in the index
        self.frames = {}
        for Frame in (Index, View, Connection, CreateUser, Insert):

            frame = Frame(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[Frame] = frame

        self.show_frame(Index)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Index(tk.Frame):
    def __init__(self, parent, controller):
        
        # Setup frame layout
        self.connectionstr = tk.StringVar()

        tk.Frame.__init__(self, parent, bg="#808080")
        label = tk.Label(self, text="Управление Базой Данных", font=fontstyle, bg="#808080", fg="#FFFF00")
        label.pack(pady=40, padx=100)

        button_frame = tk.Frame(self, bg="#808080")
        button_frame.pack(pady=20)

        button2 = ttk.Button(button_frame, text="Просмотр и Изменение Данных", command=lambda: controller.show_frame(View))
        button3 = ttk.Button(button_frame, text="Добавить Новую Запись", command=lambda: controller.show_frame(Insert))
        editconn = ttk.Button(button_frame, text="Подключение к БД", command=lambda: controller.show_frame(Connection))
        newuser = ttk.Button(button_frame, text="Создать Нового Пользователя", command=lambda: controller.show_frame(CreateUser))

        for button in [button2, button3, editconn, newuser]:
            button.pack(pady=10)

        bottom = tk.Frame(self, bg="#808080")
        bottom.pack(side='bottom', pady=20)

        test = ttk.Button(bottom, text="Тест Подключения", command=lambda: guihelper.connectionTest(self))
        historybutton = ttk.Button(bottom, text="Сохранить Историю Запросов", command=lambda: guihelper.saveQueryHistory())
        defaultconn = ttk.Button(bottom, text="Использовать Настройки По Умолчанию", command=lambda: guihelper.setdefaultconfig(self))

        for button in [test, historybutton, defaultconn]:
            button.pack(pady=5)

class View(tk.Frame):
    def __init__(self, parent, controller):

        self.console = tk.StringVar()
        tk.Frame.__init__(self, parent, bg="#808080")
        frame.View(self, parent, controller)

        bottom = tk.Frame(self, bg="#808080")
        bottom.pack(side='bottom', pady=20)
        ttk.Button(bottom, text="Вернуться в Главное Меню", command=lambda: controller.show_frame(Index)).pack(pady=15)

class Insert(tk.Frame):
    def __init__(self, parent, controller):

        self.console = tk.StringVar()
        tk.Frame.__init__(self, parent, bg="#808080")
        frame.Insert(self, parent, controller)

        bottom = tk.Frame(self, bg="#808080")
        bottom.pack(side='bottom', pady=20)
        ttk.Button(bottom, text="Вернуться в Главное Меню", command=lambda: controller.show_frame(Index)).pack(pady=15)

class Connection(tk.Frame):
    def __init__(self, parent, controller):
        self.connectionstr = tk.StringVar()

        tk.Frame.__init__(self, parent, bg="#808080")       
        bottom = tk.Frame(self, bg="#808080")
        bottom.pack(side='bottom', pady=20)

        frame.Connection(self, parent)

        index = ttk.Button(bottom, text="Вернуться в Главное Меню", command=lambda: controller.show_frame(Index))
        index.pack(pady=15)

class CreateUser(tk.Frame):
    def __init__(self, parent, controller):
        self.connectionstr = tk.StringVar()

        tk.Frame.__init__(self, parent, bg="#808080")       
        bottom = tk.Frame(self, bg="#808080")
        bottom.pack(side='bottom', pady=20)

        frame.NewUser(self, parent)

        index = ttk.Button(bottom, text="Вернуться в Главное Меню", command=lambda: controller.show_frame(Index))
        index.pack(pady=15)

# Apply custom style for buttons
style = ttk.Style()
style.configure("TButton", background="#FFFF00", foreground="#808080", borderwidth=2, relief="solid", font=("Helvetica", 12))

if __name__ == "__main__":
    app = main()
    app.mainloop()