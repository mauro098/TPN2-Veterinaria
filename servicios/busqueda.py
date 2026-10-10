
# Función búsqueda por código, devuelve el paciente y la cantidad de comparaciones
def buscar_por_codigo(lista_pacientes: list, codigo: str) -> tuple:
    contador = 0
    for paciente in lista_pacientes:
        contador += 1
        if paciente.codigo == codigo:
            return (paciente, contador)
    return (None, contador)


# Función búsqueda por nombre, devuelve el paciente y la cantidad de comparaciones
def buscar_por_nombre(lista_pacientes: list, nombre: str) -> tuple:
    contador = 0
    nombre_salida = nombre.lower()
    for paciente in lista_pacientes:
        contador += 1
        if paciente.nombre.lower() == nombre_salida:
            return (paciente, contador)
    return (None, contador)

# Función búsqueda por dueño, devuelve el paciente y la cantidad de comparaciones
def buscar_por_duenio(lista_pacientes: list, duenio: str)-> tuple:
    contador = 0
    # Guarda todas las mascotas del dueño
    mascotas = []
    duenio_salida = duenio.lower()
    for paciente in lista_pacientes:
        contador += 1
        if paciente.duenio.lower() == duenio_salida:
            mascotas.append(paciente)
    if len(mascotas) > 0:
        return (mascotas, contador)
    return (None, contador)
