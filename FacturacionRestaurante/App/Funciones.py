from csv import DictWriter
from csv import DictReader
from pathlib import Path
from datetime import datetime

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
                listaVacia = len(list(DictReader(file))) == 0
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
                listaVacia = len(list(DictReader(file))) == 0
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
    cliente["Teléfono"] = telefono
    cliente["Email"] = email

    while(True):
        try:
            with open (ruta/"Clientes.csv","r",newline="",encoding="utf-8") as file:
                listaVacia = len(list(DictReader(file))) == 0
            break
        except FileNotFoundError:
            with open (ruta/"Clientes.csv", "w", newline="", encoding="utf-8"):
                pass

    with open (ruta/"Clientes.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["ID","Nombre","Teléfono","Email"])
        if listaVacia:
            writerCSV.writeheader()
        writerCSV.writerows([cliente])

def facturar(codigoMesa,idCliente):
    with open(ruta/"Mesas.csv","r",newline="",encoding="utf-8") as file:
        listaMesas = DictReader(file)
        mesa = next((mesa for mesa in listaMesas if codigoMesa == mesa["Código"]),None)
    if mesa:
        with open(ruta/"Clientes.csv","r",newline="",encoding="utf-8") as file:
            listaClientes = DictReader(file)
            cliente = next((cliente for cliente in listaClientes if idCliente == cliente["ID"]), None)
        if cliente:
            factura = {}

            factura["ID_FACTURA"] = asignarCodigoFactura()
            factura["Fecha"] = datetime.now()
            factura["Mesa"] = mesa["Código"]
            factura["ID_CLIENTE"] = cliente["ID"]
            factura["Nombre_Cliente"] = cliente["Nombre"]
            factura["Teléfono"] = cliente["Teléfono"]
            factura["Email"] = cliente["Email"]

            return factura


def asignarCodigoFactura():
    with open(ruta/"Facturas.csv","r",newline="",encoding="utf-8") as file:
        listaFacturas = list(DictReader(file))

    if listaFacturas:
        codigo = listaFacturas[-1]["ID_FACTURA"]+1
    else:
        codigo = 1
    return codigo


def agregarProducto(codigoProducto, cantidad, detalleFactura):
    with open(ruta/"Productos.csv","r",newline="",encoding="utf-8") as file:
        listaProductos = list(DictReader(file))
    producto = next((producto for producto in listaProductos if codigoProducto == producto["Código"]),None)

    if producto:
        for pedido in detalleFactura:
            if codigoProducto == pedido["ID_PRODUCTO"]:
                pedido["Cantidad"] += cantidad
                return

        pedido = {}

        pedido["ID_PRODUCTO"] = producto["Código"]
        pedido["Nombre_Producto"] = producto["Nombre"]
        pedido["Cantidad"] = cantidad
        pedido["Precio_unitario"] = int(producto["Valor"])
        pedido["IVA"] = int(producto['IVA'])
        pedido["Subtotal"] = round(((int(producto["Valor"]) + (int(producto["Valor"]) * int(producto['IVA'])/100)) * cantidad),2)

        detalleFactura.append(pedido)
        

def sacarProducto(codigoProducto, cantidad, detalleFactura):
    for pedido in detalleFactura:
        if codigoProducto == pedido["ID_PRODUCTO"]:
            if cantidad <= pedido["Cantidad"]:
                pedido["Cantidad"] -= cantidad
                pedido["Subtotal"] = round(((pedido["Precio_unitario"] + (pedido["Precio_unitario"] * pedido['IVA']/100)) * pedido["Cantidad"]),2)
                if pedido["Cantidad"] == 0:
                    detalleFactura.remove(pedido)
                break
            else:
                return f"No se pudo eliminar {cantidad} unidades de {pedido['Nombre_Producto']} porque solo hay {pedido['Cantidad']}"


def guardarInformacionFactura(factura, detalleFactura):

    listaFacturas = verificarExistencia(ruta,"Facturas.csv")

    with open(ruta/"Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_FACTURA","Mesa","Fecha","ID_CLIENTE","Nombre_Cliente","Teléfono","Email"])
        if not listaFacturas:
            writerCSV.writeheader()
        writerCSV.writerows([factura])

    listaDetalles = verificarExistencia(ruta,"Detalle_Facturas.csv")

    with open(ruta/"Detalle_Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_PRODUCTO","Nombre_Producto","Cantidad","Precio_unitario","IVA","Subtotal"])
        if not listaDetalles:
            writerCSV.writeheader()
        writerCSV.writerows(detalleFactura)


def guardarFacturaVisual(facturaVisual):
    with open(ruta/"Facturas_Visual.txt","a") as file:
        file.write(facturaVisual)
        file.write("\n")


def generarReporte(fecha):
    detalles = verificarExistencia(ruta, "Detalle_Facturas.csv")
    facturas = verificarExistencia(ruta, "Facturas.csv")

    if not detalles or not facturas:
        return []

    facturasFecha = [f for f in facturas if datetime.strptime(f["Fecha"][:10], "%Y-%m-%d").strftime("%d/%m/%Y") == fecha]

    if not facturasFecha:
        return []

    reporte = []

    for factura in facturasFecha:
        idFactura = factura["ID_FACTURA"]
        detallesMesa = [d for d in detalles if d["ID_FACTURA"] == idFactura]

        totalProductos = sum(int(d["Cantidad"]) for d in detallesMesa)
        subtotalBruto = sum(round(float(d["Precio_unitario"]) * int(d["Cantidad"]), 2) for d in detallesMesa)
        subtotalIVA = sum(round((float(d["Precio_unitario"]) * int(d["IVA"]) / 100) * int(d["Cantidad"]), 2) for d in detallesMesa)
        subtotal = round(subtotalBruto + subtotalIVA, 2)

        reporte.append({
            "Mesa": factura["Mesa"],
            "Total_Productos": totalProductos,
            "Subtotal_Bruto": subtotalBruto,
            "Subtotal_IVA": subtotalIVA,
            "Subtotal": subtotal
        })

    return reporte




def verificarExistencia(ruta, archivo):
    while(True):
        try:
            with open(ruta/archivo,"r",newline="",encoding="utf-8") as file:
                lista = list(DictReader(file))
            return lista
        except FileNotFoundError:
            with open(ruta/archivo,"w",newline="",encoding="utf-8") as file:
                pass
