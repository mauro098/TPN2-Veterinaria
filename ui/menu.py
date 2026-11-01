def mostrar_opciones():
    print("\n" + "=" * 40)
    print("      SISTEMA DE GESTIÓN VETERINARIA")
    print("=" * 40)
    print("1. Listar todos los pacientes")
    print("2. Buscar paciente (por nombre o dueño)")
    print("3. Agregar nuevo paciente")
    print("4. Modificar paciente")
    print("5. Eliminar paciente")
    print("0. Salir")
    print("=" * 40)

def ejecutar_menu():
    while True:
        mostrar_opciones()
        opcion = input("\nIngrese el número de opción deseada: ").strip()

        if opcion == "1":
            print("\n--- [1] LISTADO DE PACIENTES ---")
            print("Función en desarrollo por el equipo...")
        elif opcion == "2":
            print("\n--- [2] BÚSQUEDA DE PACIENTES ---")
            busqueda = input("Ingrese el término a buscar: ").strip()
            print(f"Buscando '{busqueda}'...")
        elif opcion == "3":
            print("\n--- [3] AGREGAR PACIENTE ---")
            nombre = input("Nombre de la mascota: ").strip()
            print(f"Paciente '{nombre}' registrado temporalmente.")
        elif opcion == "4":
            print("\n--- [4] MODIFICAR PACIENTE ---")
            codigo = input("Ingrese el código del paciente: ").strip()
            print(f"Modificando paciente {codigo}...")
        elif opcion == "5":
            print("\n--- [5] ELIMINAR PACIENTE ---")
            codigo = input("Ingrese el código del paciente a eliminar: ").strip()
            print(f"Eliminando paciente {codigo}...")
        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema de veterinaria!\n")
            break
        else:
            print("\n [!] Opción no válida. Ingrese un número del 0 al 5.")
