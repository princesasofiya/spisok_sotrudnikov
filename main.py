import tkinter as tk
import tkinter.ttk as ttk
import sqlite3 as sl
from tkinter.messagebox import askyesno, showinfo

#Подключение к бд
con = sl.connect("sotrudnik.db")
cur = con.cursor()

#Глобальная переменная id выбранного сотрудника
values = [0]

#создание таблицы в Базе данных если ее нет
def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS sotrudnik(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         fam TEXT,
         name TEXT,
         otch TEXT,
         phone TEXT,
         email TEXT,
         salary TEXT
         )""")
    con.commit()

#Создание окна Добавления и редактирования сотрудников
def edit_sotrudnik():
    global values
    top=tk.Toplevel()
    top.title("Редактирование")
    label1 = ttk.Label(top, text="Фамилия: ")
    entry1 = ttk.Entry(top)
    label2 = ttk.Label(top,text="Имя: ")
    entry2 = ttk.Entry(top)
    label3 = ttk.Label(top,text="Отчество: ")
    entry3 = ttk.Entry(top)
    label4 = ttk.Label(top,text="Телефон: ")
    entry4 = ttk.Entry(top)
    label5 = ttk.Label(top,text="Почта: ")
    entry5 = ttk.Entry(top)
    label6 = ttk.Label(top,text="Зарплата: ")
    entry6 = ttk.Entry(top)
    label1.grid(row=0,column=0)
    label2.grid(row=1,column=0)
    label3.grid(row=2,column=0)
    label4.grid(row=3,column=0)
    label5.grid(row=4,column=0)
    label6.grid(row=5,column=0)
    entry1.grid(row=0,column=1)
    entry2.grid(row=1,column=1)
    entry3.grid(row=2,column=1)
    entry4.grid(row=3,column=1)
    entry5.grid(row=4,column=1)
    entry6.grid(row=5,column=1)
    if int(values[0]) > 0:
       entry1.insert(0, values[1])
       entry2.insert(0, values[2])
       entry3.insert(0, values[3])
       entry4.insert(0, values[4])
       entry5.insert(0, values[5])
       entry6.insert(0, values[6])
    def save():
        if int(values[0]) > 0:
            cur.execute(f"update sotrudnik set fam='{entry1.get()}',name='{entry2.get()}',otch='{entry3.get()}',phone='{entry4.get()}',email='{entry5.get()}',salary='{entry6.get()}'  where id={int(values[0])}")
        else:
            cur.execute(f"insert into sotrudnik (fam,name,otch,phone,email,salary) values('{entry1.get()}','{entry2.get()}','{entry3.get()}','{entry4.get()}','{entry5.get()}','{entry6.get()}')")
        con.commit()
        top.destroy()
        seldata()
    btn_save = ttk.Button(top , text = "Сохранить", command = save)
    btn_save.grid(row=7,column=0)
    btn_cancel = ttk.Button(top , text = "Отмена", command = top.destroy)
    btn_cancel.grid(row=7,column=1)

#Новый сотрудник
def new_sot():
    global values
    values = [0]
    edit_sotrudnik()

#Редактирование сотрудника
def edit_sot():
    global values
    if int(values[0]) == 0:
       showinfo(title="Информация", message="Вы не выбрали сотрудника для редактирования!!!")
    else:
       edit_sotrudnik()

#Вычисление выбранной строки в таблице
def on_select(event):
    global values
    if not tree.selection():
        return
    # Получаем id первого выделенного элемента
    selected_item = tree.selection()[0]
    # Получаем значения в выделенной строке
    values = tree.item(selected_item, option="values")

#Выборка всех сотрудников
def seldata(sql="SELECT * FROM `sotrudnik`"):
   tree.delete(*tree.get_children())
   cur.execute(sql)
   fetch = cur.fetchall()
   for data in fetch:
      tree.insert('', 'end', values=(data[0], data[1], data[2],data[3], data[4], data[5], data[6]))

#Удаление сотрудника
def del_sot():
   global values
   if int(values[0]) > 0:
       result = askyesno(title="Подтвержение удаления", message="Удалить Выбранную запись?")
       if result:
           cur.execute(f"delete FROM `sotrudnik` where id={int(values[0])}")
           con.commit()
   seldata()

#Очистить поиск
def reset_find():
    entry.delete(0, 'end')
    seldata()

#Поиск сотрудника
def find_sot(event):
    find = entry.get()
    sel = "SELECT * FROM `sotrudnik`"
    sqlsel = f"{sel} where fam LIKE '%{find}%' or name LIKE '%{find}%' or otch LIKE '%{find}%' or phone LIKE '%{find}%' or email LIKE '%{find}%' or salary LIKE '%{find}%'"
    seldata(sqlsel)

#Создание основного окна приложения
app = tk.Tk()
create_table()
app.resizable(False, False)
app.title("Список сотрудников компании")
label = ttk.Label(text="Поиск: ")
entry = ttk.Entry()
entry.bind('<KeyPress>', find_sot)
btn = ttk.Button(text="Сброс поиска", command = reset_find)
btn_add = ttk.Button(text="Добавить", command = new_sot)
btn_edit = ttk.Button(text="Редактировать", command = edit_sot)
btn_del = ttk.Button(text="Удалить", command = del_sot)
columns = ("#1","#2","#3","#4","#5","#6","#7")
tree = ttk.Treeview(show="headings", columns = columns)
tree.bind('<<TreeviewSelect>>', on_select)
tree.heading("#1", text="№")
tree.heading("#2", text="Фамилия")
tree.heading("#3", text="Имя")
tree.heading("#4", text="Отчество")
tree.heading("#5", text="Телефон")
tree.heading("#6", text="Почта")
tree.heading("#7", text="Зарплата ")
tree.column('#1', width=50)
tree.column('#2', width=130)
tree.column('#3', width=130)
tree.column('#4', width=130)
tree.column('#5', width=100)
tree.column('#6', width=120)
tree.column('#7', width=80)
ysb = ttk.Scrollbar(orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=ysb.set)
seldata()
label.grid(row=0, column=1)
entry.grid(row=0, column=2)
btn.grid(row=0, column=3)
tree.grid(row=1, column=0, columnspan=4)
ysb.grid(row=1, column=5, sticky=tk.N + tk.S)
btn_add.grid(row=3, column=1)
btn_edit.grid(row=3, column=2)
btn_del.grid(row=3, column=3)


app.mainloop()

