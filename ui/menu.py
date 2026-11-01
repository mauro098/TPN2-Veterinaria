from servicios.gestor_pacientes import GestorPacientes
from servicios.busqueda import buscar_por_codigo, buscar_por_nombre, buscar_por_duenio

def mostrar_opciones():
    print("\n" + "=" * 40)
    print("      SISTEMA DE GESTIÓN VETERINARIA")
    print("=" * 40)
    print("1. Listar todos los pacientes")
    print("2. Buscar paciente (por código, nombre o dueño)")
    print("3. Agregar nuevo paciente")
    print("4. Modificar paciente")
    print("5. Eliminar paciente")
    print("0. Salir")
    print("=" * 40)

def ejecutar_menu():
    gestor = GestorPacientes()

    while True:
        mostrar_opciones()
        opcion = input("\nIngrese el número de opción deseada: ").strip()

        if opcion == "1":
            print("\n--- [1] LISTADO DE PACIENTES ---")
            if not gestor.lista_pacientes:
                print("No hay pacientes registrados.")
            else:
                for p in gestor.lista_pacientes:
                    print(p)

        elif opcion == "2":
            print("\n--- [2] BÚSQUEDA DE PACIENTES ---")
            print("a. Buscar por Código")
            print("b. Buscar por Nombre de mascota")
            print("c. Buscar por Nombre de dueño")
            sub_op = input("Elija opción (a/b/c): ").strip().lower()

            if sub_op == "a":
                cod = input("Ingrese el código: ").strip()
                paciente, comp = buscar_por_codigo(gestor.lista_pacientes, cod)
                if paciente:
                    print(f"\nEncontrado: {paciente}")
                else:
                    print("\nNo se encontró ningún paciente con ese código.")
                print(f"[Comparaciones realizadas: {comp}]")

            elif sub_op == "b":
                nom = input("Ingrese el nombre de la mascota: ").strip()
                paciente, comp = buscar_por_nombre(gestor.lista_pacientes, nom)
                if paciente:
                    print(f"\nEncontrado: {paciente}")
                else:
                    print("\nNo se encontró ninguna mascota con ese nombre.")
                print(f"[Comparaciones realizadas: {comp}]")

            elif sub_op == "c":
                due = input("Ingrese el nombre del dueño: ").strip()
                mascotas, comp = buscar_por_duenio(gestor.lista_pacientes, due)
                if mascotas:
                    print(f"\nMascotas encontradas ({len(mascotas)}):")
                    for m in mascotas:
                        print(m)
                else:
                    print("\nNo se encontraron mascotas para ese dueño.")
                print(f"[Comparaciones realizadas: {comp}]")
            else:
                print("Opción de búsqueda no válida.")

        elif opcion == "3":
            print("\n--- [3] AGREGAR PACIENTE ---")
            codigo = input("Código (ej. P031): ").strip()
            nombre = input("Nombre de la mascota: ").strip()
            especie = input("Especie (ej. Perro/Gato): ").strip()
            raza = input("Raza: ").strip()
            try:
                edad = int(input("Edad: ").strip())
            except ValueError:
                print("Edad inválida. Debe ser un número.")
                continue
            duenio = input("Nombre del dueño: ").strip()

            gestor.insertar_paciente(codigo, nombre, especie, raza, edad, duenio)

        elif opcion == "4":
            print("\n--- [4] MODIFICAR PACIENTE ---")
            codigo = input("Ingrese el código del paciente a modificar: ").strip()
            try:
                nueva_edad = int(input("Nueva edad: ").strip())
            except ValueError:
                print("Edad inválida.")
                continue
            nuevo_duenio = input("Nuevo nombre de dueño: ").strip()

            gestor.modificar_paciente(codigo, nueva_edad, nuevo_duenio)

        elif opcion == "5":
            print("\n--- [5] ELIMINAR PACIENTE ---")
            codigo = input("Ingrese el código del paciente a eliminar: ").strip()
            gestor.eliminar_paciente(codigo)

        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema de veterinaria!\n")
            break

        else:
            print("\n [!] Opción no válida. Ingrese un número del 0 al 5.")
