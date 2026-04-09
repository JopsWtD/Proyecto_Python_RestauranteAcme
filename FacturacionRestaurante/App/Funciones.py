from csv import DictWriter
from csv import DictReader
from pathlib import Path
from datetime import datetime

rutaBase = Path(__file__).parent.parent
ruta = rutaBase/"DB"

def crearProducto(codigo, tipoProducto, nombre, valor, iva):
    producto = {}

    producto["Código"] = codigo
    producto["Tipo_Producto"] = tipoProducto
    producto["Nombre"] = nombre
    producto["Valor"] = valor
    producto["IVA"] = iva

    listaProductos = verificarExistencia(ruta,"Productos.csv")

    with open (ruta/"Productos.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Producto","Nombre","Valor","IVA"])
        if not listaProductos:
            writerCSV.writeheader()
        writerCSV.writerows([producto])

def crearMesa(codigo,tipoMesa,puestos):
    mesa = {}

    mesa["Código"] = codigo
    mesa["Tipo_Mesa"] = tipoMesa
    mesa["Cantidad_Puestos"] = puestos

    listaMesas = verificarExistencia(ruta,"Mesas.csv")

    with open (ruta/"Mesas.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Mesa","Cantidad_Puestos"])
        if not listaMesas:
            writerCSV.writeheader()
        writerCSV.writerows([mesa])


def crearCliente(id, nombre, telefono, email):
    cliente = {}
    
    cliente["ID"] = id
    cliente["Nombre"] = nombre
    cliente["Teléfono"] = telefono
    cliente["Email"] = email

    listaClientes = verificarExistencia(ruta,"Clientes.csv")

    with open (ruta/"Clientes.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["ID","Nombre","Teléfono","Email"])
        if not listaClientes:
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
            factura["Fecha"] = datetime.now().strftime("%d/%m/%Y")
            factura["Mesa"] = mesa["Código"]
            factura["ID_CLIENTE"] = cliente["ID"]
            factura["Nombre_Cliente"] = cliente["Nombre"]
            factura["Teléfono"] = cliente["Teléfono"]
            factura["Email"] = cliente["Email"]

            return factura


def asignarCodigoFactura():
    listaFacturas = verificarExistencia(ruta,"Facturas.csv")

    if listaFacturas:
        codigo = int(listaFacturas[-1]["ID_FACTURA"])+1
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
                pedido["Subtotal"] = round(((pedido["Precio_unitario"] + (pedido["Precio_unitario"] * pedido["IVA"] / 100)) * pedido["Cantidad"]), 2)
                return

        pedido = {}
        pedido["ID_FACTURA"] = None
        pedido["ID_PRODUCTO"] = producto["Código"]
        pedido["Nombre_Producto"] = producto["Nombre"]
        pedido["Cantidad"] = cantidad
        pedido["Precio_unitario"] = int(producto["Valor"])
        pedido["IVA"] = int(producto['IVA'])


        pedido["Subtotal"] = round((((pedido["Precio_unitario"] + (pedido["Precio_unitario"] * pedido['IVA'])/100)) * cantidad),2)

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

    for pedido in detalleFactura:
        pedido["ID_FACTURA"] = factura["ID_FACTURA"]

    listaFacturas = verificarExistencia(ruta,"Facturas.csv")

    with open(ruta/"Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_FACTURA","Mesa","Fecha","ID_CLIENTE","Nombre_Cliente","Teléfono","Email"])
        if not listaFacturas:
            writerCSV.writeheader()
        writerCSV.writerows([factura])

    listaDetalles = verificarExistencia(ruta,"Detalle_Facturas.csv")

    with open(ruta/"Detalle_Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_FACTURA","ID_PRODUCTO","Nombre_Producto","Cantidad","Precio_unitario","IVA","Subtotal"])
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

    if detalles and facturas:
        facturasFecha = [f for f in facturas if f["Fecha"] == fecha]

        if facturasFecha:
            reporte = []

            for factura in facturasFecha:
                idFactura = factura["ID_FACTURA"]
                detallesMesa = [d for d in detalles if d["ID_FACTURA"] == idFactura]

                totalProductos = 0
                subtotalBruto = 0
                subtotalIVA = 0

                for d in detallesMesa:
                    totalProductos += int(d["Cantidad"])
                    subtotalBruto += round(float(d["Precio_unitario"]) * int(d["Cantidad"]), 2)
                    subtotalIVA += round((float(d["Precio_unitario"]) * int(d["IVA"]) / 100) * int(d["Cantidad"]), 2)

                subtotal = round(subtotalBruto + subtotalIVA, 2)

                fila = {}
                fila["Mesa"] = factura["Mesa"]
                fila["Total_Productos"] = totalProductos
                fila["Subtotal_Bruto"] = round(subtotalBruto, 2)
                fila["Subtotal_IVA"] = round(subtotalIVA, 2)
                fila["Subtotal"] = subtotal

                reporte.append(fila)

            return reporte


def guardarReporteCSV(reporte, fecha, totalVentaBruta, totalIVA, totalVentas):
    totales = {}
    totales["Fecha"] = fecha
    totales["Mesa"] = "TOTALES"
    totales["Total_Productos"] = 0
    totales["Subtotal_Bruto"] = round(totalVentaBruta, 2)
    totales["Subtotal_IVA"] = round(totalIVA, 2)
    totales["Subtotal"] = round(totalVentas, 2)

    for fila in reporte:
        totales["Total_Productos"] += fila["Total_Productos"]

    listaReportes = verificarExistencia(ruta, "Reporte_Ventas.csv")

    for fila in reporte:
        fila["Fecha"] = fecha

    with open(ruta/"Reporte_Ventas.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(file, fieldnames=["Fecha","Mesa","Total_Productos","Subtotal_Bruto","Subtotal_IVA","Subtotal"])
        if not listaReportes:
            writerCSV.writeheader()
        writerCSV.writerows(reporte)
        writerCSV.writerow(totales)



def verificarExistencia(ruta, archivo):
    while(True):
        try:
            with open(ruta/archivo,"r",newline="",encoding="utf-8") as file:
                lista = list(DictReader(file))
            return lista
        except FileNotFoundError:
            with open(ruta/archivo,"w",newline="",encoding="utf-8") as file:
                pass