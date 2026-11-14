"""Gestor de vacunas y controles pendientes.

Mantiene una lista en memoria de controles veterinarios programados,
con datos de prueba vinculados a los pacientes existentes.
"""

from modelos.paciente import Paciente


class VacunaPendiente:
    """Representa una vacuna o control pendiente de una mascota."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tipo: str,
        icono: str = "fa-syringe",
        estado: str = "pendiente",
        fecha: str = "",
        diasRestantes: int | None = None,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.icono = icono
        self.estado = estado
        self.fecha = fecha
        self.diasRestantes = diasRestantes

    def to_dict(self) -> dict:
        """Serializa el control a diccionario para respuesta JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "icono": self.icono,
            "estado": self.estado,
            "fecha": self.fecha,
            "diasRestantes": self.diasRestantes,
        }


class GestorVacunas:
    """Gestor en memoria de vacunas y controles pendientes."""

    def __init__(self):
        self.lista_vacunas: list[VacunaPendiente] = []
        self._cargar_datos_prueba()

    def _cargar_datos_prueba(self):
        """Carga controles de prueba vinculados a pacientes existentes."""
        datos_prueba = [
            VacunaPendiente("001", "Firulais", "Rabia", "fa-syringe", "urgente", "2026-11-18", 5),
            VacunaPendiente("002", "Michi", "Triple felina", "fa-syringe", "pendiente", "2026-11-25", 12),
            VacunaPendiente("003", "Roco", "Moquillo", "fa-syringe", "pendiente", "2026-11-28", 15),
            VacunaPendiente("004", "Luna", "Desparasitación interna", "fa-pills", "pendiente", "2026-12-02", 19),
            VacunaPendiente("005", "Piolín", "Control de plumas", "fa-feather", "urgente", "2026-11-15", 2),
            VacunaPendiente("006", "Boby", "Bordetella", "fa-syringe", "pendiente", "2026-12-10", 27),
            VacunaPendiente("007", "Simba", "Leucemia felina", "fa-syringe", "pendiente", "2026-12-05", 22),
            VacunaPendiente("008", "Thor", "Control geriátrico", "fa-stethoscope", "pendiente", "2026-12-15", 32),
            VacunaPendiente("009", "Lola", "Leptospirosis", "fa-syringe", "al-dia", "2026-10-20", None),
            VacunaPendiente("010", "Manchas", "Vacuna anual", "fa-syringe", "pendiente", "2026-12-01", 18),
        ]
        self.lista_vacunas = datos_prueba

    def listar_pendientes(self) -> list[VacunaPendiente]:
        """Retorna todos los controles pendientes (excluye los al día y atendidos)."""
        return [
            v for v in self.lista_vacunas if v.estado not in ("al-dia", "atendido")
        ]

    def listar_todos(self) -> list[VacunaPendiente]:
        """Retorna todos los controles registrados."""
        return list(self.lista_vacunas)

    def actualizar_estado(self, codigo: str, nuevo_estado: str) -> bool:
        """Cambia el estado de una vacuna/control por su código."""
        for v in self.lista_vacunas:
            if v.codigo == codigo:
                v.estado = nuevo_estado
                return True
        return False
