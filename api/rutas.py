from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from api.esquemas import (
    PacienteCrear,
    PacienteRespuesta,
    ResultadoBusqueda,
    ReporteComparacion,
    RespuestaMensaje,
    VacunaPendiente,
    TurnoCrear,
    TurnoRespuesta,
)
from servicios.gestor_pacientes import GestorPacientes
from servicios.gestor_vacunas import GestorVacunas
from servicios.busqueda import (
    buscar_por_codigo,
    buscar_por_nombre,
    buscar_por_duenio,
)
from estructuras.arbol_bst import ArbolBST

router = APIRouter()

# Instancia del gestor para esta API
gestor = GestorPacientes()

# Instancia del gestor de vacunas y controles pendientes
gestor_vacunas = GestorVacunas()

# Árbol BST indexado por código para búsquedas eficientes (O(log n))
arbol_codigos = ArbolBST()


def _normalizar_codigo(codigo: str) -> str:
    """Convierte un código de entrada a formato de 3 dígitos con cero a la izquierda."""
    try:
        return f"{int(codigo):03d}"
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El código '{codigo}' no es numérico válido.",
        )


def _reconstruir_arbol():
    """Reconstruye el BST balanceado a partir de la lista actual de pacientes."""
    global arbol_codigos
    pacientes_ordenados = sorted(gestor.lista_pacientes, key=lambda p: p.codigo)
    arbol_codigos = ArbolBST.construir_balanzado(pacientes_ordenados)


# Inicializar el árbol con los datos de prueba cargados por el gestor
_reconstruir_arbol()


# Listar los pacientes
@router.get("/pacientes", response_model=list[PacienteRespuesta])
def listar_pacientes() -> list[PacienteRespuesta]:
    """Retorna una lista con todos los pacientes"""
    return gestor.lista_pacientes


# Obtener un paciente por código (búsqueda en árbol BST)
@router.get("/pacientes/{codigo}", response_model=PacienteRespuesta)
def obtener_paciente(codigo: str):
    """
    Busca un paciente por su código utilizando el árbol BST.
    Es más eficiente que la búsqueda lineal en lista.
    """
    codigo_norm = _normalizar_codigo(codigo)
    paciente, comparaciones = arbol_codigos.buscar(codigo_norm)
    if paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con el código '{codigo}'.",
        )
    return paciente


# Crear un nuevo paciente
@router.post(
    "/pacientes",
    response_model=PacienteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_paciente(paciente: PacienteCrear):
    """Agrega un nuevo paciente al sistema."""
    gestor.insertar_paciente(
        paciente.codigo,
        paciente.nombre,
        paciente.especie,
        paciente.raza,
        paciente.edad,
        paciente.duenio,
        paciente.telefono,
    )
    # Mantener el BST sincronizado con la lista tras la inserción
    _reconstruir_arbol()
    # Retornar el paciente recién creado (último de la lista)
    return gestor.lista_pacientes[-1]


# Buscar pacientes por nombre (búsqueda lineal)
@router.get("/pacientes/buscar/nombre", response_model=ResultadoBusqueda)
def buscar_paciente_por_nombre(
    nombre: str = Query(
        ...,
        description="Nombre de la mascota a buscar.",
        examples=["Firulais"],
    )
):
    """Busca un paciente por nombre mediante búsqueda lineal en la lista."""
    paciente, comparaciones = buscar_por_nombre(
        gestor.lista_pacientes, nombre
    )
    return ResultadoBusqueda(
        paciente=paciente,
        comparaciones=comparaciones,
        metodo="búsqueda lineal por nombre",
    )


# Buscar pacientes por dueño (búsqueda lineal)
@router.get("/pacientes/buscar/duenio", response_model=ResultadoBusqueda)
def buscar_paciente_por_duenio(
    duenio: str = Query(
        ...,
        description="Nombre del dueño a buscar.",
        examples=["Carlos"],
    )
):
    """Busca pacientes por nombre de dueño mediante búsqueda lineal en la lista."""
    mascotas, comparaciones = buscar_por_duenio(
        gestor.lista_pacientes, duenio
    )
    # El esquema ResultadoBusqueda admite un solo paciente; devolvemos el primero.
    paciente = mascotas[0] if mascotas else None
    return ResultadoBusqueda(
        paciente=paciente,
        comparaciones=comparaciones,
        metodo="búsqueda lineal por dueño",
    )


# Búsqueda general por nombre, dueño o código
@router.get("/buscar/general", response_model=list[PacienteRespuesta])
def buscar_paciente_general(
    criterio: str = Query(
        ...,
        description="Criterio de busqueda: nombre, duenio o codigo",
        examples=["nombre"],
    ),
    valor: str = Query(
        ...,
        description="Valor a buscar",
        examples=["Firulais"],
    ),
):
    """Busca pacientes por nombre, dueño o código mediante búsqueda lineal."""
    if criterio == "nombre":
        paciente, _ = buscar_por_nombre(gestor.lista_pacientes, valor)
        return [paciente] if paciente else []

    if criterio == "duenio":
        mascotas, _ = buscar_por_duenio(gestor.lista_pacientes, valor)
        return mascotas or []

    if criterio == "codigo":
        try:
            codigo_str = f"{int(valor):03d}"
        except ValueError:
            return []
        paciente, _ = buscar_por_codigo(gestor.lista_pacientes, codigo_str)
        return [paciente] if paciente else []

    return []


# Modificar un paciente
@router.put("/pacientes/{codigo}", response_model=PacienteRespuesta)
def modificar_paciente(
    codigo: str,
    nueva_edad: int = Query(..., description="Nueva edad del paciente.", examples=[5]),
    nuevo_duenio: str = Query(..., description="Nuevo nombre del dueño.", examples=["Juan"]),
    telefono: str | None = Query(None, description="Nuevo teléfono del dueño.", examples=["300 123 4567"]),
    nuevo_nombre: str | None = Query(None, description="Nuevo nombre del paciente.", examples=["Firulais"]),
    nueva_especie: str | None = Query(None, description="Nueva especie del paciente.", examples=["Perro"]),
    nueva_raza: str | None = Query(None, description="Nueva raza del paciente.", examples=["Labrador"]),
):
    """Modifica los datos de un paciente existente identificado por código."""
    codigo_norm = _normalizar_codigo(codigo)
    exitoso = gestor.modificar_paciente(
        codigo_norm,
        nueva_edad,
        nuevo_duenio,
        telefono,
        nuevo_nombre,
        nueva_especie,
        nueva_raza,
    )
    if not exitoso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con el código '{codigo}'.",
        )
    # Retornar el paciente actualizado (consulta al BST sincronizado)
    paciente, _ = arbol_codigos.buscar(codigo_norm)
    return paciente


# Eliminar un paciente
@router.delete("/pacientes/{codigo}", response_model=RespuestaMensaje)
def eliminar_paciente(codigo: str):
    """Elimina un paciente del sistema por su código."""
    codigo_norm = _normalizar_codigo(codigo)
    exitoso = gestor.eliminar_paciente(codigo_norm)
    if not exitoso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con el código '{codigo}'.",
        )
    # Mantener el BST sincronizado tras la eliminación
    _reconstruir_arbol()
    return RespuestaMensaje(
        mensaje=f"Paciente con código '{codigo}' eliminado correctamente."
    )


# Health check
@router.get("/health")
def health_check():
    """Endpoint de salud de la API."""
    return {"status": "ok"}


# ============================================================
# Endpoints de turnos
# ============================================================

# Horarios disponibles por defecto (mañana, tarde, noche)
_HORARIOS_POR_TURNO = {
    "Mañana": ["09:00", "10:00", "11:00"],
    "Tarde": ["14:00", "15:00", "16:00", "17:00"],
    "Noche": ["18:00", "19:00", "20:00"],
}


@router.get(
    "/turnos/disponibilidad",
    response_model=list[str],
    summary="Horarios disponibles para turnos",
    description="Retorna la lista de horarios disponibles para una fecha y veterinario dados.",
)
def obtener_disponibilidad_turnos(
    fecha: str,
    veterinario: Optional[str] = Query(None, description="Veterinario deseado (opcional)."),
):
    """Devuelve los horarios disponibles para solicitar un turno."""
    # TODO: En una versión futura, consultar turnos ya reservados para esa fecha/veterinario
    # y excluir aquellos horarios ya ocupados.
    todos = []
    for horarios in _HORARIOS_POR_TURNO.values():
        todos.extend(horarios)
    return todos


@router.post(
    "/turnos",
    response_model=TurnoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Solicitar un turno veterinario",
    description="Registra un nuevo turno de consulta veterinaria.",
)
def crear_turno(turno: TurnoCrear):
    """Recibe los datos del turno y devuelve un mensaje de confirmación."""
    return TurnoRespuesta(
        mensaje=f"Turno solicitado para {turno.mascota} el {turno.fecha} a las {turno.horario}."
    )


# Comparar eficiencia: lista lineal vs árbol BST
@router.get("/comparar", response_model=ReporteComparacion)
def comparar_busquedas(
    codigo: str = Query(
        ...,
        description="Código del paciente a buscar en ambas estructuras.",
        examples=["005"],
    )
):
    """
    Compara la eficiencia de búsqueda entre lista lineal y árbol BST
    para un mismo código de paciente.
    """
    codigo_norm = _normalizar_codigo(codigo)
    # Búsqueda en lista lineal
    paciente_lista, comp_lista = buscar_por_codigo(
        gestor.lista_pacientes, codigo_norm
    )
    # Búsqueda en árbol BST
    paciente_bst, comp_bst = arbol_codigos.buscar(codigo_norm)

    busqueda_lista = ResultadoBusqueda(
        paciente=paciente_lista,
        comparaciones=comp_lista,
        metodo="búsqueda lineal en lista",
    )
    busqueda_bst = ResultadoBusqueda(
        paciente=paciente_bst,
        comparaciones=comp_bst,
        metodo="búsqueda en árbol BST",
    )

    ahorro = comp_lista - comp_bst
    porcentaje = (ahorro / comp_lista * 100) if comp_lista > 0 else 0.0

    return ReporteComparacion(
        busqueda_lista=busqueda_lista,
        busqueda_bst=busqueda_bst,
        ahorro_comparaciones=ahorro,
        porcentaje_eficiencia=porcentaje,
    )


# Comparar eficiencia con varios códigos de prueba (inicio, medio, final, inexistente)
@router.get("/comparar/multiplo", response_model=list[ReporteComparacion])
def comparar_multiplo(
    codigos: str = Query(
        "001,015,030,999",
        description="Lista de códigos separados por coma para probar ambos métodos.",
        examples=["001,015,030,999"],
    )
):
    """
    Compara lista lineal vs BST para varios códigos, mostrando cuál método
    es más eficiente en cada caso (según la posición del código buscado).
    """
    codigos_lista = [c.strip() for c in codigos.split(",") if c.strip()]
    resultados = []

    for codigo in codigos_lista:
        try:
            codigo_norm = _normalizar_codigo(codigo)
        except ValueError:
            continue

        paciente_lista, comp_lista = buscar_por_codigo(
            gestor.lista_pacientes, codigo_norm
        )
        paciente_bst, comp_bst = arbol_codigos.buscar(codigo_norm)

        busqueda_lista = ResultadoBusqueda(
            paciente=paciente_lista,
            comparaciones=comp_lista,
            metodo="búsqueda lineal en lista",
        )
        busqueda_bst = ResultadoBusqueda(
            paciente=paciente_bst,
            comparaciones=comp_bst,
            metodo="búsqueda en árbol BST",
        )

        ahorro = comp_lista - comp_bst
        porcentaje = (ahorro / comp_lista * 100) if comp_lista > 0 else 0.0

        resultados.append(
            ReporteComparacion(
                busqueda_lista=busqueda_lista,
                busqueda_bst=busqueda_bst,
                ahorro_comparaciones=ahorro,
                porcentaje_eficiencia=porcentaje,
            )
        )

    return resultados


# Listar vacunas y controles pendientes
@router.get(
    "/vacunas/pendientes",
    response_model=list[VacunaPendiente],
    summary="Vacunas y controles pendientes",
    description="Retorna la lista de vacunas y controles veterinarios pendientes por vencer.",
)
def listar_vacunas_pendientes() -> list[VacunaPendiente]:
    """Retorna los controles pendientes (excluye los marcados como al-día o atendidos)."""
    return gestor_vacunas.listar_pendientes()


# Cambiar el estado de una vacuna o control pendiente
@router.put(
    "/vacunas/{codigo}/estado",
    response_model=VacunaPendiente,
    summary="Cambiar estado de vacuna o control",
    description="Actualiza el estado de una vacuna o control veterinario (ej. pendiente -> atendido).",
)
def cambiar_estado_vacuna(
    codigo: str,
    estado: str = Query(
        ...,
        description="Nuevo estado del control (pendiente, urgente, al-dia, atendido).",
        examples=["atendido"],
    ),
):
    """Cambia el estado de una vacuna o control identificado por código del paciente."""
    codigo_norm = _normalizar_codigo(codigo)
    exitoso = gestor_vacunas.actualizar_estado(codigo_norm, estado)
    if not exitoso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una vacuna o control para el código '{codigo}'.",
        )
    # Retornar la vacuna actualizada
    for v in gestor_vacunas.listar_todos():
        if v.codigo == codigo_norm:
            return v
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró una vacuna o control para el código '{codigo}'.",
    )
