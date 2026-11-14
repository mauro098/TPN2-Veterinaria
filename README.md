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
├── api/
│   ├── __init__.py
│   ├── esquemas.py
│   └── rutas.py
├── datos/
│   └── veterinaria.db
├── estructuras/
│   ├── __init__.py
│   ├── arbol_bst.py
│   └── arbol_categorias.py
├── modelos/
│   ├── __init__.py
│   └── paciente.py
├── servicios/
│   ├── __init__.py
│   ├── busqueda.py
│   ├── comparador.py
│   ├── gestor_pacientes.py
│   ├── gestor_vacunas.py
│   └── persistencia.py
├── ui/
│   ├── __init__.py
│   └── menu.py
├── web/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── USO-DE-IA.md
```

## Funcionalidades y estructuras usadas

| Funcionalidad                     | Estructura de datos       |
| --------------------------------- | ------------------------- |
| Clasificación jerárquica          | Árbol general (n-ario)    |
| Búsqueda eficiente por código     | Árbol binario de búsqueda |
| Búsqueda secuencial               | Lista (recorrido lineal)  |
| Comparación de eficiencia         | Lista + BST               |
