from csv import DictWriter
from csv import DictReader
from pathlib import Path
from datetime import datetime

import App.Utilidades as Utilities

rutaBase = Path(__file__).parent.parent
ruta = rutaBase/"DB"

def crearProducto(codigo, tipoProducto, nombre, valor, iva):
    producto = {}

    producto["Código"] = codigo
    producto["Tipo_Producto"] = tipoProducto
    producto["Nombre"] = nombre
    producto["Valor"] = valor
    producto["IVA"] = iva

    listaProductos = Utilities.verificarExistencia(ruta,"Productos.csv")
    
    productoExistente = next((producto for producto in listaProductos if codigo == int(producto["Código"])),None)
    if not productoExistente:
        with open (ruta/"Productos.csv", "a", newline="", encoding="utf-8") as file:
            writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Producto","Nombre","Valor","IVA"])
            if not listaProductos:
                writerCSV.writeheader()
            writerCSV.writerows([producto])
    else:
        return "ERROR: Ese producto ya había sido registrado antes."

def crearMesa(codigo,tipoMesa,puestos):
    mesa = {}

    mesa["Código"] = codigo
    mesa["Tipo_Mesa"] = tipoMesa
    mesa["Cantidad_Puestos"] = puestos

    listaMesas = Utilities.verificarExistencia(ruta,"Mesas.csv")

    mesaExistente = next((mesa for mesa in listaMesas if codigo == int(mesa["Código"])),None)
    if not mesaExistente:
        with open (ruta/"Mesas.csv", "a", newline="", encoding="utf-8") as file:
            writerCSV = DictWriter(file, fieldnames=["Código","Tipo_Mesa","Cantidad_Puestos"])
            if not listaMesas:
                writerCSV.writeheader()
            writerCSV.writerows([mesa])
    else:
        return "ERROR: Esa mesa ya fue creada anteriormente."


def crearCliente(idCliente, nombre, telefono, email):
    cliente = {}
    
    cliente["ID"] = idCliente
    cliente["Nombre"] = nombre
    cliente["Teléfono"] = telefono
    cliente["Email"] = email

    listaClientes = Utilities.verificarExistencia(ruta,"Clientes.csv")
    
    clienteExistente = next((cliente for cliente in listaClientes if idCliente == int(cliente["ID"])),None)
    if not clienteExistente:
        with open (ruta/"Clientes.csv", "a", newline="", encoding="utf-8") as file:
            writerCSV = DictWriter(file, fieldnames=["ID","Nombre","Teléfono","Email"])
            if not listaClientes:
                writerCSV.writeheader()
            writerCSV.writerows([cliente])
    else:
        return "ERROR: Ese cliente ya está registrado."


def facturar(codigoMesa,idCliente):
    with open(ruta/"Mesas.csv","r",newline="",encoding="utf-8") as file:
        listaMesas = DictReader(file)
        mesa = next((mesa for mesa in listaMesas if codigoMesa == int(mesa["Código"])),None)

    if not mesa:
        return "Mesa no encontrada."
    
    with open(ruta/"Clientes.csv","r",newline="",encoding="utf-8") as file:
        listaClientes = DictReader(file)
        cliente = next((cliente for cliente in listaClientes if idCliente == int(cliente["ID"])), None)

    if not cliente:
        return "Cliente no encontrado."
    
    factura = {}

    factura["ID_FACTURA"] = Utilities.asignarCodigoFactura()
    factura["Fecha"] = datetime.now().strftime("%d/%m/%Y")
    factura["Mesa"] = mesa["Código"]
    factura["ID_CLIENTE"] = cliente["ID"]
    factura["Nombre_Cliente"] = cliente["Nombre"]
    factura["Teléfono"] = cliente["Teléfono"]
    factura["Email"] = cliente["Email"]

    return factura


def agregarProducto(codigoProducto, cantidad, detalleFactura):
    with open(ruta/"Productos.csv","r",newline="",encoding="utf-8") as file:
        listaProductos = list(DictReader(file))
    producto = next((producto for producto in listaProductos if codigoProducto == int(producto["Código"])),None)
    if not producto:
        return "Producto no encontrado."
    
    for pedido in detalleFactura:
        if codigoProducto == pedido["ID_PRODUCTO"]:
            pedido["Cantidad"] += cantidad
            pedido["Subtotal"] = round(((pedido["Precio_unitario"] + (pedido["Precio_unitario"] * pedido["IVA"] / 100)) * pedido["Cantidad"]), 2)
            return "Producto actualizado con éxito."

    pedido = {}
    pedido["ID_FACTURA"] = None
    pedido["ID_PRODUCTO"] = int(producto["Código"])
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

    listaFacturas = Utilities.verificarExistencia(ruta,"Facturas.csv")

    with open(ruta/"Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_FACTURA","Mesa","Fecha","ID_CLIENTE","Nombre_Cliente","Teléfono","Email"])
        if not listaFacturas:
            writerCSV.writeheader()
        writerCSV.writerows([factura])

    listaDetalles = Utilities.verificarExistencia(ruta,"Detalle_Facturas.csv")

    with open(ruta/"Detalle_Facturas.csv","a",newline="",encoding="utf-8") as file:
        writerCSV = DictWriter(file,fieldnames=["ID_FACTURA","ID_PRODUCTO","Nombre_Producto","Cantidad","Precio_unitario","IVA","Subtotal"])
        if not listaDetalles:
            writerCSV.writeheader()
        writerCSV.writerows(detalleFactura)


def guardarFacturaVisual(facturaVisual):
    with open(ruta/"Facturas_Visual.txt","w",encoding="utf-8") as file:
        file.write(facturaVisual)


def generarReporte(fecha):
    listaDetalleFactura = Utilities.verificarExistencia(ruta, "Detalle_Facturas.csv")
    listaFacturas = Utilities.verificarExistencia(ruta, "Facturas.csv")

    if not listaDetalleFactura or not listaFacturas:
        return

    facturasEnFecha = []

    for factura in listaFacturas:
        if factura["Fecha"] == fecha:
            facturasEnFecha.append(factura)

    if len(facturasEnFecha) == 0:
        return

    reporte = []

    for factura in facturasEnFecha:
        idFactura = factura["ID_FACTURA"]

        detalleFactura = []

        for pedido in listaDetalleFactura:
            if pedido["ID_FACTURA"] == str(idFactura):
                detalleFactura.append(pedido)

        totalProductos = 0
        subtotalBruto = 0
        subtotalIVA = 0

        for pedido in detalleFactura:
            cantidad = int(pedido["Cantidad"])
            precio = float(pedido["Precio_unitario"])
            iva = int(pedido["IVA"])

            totalProductos += cantidad
            subtotalBruto += precio * cantidad
            subtotalIVA += (precio * iva / 100) * cantidad

        subtotal = subtotalBruto + subtotalIVA

        fila = {}
        fila["Mesa"] = factura["Mesa"]
        fila["Total_Productos"] = totalProductos
        fila["Subtotal_Bruto"] = round(subtotalBruto, 2)
        fila["Subtotal_IVA"] = round(subtotalIVA, 2)
        fila["Subtotal"] = round(subtotal, 2)

        reporte.append(fila)

    return reporte


def guardarReporteCSV(reporte, fecha, totalVentaBruta, totalIVA, totalVentas):
    totales = {}
    totales["Fecha"] = fecha
    totales["Tipo"] = "TOTAL"
    totales["Mesa"] = ""
    totales["Total_Productos"] = 0
    totales["Subtotal_Bruto"] = round(totalVentaBruta, 2)
    totales["Subtotal_IVA"] = round(totalIVA, 2)
    totales["Subtotal"] = round(totalVentas, 2)

    for filaReporte in reporte:
        totales["Total_Productos"] += filaReporte["Total_Productos"]

    listaReportes = Utilities.verificarExistencia(ruta, "Reporte_Ventas.csv")

    for filaReporte in reporte:
        filaReporte["Fecha"] = fecha
        filaReporte["Tipo"] = "DETALLE"

    with open(ruta/"Reporte_Ventas.csv", "a", newline="", encoding="utf-8") as file:
        writerCSV = DictWriter(
            file,
            fieldnames=["Fecha","Tipo","Mesa","Total_Productos","Subtotal_Bruto","Subtotal_IVA","Subtotal"]
        )
        if not listaReportes:
            writerCSV.writeheader()
        writerCSV.writerows(reporte)
        writerCSV.writerow(totales)

def busquedaFacturas(fechaInicio,fechaFin):
    facturasConsultadas = []

    listaFacturas = Utilities.verificarExistencia(ruta,"Facturas.csv")
    if not listaFacturas:
        return "Actualmente no hay facturas en el sistema."
    
    listaDetalles = Utilities.verificarExistencia(ruta,"Detalle_Facturas.csv")

    for factura in listaFacturas:
        if fechaInicio <= factura["Fecha"] <= fechaFin:
            facturasConsultadas.append(factura)
    
    totalProductos = totalizarProductosVendidos(facturasConsultadas,listaDetalles)
                
    totalProductos = ordenarProductosPorUnidadesVendidas(totalProductos)

    listarProductosMenosVendidos(totalProductos)


def totalizarProductosVendidos(facturasConsultadas, listaDetalles):

    totalProductos = {}
    idValida = {factura["ID_FACTURA"] for factura in facturasConsultadas}

    for detalle in listaDetalles:
        if detalle["ID_FACTURA"] in idValida:
            nombre = detalle["Nombre_Producto"]
            cantidad = int(detalle["Cantidad"])

            if nombre in totalProductos:
                totalProductos[nombre] += cantidad
            else:
                totalProductos[nombre] = cantidad
    return [{"Nombre": key, "Cantidad": value} for key,value in totalProductos.items()]


def ordenarProductosPorUnidadesVendidas(totalProductos):
    totalProductosOrdenados = []

    for i in range(0,len(totalProductos)):
        actual = None
        productoAgregar = None

        for producto in totalProductos:
            if producto not in totalProductosOrdenados:
                if actual == None or int(producto["Cantidad"]) < actual:
                    actual = int(producto["Cantidad"])
                    productoAgregar = producto

        totalProductosOrdenados.append(productoAgregar)
    return totalProductosOrdenados


def listarProductosMenosVendidos(totalProductos):
    productosMostrar = totalProductos[:5]
    print("TOP 5 productos menos vendidos:")
    for i,producto in enumerate(productosMostrar, start = 1):
            print(f"{i}. {producto['Nombre']} ({producto['Cantidad']} unidades vendidas).")