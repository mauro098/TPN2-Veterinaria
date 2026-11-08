# 📚 Veterinaria — TP Estructuras de Datos

## Descripción

Sistema de consola para gestionar una veterinaria.
Desarrollado como Trabajo Práctico de la materia **Estructuras de Datos**
de la Tecnicatura Universitaria.

El programa implementa **desde cero** las siguientes estructuras de datos:
- Árbol General (n-ario) para la jerarquía de categorías
- Árbol Binario de Búsqueda (BST) para búsqueda eficiente por código

## Integrantes

| Nombre completo       | Legajo  |
| --------------------- | ------- |
| Mirian Alejandra Gomez| *(completar)* |
| Mauro Dermisache      | *(completar)* |
| Erardo Nahuel Perez   | *(completar)* |
| Javier Cerda          | *(completar)* |
| Elias de Sousa        | *(completar)* |

## Cómo ejecutar

```bash
# Desde la carpeta TPN2-Veterinaria/
python main.py
```

**Requisitos:**
- Python 3.10 o superior

## Estructura del proyecto

```
TPN2-Veterinaria/
├── modelos/
│   ├── __init__.py
│   └── paciente.py                  # Clase Libro (dominio)
├── estructuras/
│   ├── __init__.py
│   ├── arbol_categorias.py       # Árbol general n-ario
│   └── arbol_bst.py              # Árbol binario de búsqueda
├── servicios/
│   ├── __init__.py
│   ├── busqueda.py               # Búsquedas secuenciales
│   ├── gestor_pacientes.py       # Modulo de gestion de pacientes
│   └── comparador.py             # Comparación de eficiencia
├── ui/
│   ├── __init__.py
│   └── menu.py                   # Menú de consola
├── main.py                       # Punto de entrada
├── README.md                     # Este archivo
├── USO-DE-IA.md                  # Declaración de uso de IA
└── .gitignore
```

## Funcionalidades y estructuras usadas

| Funcionalidad                     | Estructura de datos       |
| --------------------------------- | ------------------------- |
| Clasificación jerárquica          | Árbol general (n-ario)    |
| Búsqueda eficiente por código     | Árbol binario de búsqueda |
| Búsqueda secuencial               | Lista (recorrido lineal)  |
| Comparación de eficiencia         | Lista + BST               |
