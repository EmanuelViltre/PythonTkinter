from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re

########################################## CREO TABLA DE BASE DE DATOS ##################################


def conexion():
    con = sqlite3.connect("base.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE operaciones
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre VARCHAR(255) NOT NULL,
             apellido VARCHAR(255) NOT NULL,
             operacion real NOT NULL,
             producto VARCHAR(50))
    """
    cursor.execute(sql)
    con.commit()


try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")


########################################## DEFINO FUNCIONES ##################################
con = conexion()


def alta(nombre, apellido, operacion, producto, tree):
    producto_regex = producto
    patron = "^[A-Za-záéíóú]*$"
    if re.match(patron, producto_regex):
        print(nombre, apellido, operacion, producto)
        con = conexion()
        cursor = con.cursor()
        data = (nombre, apellido, operacion, producto)
        sql = "INSERT INTO operaciones(nombre, apellido, operacion, producto) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        actualizar_treeview(tree)
        messagebox.showinfo("Alta", "Alta satisfactoria")
    else:
        print("error")
        messagebox.showerror("Error", "Alta insatisfactoria")


def consultar():
    global nombre
    global apellido
    global operacion
    global producto

    actualizar_treeview(tree)


def borrar(tree):
    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item["text"]
    con = conexion()
    cursor = con.cursor()
    data = (mi_id,)
    sql = "DELETE FROM operaciones WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    messagebox.showinfo("Borrar", "Elemento eliminado")


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM operaciones ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert(
            "", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4])
        )


####################################### VISTA ############################################


root = Tk()


root.title("Proyecto Final")

titulo = Label(
    root,
    text="Ingrese los datos de la Operacion",
    bg="white",
    fg="black",
    height=1,
    width=80,
)


titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W + E)
nombre = Label(root, text="Nombre")
nombre.grid(row=1, column=0, sticky=W)
apellido = Label(root, text="Apellido")
apellido.grid(row=2, column=0, sticky=W)
operacion = Label(root, text="Operacion")
operacion.grid(row=3, column=0, sticky=W)
producto = Label(root, text="Producto")
producto.grid(row=4, column=0, sticky=W)

n_val, a_val, o_val, p_val = StringVar(), StringVar(), DoubleVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable=n_val, width=w_ancho)
entrada1.grid(row=1, column=0)
entrada2 = Entry(root, textvariable=a_val, width=w_ancho)
entrada2.grid(row=2, column=0)
entrada3 = Entry(root, textvariable=o_val, width=w_ancho)
entrada3.grid(row=3, column=0)
entrada4 = Entry(root, textvariable=p_val, width=w_ancho)
entrada4.grid(row=4, column=0)


####################################### TREEVIEW ############################################


tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Apellido")
tree.heading("col3", text="Operacion")
tree.heading("col4", text="Producto")
tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(
    root,
    text="Alta",
    command=lambda: alta(n_val.get(), a_val.get(), o_val.get(), p_val.get(), tree),
)
boton_alta.grid(row=3, column=1)

boton_consulta = Button(root, text="Consultar", command=lambda: consultar())
boton_consulta.grid(row=3, column=2)

boton_borrar = Button(root, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=3, column=3)


root.mainloop()
