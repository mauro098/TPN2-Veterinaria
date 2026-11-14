"""Esquemas Pydantic para la API de la veterinaria.

Define los modelos de entrada y salida de los endpoints REST, con
validaciones Field(), descripciones y ejemplos para la documentación
interactiva Swagger UI (/docs).
"""

from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class PacienteBase(BaseModel):
    """Campos comunes de un paciente (mascota)."""

    nombre: str = Field(
        ...,
        description="Nombre de la mascota.",
        examples=["Max"],
    )
    especie: str = Field(
        ...,
        description="Especie de la mascota (perro, gato, etc.).",
        examples=["Perro"],
    )
    raza: str = Field(
        ...,
        description="Raza de la mascota.",
        examples=["Labrador Retriever"],
    )
    edad: int = Field(
        ...,
        description="Edad de la mascota en años. Debe ser mayor o igual a 0.",
        examples=[3],
        ge=0,
    )
    duenio: str = Field(
        ...,
        description="Nombre del dueño de la mascota.",
        examples=["Juan Pérez"],
    )
    telefono: Optional[str] = Field(
        None,
        description="Teléfono de contacto del dueño.",
        examples=["300 123 4567"],
    )


class PacienteCrear(PacienteBase):
    """Esquema para recibir peticiones POST de creación de pacientes."""

    codigo: str = Field(
        ...,
        description="Código único del paciente (ej. '001', '101').",
        examples=["101"],
        min_length=1,
    )


class PacienteRespuesta(PacienteBase):
    """Esquema de respuesta de un paciente, serializable desde objetos ORM."""

    codigo: str = Field(
        ...,
        description="Código único del paciente (ej. '001', '101').",
        examples=["101"],
    )

    model_config = ConfigDict(from_attributes=True)


class ResultadoBusqueda(BaseModel):
    """Resultado de una búsqueda de pacientes."""

    paciente: Optional[PacienteRespuesta] = Field(
        None,
        description="Paciente encontrado, o None si no se encontró ningún resultado.",
        examples=[None],
    )
    comparaciones: int = Field(
        ...,
        description="Cantidad de comparaciones realizadas durante la búsqueda.",
        examples=[5],
    )
    metodo: str = Field(
        ...,
        description="Método de búsqueda utilizado (lista lineal o árbol BST).",
        examples=["búsqueda lineal"],
    )


class ReporteComparacion(BaseModel):
    """Respuesta del endpoint /api/comparar."""

    busqueda_lista: ResultadoBusqueda = Field(
        ...,
        description="Resultado de la búsqueda en lista lineal.",
    )
    busqueda_bst: ResultadoBusqueda = Field(
        ...,
        description="Resultado de la búsqueda en árbol BST.",
    )
    ahorro_comparaciones: int = Field(
        ...,
        description="Cantidad de comparaciones ahorradas al usar BST en lugar de lista.",
        examples=[3],
    )
    porcentaje_eficiencia: float = Field(
        ...,
        description="Porcentaje de eficiencia obtenida con el BST respecto a la lista.",
        examples=[60.0],
    )


class RespuestaMensaje(BaseModel):
    """Respuesta de texto para confirmaciones de borrado o avisos."""

    mensaje: str = Field(
        ...,
        description="Mensaje de confirmación o aviso.",
        examples=["Paciente eliminado correctamente."],
    )


class VacunaPendiente(BaseModel):
    """Esquema de respuesta para una vacuna o control pendiente."""

    codigo: str = Field(
        ...,
        description="Código del paciente (mascota).",
        examples=["001"],
    )
    nombre: str = Field(
        ...,
        description="Nombre de la mascota.",
        examples=["Firulais"],
    )
    tipo: str = Field(
        ...,
        description="Tipo de vacuna o control pendiente.",
        examples=["Rabia"],
    )
    icono: str = Field(
        "fa-syringe",
        description="Clase de icono de FontAwesome para la tarjeta.",
        examples=["fa-syringe"],
    )
    estado: str = Field(
        ...,
        description="Estado del control: urgente, pendiente o al-dia.",
        examples=["urgente"],
    )
    fecha: str = Field(
        ...,
        description="Fecha programada del control (ISO o texto legible).",
        examples=["2026-11-20"],
    )
    diasRestantes: int | None = Field(
        None,
        description="Días restantes para el vencimiento del control.",
        examples=[5],
    )

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# Esquemas para los endpoints de turnos
# ============================================================

class TurnoCrear(BaseModel):
    """Esquema de entrada para crear un turno (POST /api/turnos)."""

    duenio: str = Field(
        ...,
        description="Nombre del dueño de la mascota.",
        examples=["Juan Pérez"],
    )
    telefono: str = Field(
        ...,
        description="Teléfono de contacto del dueño.",
        examples=["300 123 4567"],
    )
    email: Optional[str] = Field(
        None,
        description="Correo electrónico del dueño (opcional).",
        examples=["juan@example.com"],
    )
    mascota: str = Field(
        ...,
        description="Nombre de la mascota.",
        examples=["Firulais"],
    )
    especie: str = Field(
        ...,
        description="Especie de la mascota.",
        examples=["Perro"],
    )
    motivo: str = Field(
        ...,
        description="Motivo de la consulta veterinaria.",
        examples=["Vacunación anual"],
    )
    fecha: str = Field(
        ...,
        description="Fecha del turno (formato YYYY-MM-DD).",
        examples=["2026-11-20"],
    )
    horario: str = Field(
        ...,
        description="Horario del turno (formato HH:MM).",
        examples=["09:00"],
    )
    veterinario: Optional[str] = Field(
        None,
        description="Veterinario asignado (opcional).",
        examples=["Dra. Ana Martínez"],
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones adicionales del turno.",
        examples=["La mascota es algo nerviosa."],
    )


class TurnoRespuesta(BaseModel):
    """Esquema de respuesta para la creación de un turno."""

    mensaje: str = Field(
        ...,
        description="Mensaje de confirmación del turno solicitado.",
        examples=["Turno solicitado correctamente."],
    )

    model_config = ConfigDict(from_attributes=True)

