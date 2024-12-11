import database as postgres
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
import sys

config = []
query_history=[]
data = []
selection = []
tableptr = 0
table = ''
column_type_dict = {}
data_inside = {}
columnnames = []
list_of_lines = []
fontstyle = ("Helvetica", 18)

def connectionTest(self):

    if (len(config) == 0):
        err = 'Настройки подключения не указаны. Пожалуйста, настройте соединение.'
        self.connectionstr.set(err)
        return False

    if (postgres.connect(config)):
        success = 'Подключение успешно'
        self.connectionstr.set(success)
        return True
    else:
        fail = 'Подключения нет. Попробуйте поменять настройки соединения'
        self.connectionstr.set(fail)
        return False

def createNewUser(self):
    global config

    user = self.user.get('1.0', 'end-1c')
    pwd = self.password.get('1.0', 'end-1c')
    setdefaultconfig(self)

    postgres.createNewUser(user, pwd)
    config = ['localhost', 'wawa', user, pwd]
    print(config)

    connectionTest(self)


def setdefaultconfig(self):

    global config

    dbname = 'wawa'
    user = 'postgres'
    pwd = '36701'
    host = 'localhost'

    config = [host, dbname, user, pwd]

    if (postgres.connect(config)):
        success = 'Подключение успехно'
        self.connectionstr.set(success)
        return True

def setConfig(self):

    global config

    dbname = self.dbname.get('1.0', 'end-1c')
    user = self.user.get('1.0', 'end-1c')
    pwd = self.password.get('1.0', 'end-1c')
    host = self.host.get('1.0', 'end-1c')
    if dbname == "":
        dbname = "wawa"
    if host == "":
        host = "localhost"
    messagebox.showinfo("Успех", "Все данные успешно загружены и элементы добавлены.")

    config = [host, dbname, user, pwd]
    connectionTest(self)

def getConfig():

    return config

def setData(arr):

    global data
    data = arr

def getData():
    return data

def addToQueryHistory(query):
    global query_history
    query_history.append(query)

def saveQueryHistory():
    with open("log.txt",'a') as f:
        for line in query_history:
            f.write(line+"\n")

def setColumnNames(arr):
    global columnnames
    columnnames = arr

def getColumnNames():
    return columnnames
    
def getUsernames():
    names = []
    fetch = postgres.getUsers()
    for item in fetch:
        names.append(item[0])
    #fr.setOptions(names)
    return names

def getTable(self, textbox):
    global table

    table = textbox.get()
    postgres.viewColumnNames(table)
    output = postgres.viewrange(table,0)
    self.console.set(output)

def getNewPageTable(self):
    global column_type_dict
    global data_inside
    output = postgres.viewrange(table, tableptr,column_type_dict,data_inside)
    self.console.set(output)

def getName():
    return table

def getSelection():
    return selection

def setSelection(arr):
    global selection
    selection = arr

def item_select(_):
    global tv
    temp = []
    for i in tv.selection():
        temp.append(tv.item(i)['values'])
    setSelection(temp)
    print(temp)

def delete_items(_):
    global tv
    res = postgres.deleteItems()
    if res[0] !='Error deleting item.':
        for i in tv.selection():
            tv.delete(i)
    else:
        messagebox.showwarning("damn.",res[1])

def loadColumnLinesToChange(self, table_name, tselection):
    list_of_lines_to_change=[]
    try:
        data_types = {}# every column type except id
        for item in postgres.getDataType(table_name):
            if "id" not in item:
                data_types[item[0]] = item[1]
        print(postgres.viewColumnNames(table_name))#sets columnnames

        for item in range(len(columnnames)):#for each column
            if "id" not in columnnames[item]:
                set_text = tk.Text(self, height = 1, width = 25)
                set_text.insert(tk.END, tselection[0][item])
                list_of_lines_to_change.append([ttk.Label(self, text=f"{columnnames[item]} - {data_types[columnnames[item]]}"),set_text])
    
        for thing in list_of_lines_to_change:
            thing[0].pack()
            thing[1].pack()

        if len(list_of_lines_to_change)!=0:
            ttk.Label(self, text="").pack()
            ttk.Button(self, text = "Подтвердить изменения", command = lambda: help_update(self, table_name, tselection,
                [item[1].get('1.0', 'end-1c') for item in list_of_lines_to_change])).pack(pady = (10, 50))
    except Exception as e:
        print(e)

def help_update(self, table_name, tselection, vals):
    res = postgres.updateData(table_name, tselection, vals)
    if res[0]!='Error updating item.':
        self.destroy()
    else:
        messagebox.showwarning("damn.",res[1])


def change_item(_):
    if len(selection)!=1:
        print("Must select only ONE row.")
        return 
    changeItemWindow = tk.Tk()
    changeItemWindow.title("Item changer")
    #wm_title(self, 'SQL App')
    label = tk.Label(changeItemWindow, text="Изменение данных строки", font=fontstyle)
    label.pack(pady = (15, 25), padx = 100)
    label.pack()
    loadColumnLinesToChange(changeItemWindow, table, selection.copy())
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
def conditionSelect(self, table_frame, table_name):#.get() for name, self is tk.Frame
    if (table_frame.treeview is None):
        loadTable(self, table_frame, table_name)
    conditionSelectWindow = tk.Tk()
    conditionSelectWindow.title("Conditioned Select")
    #wm_title(self, 'SQL App')
    label = tk.Label(conditionSelectWindow, text="Расширенный поиск", font=fontstyle)
    label.pack(pady = (15, 0), padx = 100)
    ttk.Label(conditionSelectWindow, text=f"по таблице {table_name.get()}").pack(pady = (0, 15))
    loadColumnLinesToCondition(conditionSelectWindow, self, table_name.get(), table_frame)
    
def loadColumnLinesToCondition(self, old_self, table_name, table_frame):
    list_of_conditions_string=[]
    list_of_conditions_int=[]
    data_dict={}
    try:
        data_types = {}# every column type
        for item in postgres.getDataType(table_name):
            data_types[item[0]] = item[1]
        print(postgres.viewColumnNames(table_name))#sets columnnames
        #print(data_types)#{'id': 'integer', 'name': 'character varying', 'author': 'character varying', 'lenght': 'time without time zone'}
        for item in range(len(columnnames)):#for each integer column
            if data_types[columnnames[item]] == 'integer':
                data_dict[columnnames[item]] = data_types[columnnames[item]]
                list_of_conditions_int.append([ttk.Label(self, text=f"{columnnames[item]} - {data_types[columnnames[item]]}"),
                    tk.Text(self, height = 1, width = 25)])
        for item in range(len(columnnames)):#for each string column
            if data_types[columnnames[item]] == 'character varying':
                data_dict[columnnames[item]] = data_types[columnnames[item]]
                list_of_conditions_string.append([ttk.Label(self, text=f"{columnnames[item]} - {data_types[columnnames[item]]}"),
                    tk.Text(self, height = 1, width = 25)])       
        for thing in list_of_conditions_int:
            thing[0].pack()
            thing[1].pack()
        for thing in list_of_conditions_string:
            thing[0].pack()
            thing[1].pack()
        
        if len(list_of_conditions_int)+len(list_of_conditions_string)!=0:
            ttk.Label(self, text="").pack()
            ttk.Button(self, text = "Поиск", command = lambda: loadConditionTable(self, old_self, table_name, 
                data_dict, table_frame, [item[1].get('1.0', 'end-1c') for item in list_of_conditions_int], 
                [item[1].get('1.0', 'end-1c') for item in list_of_conditions_string])).pack(pady=10)
                #[item[1].get('1.0', 'end-1c') for item in list_of_conditions_int] 
                #[item[1].get('1.0', 'end-1c') for item in list_of_conditions_string]
                # these are text input areas
    except Exception as e:
        print(e)


def loadConditionTable(self, old_self, table_name, data_dict, table_frame,
        list_of_conditions_int, list_of_conditions_string):# self is main view frame
    global tableptr
    global table
    global tv
    global column_type_dict
    global data_inside

    table = table_name
    tableptr = 0
    typein = list_of_conditions_int+list_of_conditions_string#['12','NAME', 'AAA']
    dict_as_list=list(data_dict.items())#[('id', 'integer'), ('name', 'character varying'), ('author', 'character varying')]
    data_inside={}
    for i in range(len(typein)):
        data_inside[dict_as_list[i][0]] = typein[i]
    column_type_dict=data_dict

    postgres.viewColumnNames(table_name)
    postgres.viewrange(table_name, tableptr, data_dict, data_inside)

    if (table_frame.treeview is not None):
        remove_all(table_frame)

    temp = data
    if len(columnnames)!=0:
        table_frame.treeview['columns'] = tuple(columnnames)#changes headers dynamically
        for name in columnnames:
            table_frame.treeview.heading(name, text=name, anchor='w')
            table_frame.treeview.column(name, anchor='w', width=100)

    temp_array = []
    for entry in reversed(temp):
        for i in range(len(temp[0])):
            temp_array.append(entry[i])
        table_frame.treeview.insert('', 0, values=tuple(temp_array))
        temp_array = []
    #COPY LOADING HERE
    #loadTable(old_self, table_frame, temp)

    tv['show'] = 'headings'
    if len(columnnames) != 0:
        tv['columns'] = tuple(columnnames)
        for name in columnnames:
            tv.heading(name, text=name, anchor='w')
            tv.column(name, anchor='w', width=100)
    
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
def drawTable(self):
    global columnnames
    global tv
    tv = ttk.Treeview(self)
    tv['show'] = 'headings'
    if len(columnnames) != 0:
        tv['columns'] = tuple(columnnames)
        for name in columnnames:
            tv.heading(name, text=name, anchor='w')
            tv.column(name, anchor='w', width=100)
    else:
        tv['columns'] = ('1', '2', '3', '4', '5', '6', '7')
        for name in range(7):
            tv.heading(str(name+1), text=str(name+1), anchor='w')
            tv.column(str(name+1), anchor='w', width=100)
        tv.pack()
    tv.bind('<<TreeviewSelect>>', item_select)
    tv.bind('<Delete>', delete_items)
    tv.bind('<Double-Button-1>', change_item)
    self.treeview = tv


def loadTable(self, table, textbox):
    global tableptr
    global column_type_dict
    global data_inside
    column_type_dict={}
    data_inside={}

    tableptr = 0
    if (table.treeview is not None):
        remove_all(table)

    getTable(self, textbox)
    temp = data
    if len(columnnames)!=0:
        table.treeview['columns'] = tuple(columnnames)#changes headers dynamically
        for name in columnnames:
            table.treeview.heading(name, text=name, anchor='w')
            table.treeview.column(name, anchor='w', width=100)

    temp_array = []
    for entry in reversed(temp):
        for i in range(len(temp[0])):
            temp_array.append(entry[i])
        table.treeview.insert('', 0, values=tuple(temp_array))
        temp_array = []
    
def loadNext(self, table, textbox):

    global tableptr
    
    if (table.treeview is not None):
        remove_all(table)

    tableptr += 10
    getNewPageTable(self)
    temp_array = []
    temp = data
    for entry in reversed(temp):
        for i in range(len(temp[0])):
            temp_array.append(entry[i])
        table.treeview.insert('', 0, values=tuple(temp_array))
        temp_array = []
    
    
def getListToInsert():
    global list_of_lines
    temp_copy = list_of_lines.copy()
    temp_copy.pop()
    temp = []
    for item in temp_copy:
        temp.append(item[1].get('1.0', 'end-1c'))
    return temp

def help_insert(table_name):
    res = postgres.insert(table_name.get())
    messagebox.showinfo("Успех", "Все данные успешно загружены и элементы добавлены.")
    if res[0]=='Error inserting item.':
        messagebox.showwarning("damn.",res[1])
        
def loadColumnFlags(self, table_name):
    global list_of_lines
    try:
        if len(list_of_lines)!=0:
            for item in list_of_lines:
                item[0].destroy()
                item[1].destroy()
            list_of_lines=[]
        data_types = {}
        for item in postgres.getDataType(table_name.get()):
            if "id" not in item:
                data_types[item[0]] = item[1]
        print(postgres.viewColumnNames(table_name.get()))
        for item in columnnames:
            if "id" not in item:
                list_of_lines.append([ttk.Label(self, text=f"{item} - {data_types[item]}"),
                tk.Text(self, height = 1, width = 25)])
        if len(list_of_lines)!=0:
            list_of_lines.append([ttk.Label(self, text="Кнопка подтверждения"),
                ttk.Button(self, text = "Подтвердить", command = lambda: help_insert(table_name))])
        for thing in list_of_lines:
            thing[0].pack()
            thing[1].pack()
        messagebox.showinfo("Успех", "Таблица изменена.")
    except Exception as e:
        print(e)

def loadPrev(self, table, textbox):
    
    global tableptr
    if (tableptr > 0):
        if (table.treeview is not None):
            remove_all(table)
        tableptr -= 10
        getNewPageTable(self)
        temp_array = []
        temp = data
        for entry in reversed(temp):
            for i in range(len(temp[0])):
                temp_array.append(entry[i])
            table.treeview.insert('', 0, values=tuple(temp_array))
            temp_array = []


def remove_all(table):
    x = table.treeview.get_children()
    if x != '()':
        for child in x:
            table.treeview.delete(child)