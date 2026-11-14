import os
import sqlite3

from modelos.paciente import Paciente


def obtener_conexion(ruta_db: str = 'datos/veterinaria.db') -> sqlite3.Connection:
    directorio = os.path.dirname(ruta_db)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
    return sqlite3.connect(ruta_db)


def inicializar_db(ruta_db: str = 'datos/veterinaria.db') -> None:
    with obtener_conexion(ruta_db) as conn:
        conn.execute(
            'CREATE TABLE IF NOT EXISTS pacientes ('
            'codigo TEXT PRIMARY KEY, '
            'nombre TEXT, '
            'especie TEXT, '
            'raza TEXT, '
            'edad INTEGER, '
            'duenio TEXT, '
            'telefono TEXT)'
        )


def guardar_paciente(paciente: Paciente, ruta_db: str = 'datos/veterinaria.db') -> bool:
    with obtener_conexion(ruta_db) as conn:
        conn.execute(
            'INSERT OR REPLACE INTO pacientes '
            '(codigo, nombre, especie, raza, edad, duenio, telefono) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                paciente.codigo,
                paciente.nombre,
                paciente.especie,
                paciente.raza,
                paciente.edad,
                paciente.duenio,
                paciente.telefono,
            ),
        )
    return True


def obtener_paciente_por_codigo(codigo: str, ruta_db: str = 'datos/veterinaria.db') -> Paciente | None:
    with obtener_conexion(ruta_db) as conn:
        fila = conn.execute(
            'SELECT codigo, nombre, especie, raza, edad, duenio, telefono FROM pacientes WHERE codigo = ?',
            (codigo,),
        ).fetchone()
    if fila is None:
        return None
    return Paciente(*fila)


def obtener_todos_los_pacientes(ruta_db: str = 'datos/veterinaria.db') -> list[Paciente]:
    with obtener_conexion(ruta_db) as conn:
        filas = conn.execute(
            'SELECT codigo, nombre, especie, raza, edad, duenio, telefono FROM pacientes'
        ).fetchall()
    return [
        Paciente(codigo, nombre, especie, raza, edad, duenio, telefono)
        for codigo, nombre, especie, raza, edad, duenio, telefono in filas
    ]


def actualizar_paciente(codigo: str, paciente: Paciente, ruta_db: str = 'datos/veterinaria.db') -> bool:
    with obtener_conexion(ruta_db) as conn:
        cursor = conn.execute(
            'UPDATE pacientes SET nombre = ?, especie = ?, raza = ?, edad = ?, duenio = ?, telefono = ? WHERE codigo = ?',
            (
                paciente.nombre,
                paciente.especie,
                paciente.raza,
                paciente.edad,
                paciente.duenio,
                paciente.telefono,
                codigo,
            ),
        )
        actualizado = cursor.rowcount > 0
    return actualizado


def eliminar_paciente(codigo: str, ruta_db: str = 'datos/veterinaria.db') -> bool:
    with obtener_conexion(ruta_db) as conn:
        cursor = conn.execute(
            'DELETE FROM pacientes WHERE codigo = ?',
            (codigo,),
        )
        eliminado = cursor.rowcount > 0
    return eliminado
