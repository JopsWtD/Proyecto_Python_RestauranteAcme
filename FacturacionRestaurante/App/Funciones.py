from csv import DictWriter
from csv import DictReader
from pathlib import Path

rutaBase = Path(__file__).parent
ruta = rutaBase/"DB"

def crearProducto(codigo, tipoProducto, nombre, valor, iva):
    producto = {}

    producto["Código"] = codigo
    producto["Tipo_Producto"] = tipoProducto
    producto["Nombre"] = nombre
    producto["Valor"] = valor
    producto["IVA"] = iva

    while(True):
        try:
            with open (ruta/"Productos.csv","r",newline="",encoding="utf-8") as file:
                listaVacia = len(list(DictReader(file)))
            break
        except FileNotFoundError:
            with open (ruta/"Productos.csv", "w", newline="", encoding="utf-8"):
                pass

    with open (ruta/"Productos.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Producto","Nombre","Valor","IVA"])
        if listaVacia:
            writerCSV.writeheader()
        writerCSV.writerows([producto])

def crearMesa(codigo,tipoMesa,puestos):
    mesa = {}

    mesa["Código"] = codigo
    mesa["Tipo_Mesa"] = tipoMesa
    mesa["Cantidad_Puestos"] = puestos

    while(True):
        try:
            with open (ruta/"Mesas.csv","r",newline="",encoding="utf-8") as file:
                listaVacia = len(list(DictReader(file)))
            break
        except FileNotFoundError:
            with open (ruta/"Mesas.csv", "w", newline="", encoding="utf-8"):
                pass

    with open (ruta/"Mesas.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Mesa","Cantidad_Puestos"])
        if listaVacia:
            writerCSV.writeheader()
        writerCSV.writerows([mesa])


def crearCliente(id, nombre, telefono, email):
    cliente = {}
    
    cliente["ID"] = id
    cliente["Nombre"] = nombre
    cliente["Número de teléfono"] = telefono
    cliente["Email"] = email

    while(True):
        try:
            with open (ruta/"Clientes.csv","r",newline="",encoding="utf-8") as file:
                listaVacia = len(list(DictReader(file)))
            break
        except FileNotFoundError:
            with open (ruta/"Clientes.csv", "w", newline="", encoding="utf-8"):
                pass

    with open (ruta/"Clientes.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Mesa","Cantidad_Puestos"])
        if listaVacia:
            writerCSV.writeheader()
        writerCSV.writerows([cliente])
