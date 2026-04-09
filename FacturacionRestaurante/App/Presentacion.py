import Funciones
from datetime import datetime

def crearProducto():
    opcion = ""
    print("Para la creación de un producto, necesitamos los siguientes datos:")
    while(opcion not in ("1","2","3")):
        print("El producto a añadir es:\n1.Bebida\n2.Platillo\n3.Postre")
        opcion = input("Opción ->")
        match(opcion):
            case "1":
                tipoProducto = "Bebida"
            case "2":
                tipoProducto = "Platillo"
            case "3":
                tipoProducto = "Postre"
            case _:
                print("Opción inválida. Intente de nuevo.")

    while(True):
        codigo = input("Código del producto -> ").strip()
        if codigo.isdigit():
            break
        print("El código solo puede contener números.")

    nombre = input("Nombre del producto -> ").title()

    while(True):
        try:
            valor = float(input("Valor del producto -> "))
            break
        except ValueError:
            print("El campo (Precio) solo puede contener números.")
    
    while(True):
        try:
            iva = int(input("IVA aplicable al producto -> "))
        except ValueError:
            print("El campo (IVA) tiene que tener valor numérico.")
            continue
        if iva >=1 and iva <= 29:
            break
        else:
            if iva < 1:
                print("El IVA no puede ser nulo ni negativo.")
            if iva > 30:
                print("Nuestro restaurante no maneja más de un 30% DE IVA en sus productos.")
    
    Funciones.crearProducto(codigo,tipoProducto,nombre,valor,iva)
    print(f"El producto {nombre} se creó correctamente.")    


def crearMesa():
    print("Para crear una mesa, necesitamos los siguientes datos: ")

    while(True):
        codigo = input("Código de la mesa -> ").strip()
        if codigo.isdigit():
            break
        print("El código solo puede contener números.")

    while(True):
        try:
            puestos = int(input("Cantidad de puestos -> "))
        except ValueError:
            print("El campo (Puestos) solo puede contener números.")
            continue

        if puestos > 0 and puestos <= 50:
            if puestos == 1:
                tipoMesa = "Individual"
            elif puestos == 2:
                tipoMesa = "Pareja"
            elif puestos >= 3 and puestos <= 16:
                tipoMesa = "Familiar"
            else:
                tipoMesa = "Corporación"
            break
        else:
            if puestos <= 0:
                print("Una mesa no puede tener una cantidad nula o negativa de puestos.")
            if puestos > 50:
                print("Nuestro restaurante no tiene capacidad para una mesa con más de 50 puestos.")

    Funciones.crearMesa(codigo,tipoMesa,puestos)
    print("Se creó la mesa correctamente.")

def crearCliente():
    print("Para crear un cliente, necesitamos los siguientes datos: ")

    while(True):
        id = input("Identificación -> ").strip()
        if id.isdigit():
            break
        print("El ID solo puede contener números.")
        continue

    nombre = input("Nombre del cliente -> ").title()

    while(True):
        telefono = input("Número de teléfono -> ").strip()
        if telefono.isdigit():
            telefono = f"+57 {telefono}"
            break
        print("El número de teléfono solo puede contener números.")
        continue
    
    while(True):
        texto = ""
        email = input("Correo electrónico -> ")
        if "@" in email:
            texto += email[email.find("@")+1:]
            if texto in ("gmail.com","hotmail.com","hotmail.es"):
                break
        print("El correo electrónico no es válido o no está soportado por nuestros servidores. (Gmail o Hotmail)")
    
    Funciones.crearCliente(id,nombre,telefono,email)
    print(f"El cliente {nombre} se creó correctamente.")


def inicioFacturacion():
    print("Para empezar un proceso de factuación, necesitamos los siguientes datos:")

    
    while(True):
        codigoMesa = input("Código de la mesa -> ").strip()
        if codigoMesa.isdigit():
            break
        print("El código solo puede contener números.")

    while(True):
        idCliente = input("Identificación -> ").strip()
        if idCliente.isdigit():
            break
        print("El ID solo puede contener números.")
        continue

    factura = Funciones.facturar(codigoMesa,idCliente)
    if factura:
        iniciarVenta(factura)


def iniciarVenta(factura):
    detalleFactura = []
    opcion = ""

    while(opcion != "0"):
        print("-"*35)
        print("""¿Qué quieres hacer a continuación?
    1. Agregar productos al pedido
    2. Sacar productos del pedido
    0. Finalizar pedido""")
        print("-"*35)
        opcion = input("Número de opción -> ")
        match(opcion):

            case "1":
                agregarProducto(detalleFactura)
            case "2":
                sacarProducto(detalleFactura)
            case "0":
                finalizarPedido(factura, detalleFactura)


def agregarProducto(detalleFactura):
    print("Para agregar un producto:")
    while(True):
        codigoProducto = input("Código del producto -> ").strip()
        if codigoProducto.isdigit():
            break
        print("El código solo puede contener números.")
    while(True):
        try:
            cantidad = int(input("Cantidad a añadir -> "))
        except ValueError:
            print("La cantidad solo puede contener números.")
            continue

        if cantidad > 0:
            break
        print("El campo (CANTIDAD) no puede ser negativo ni nulo.")

    Funciones.agregarProducto(codigoProducto,cantidad,detalleFactura)


def sacarProducto(detalleFactura):
    if len(detalleFactura) > 0:
        print("Para sacar un producto:")
        while(True):
            codigoProducto = input("Código del producto -> ").strip()
            if codigoProducto.isdigit():
                break
            print("El código solo puede contener números.")
        while(True):
            try:
                cantidad = int(input("Cantidad a añadir -> "))
            except ValueError:
                print("La cantidad solo puede contener números.")
                continue

            if cantidad > 0:
                break
            print("El campo (CANTIDAD) no puede ser negativo ni nulo.")

        for pedido in detalleFactura:
            if codigoProducto == pedido["ID_PRODUCTO"]:
                mensaje = Funciones.sacarProducto(codigoProducto,cantidad,detalleFactura)
                if mensaje:
                    print(mensaje)
                else:
                    print(f"Se quitaron {cantidad} unidades de {pedido['Nombre_Producto']} éxitosamente.")
            else:
                print("Ese producto no está en el pedido.")

    else:
        print("No se puede sacar productos del pedido porque está vacío.")

def finalizarPedido(factura, detalleFactura):
    print("Pedido finalizado: Generando factura...")
    Funciones.guardarInformacionFactura(factura,detalleFactura)
    
    facturaVisual = f"""
==========================================
            ACME RESTAURANT
==========================================
Fecha: {factura['Fecha']}
Mesa: {factura['Mesa']}
------------------------------------------
CLIENTE:
Nombre: {factura['Nombre_Cliente']}
ID: {factura['ID_CLIENTE']}
Tel: {factura['Teléfono']}
Email: {factura['Email']}
------------------------------------------
DETALLE:
Cod | Producto | Cant | V.Unit | IVA | Subtotal
"""
    totalFactura = 0
    for p in detalleFactura:
        linea = f"{p['ID_PRODUCTO']} | {p['Nombre_Producto']} | {p['Cantidad']} | {p['Precio_unitario']} | {p['IVA']}% | {p['Subtotal']}\n"
        facturaVisual += linea
        total_factura += float(p["Subtotal"])

    facturaVisual += "------------------------------------------"
    facturaVisual += f"\nTOTAL A PAGAR: ${round(totalFactura, 2)}"
    facturaVisual += "\n==========================================\n"

    print(facturaVisual)

    while(True):
        respuesta = input("¿Quiere guardar la factura?").title()
        if respuesta in ("Si","Sí"):
            print("Guardando la factura...")
            Funciones.guardarFacturaVisual(facturaVisual)
            break
        elif respuesta in ("No"):
            print("Ha elegido no guardar la factura.")
            break
        print("Opción inválida.")

def reporteVentas():
    while True:
        fecha = input("Ingrese la fecha para el reporte (DD/MM/AAAA) -> ").strip()
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            break
        except ValueError:
            print("Formato de fecha inválido. Use DD/MM/AAAA.")

    reporte = Funciones.generarReporte(fecha)

    if not reporte:
        print(f"No se encontraron ventas para la fecha {fecha}.")
        return

    reporteVisual = f"""
==========================================
        REPORTE DE VENTAS - ACME
==========================================
Fecha: {fecha}
------------------------------------------
Mesa | Total Productos | Subtotal Bruto | Subtotal IVA | Subtotal
"""

    totalVentaBruta = 0
    totalIVA = 0
    totalVentas = 0

    for fila in reporte:
        linea = f"{fila['Mesa']} | {fila['Total_Productos']} | ${fila['Subtotal_Bruto']} | ${fila['Subtotal_IVA']} | ${fila['Subtotal']}\n"
        reporteVisual += linea
        totalVentaBruta += fila["Subtotal_Bruto"]
        totalIVA += fila["Subtotal_IVA"]
        totalVentas += fila["Subtotal"]

    reporteVisual += "------------------------------------------"
    reporteVisual += f"\nTotal Venta Bruta: ${round(totalVentaBruta, 2)}"
    reporteVisual += f"\nTotal IVA: ${round(totalIVA, 2)}"
    reporteVisual += f"\nTotal Ventas: ${round(totalVentas, 2)}"
    reporteVisual += "\n==========================================\n"

    print(reporteVisual)

    while True:
        respuesta = input("¿Desea imprimir el reporte en CSV? -> ").title()
        if respuesta in ("Si", "Sí"):
            Funciones.guardarReporteCSV(reporte, fecha, totalVentaBruta, totalIVA, totalVentas)
            print("Reporte guardado exitosamente.")
            break
        elif respuesta == "No":
            print("Ha elegido no guardar el reporte.")
            break
        print("Opción inválida.")