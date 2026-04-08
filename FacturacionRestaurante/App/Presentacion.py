import App.Funciones as Funciones

def crearProducto():
    opcion = ""
    print("Para la creación de un producto, necesitamos los siguientes datos:")
    while(opcion < 1 or opcion > 3):
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
        if iva >=1 and iva <= 20:
            break
        else:
            if iva <= 0:
                print("El IVA no puede ser un número negativo.")
            if iva > 30:
                print("Nuestro restaurante no maneja más de un 30% DE IVA en sus productos.")
    
    Funciones.crearProducto(tipoProducto,codigo,nombre,valor,iva)
    print("El producto {nombre} se creó correctamente.")    


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
            telefono.insert(0,+57 )
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